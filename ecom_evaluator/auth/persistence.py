"""Browser-local auth persistence for cross-tab login sync."""

from __future__ import annotations

import base64
import json
from typing import Any
from urllib.parse import unquote

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.auth.models import AuthLoginResult, AuthUser
from ecom_evaluator.auth.providers.base import get_auth_settings
from ecom_evaluator.exceptions import AnalysisError

STORAGE_KEY = "productscore_auth"
AUTH_COOKIE_NAME = "ps_auth"
_AUTH_SYNC_QUERY_KEYS = (
    "ps_auth_sync",
    "ps_logout",
    "ps_dev_user",
    "access_token",
    "refresh_token",
)


def encode_auth_cookie(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_auth_cookie(value: str) -> dict[str, Any]:
    padded = value + "=" * (-len(value) % 4)
    raw = base64.urlsafe_b64decode(padded.encode("ascii"))
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Auth cookie payload must be an object.")
    return data


def build_browser_auth_payload() -> dict[str, Any] | None:
    """Serialize the current server session for browser storage."""
    user = st.session_state.get("auth_user")
    if not isinstance(user, AuthUser):
        return None

    settings = get_auth_settings()
    payload: dict[str, Any] = {
        "v": 1,
        "provider": settings.provider,
        "user_id": user.user_id,
        "email": user.email,
        "display_name": user.display_name,
    }
    refresh_token = st.session_state.get("auth_refresh_token")
    if refresh_token:
        payload["refresh_token"] = str(refresh_token)
    return payload


def _parse_cookie_header(header: str, name: str) -> str | None:
    for part in header.split(";"):
        part = part.strip()
        if not part.startswith(f"{name}="):
            continue
        return unquote(part.split("=", 1)[1])
    return None


def _get_browser_cookie(name: str) -> str | None:
    try:
        value = st.context.cookies.get(name)
        if value:
            return str(value)
    except Exception:
        pass

    try:
        header = st.context.headers.get("Cookie") or st.context.headers.get("cookie") or ""
    except Exception:
        return None
    return _parse_cookie_header(header, name)


def _clear_auth_sync_query_params() -> None:
    for key in _AUTH_SYNC_QUERY_KEYS:
        if key in st.query_params:
            del st.query_params[key]


def _restore_dev_user(data: dict[str, Any]) -> AuthUser:
    settings = get_auth_settings()
    if settings.provider != "dev":
        raise AnalysisError("Saved sign-in data could not be restored for this auth provider.")

    if not data.get("user_id") or not data.get("email"):
        raise AnalysisError("Saved sign-in data is incomplete.")

    return AuthUser(
        user_id=str(data["user_id"]),
        email=str(data["email"]),
        display_name=data.get("display_name"),
    )


def _restore_supabase_tokens(*, access_token: str, refresh_token: str) -> AuthLoginResult:
    from ecom_evaluator.auth.providers.supabase_provider import SupabaseAuthProvider

    settings = get_auth_settings()
    if settings.provider != "supabase":
        raise AnalysisError("Saved sign-in data could not be restored for this auth provider.")

    provider = SupabaseAuthProvider(url=settings.supabase_url, anon_key=settings.supabase_anon_key)
    user = provider.complete_session_tokens(access_token=access_token, refresh_token=refresh_token)
    return AuthLoginResult(user=user, access_token=access_token, refresh_token=refresh_token)


def _restore_supabase_refresh(refresh_token: str) -> AuthLoginResult:
    from ecom_evaluator.auth.providers.supabase_provider import SupabaseAuthProvider

    settings = get_auth_settings()
    if settings.provider != "supabase":
        raise AnalysisError("Saved sign-in data could not be restored for this auth provider.")

    provider = SupabaseAuthProvider(url=settings.supabase_url, anon_key=settings.supabase_anon_key)
    return provider.refresh_session(refresh_token=refresh_token)


def _restore_from_payload(data: dict[str, Any]) -> AuthLoginResult | AuthUser:
    provider = data.get("provider")
    if provider == "supabase":
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        if access_token and refresh_token:
            return _restore_supabase_tokens(
                access_token=str(access_token),
                refresh_token=str(refresh_token),
            )
        if refresh_token:
            return _restore_supabase_refresh(refresh_token=str(refresh_token))
        raise AnalysisError("Saved sign-in data is missing session tokens.")

    if provider == "dev":
        return _restore_dev_user(data)

    raise AnalysisError("Saved sign-in data uses an unsupported auth provider.")


def restore_auth_from_browser_cookie() -> bool:
    """
    Restore auth from the shared browser cookie on the first request in a new tab.
    Returns True when auth was restored (caller should rerun).
    """
    settings = get_auth_settings()
    if not settings.auth_required:
        return False
    if st.session_state.get("auth_user") is not None:
        return False

    raw_cookie = _get_browser_cookie(AUTH_COOKIE_NAME)
    if not raw_cookie:
        return False

    from ecom_evaluator.auth.session import set_auth_user

    try:
        data = decode_auth_cookie(raw_cookie)
        restored = _restore_from_payload(data)
        if isinstance(restored, AuthLoginResult):
            set_auth_user(
                restored.user,
                access_token=restored.access_token,
                refresh_token=restored.refresh_token,
            )
        else:
            set_auth_user(restored)
        return True
    except (ValueError, json.JSONDecodeError):
        st.session_state["auth_browser_clear"] = True
        st.session_state["auth_error"] = None
        return False
    except AnalysisError:
        return False


def handle_auth_logout_sync() -> bool:
    """Apply a logout triggered from another browser tab."""
    if st.query_params.get("ps_logout") != "1":
        return False

    from ecom_evaluator.auth.session import logout_user

    logout_user()
    _clear_auth_sync_query_params()
    return True


def handle_auth_restore() -> bool:
    """
    Restore a session from localStorage via one-time query params.
    Returns True when auth was restored (caller should rerun).
    """
    if st.query_params.get("ps_auth_sync") != "1":
        return False

    from ecom_evaluator.auth.session import set_auth_user

    if st.session_state.get("auth_user") is not None:
        _clear_auth_sync_query_params()
        return False

    access_token = st.query_params.get("access_token")
    refresh_token = st.query_params.get("refresh_token")
    if access_token and refresh_token:
        try:
            result = _restore_supabase_tokens(
                access_token=str(access_token),
                refresh_token=str(refresh_token),
            )
            set_auth_user(
                result.user,
                access_token=result.access_token,
                refresh_token=result.refresh_token,
            )
            _clear_auth_sync_query_params()
            return True
        except AnalysisError:
            st.session_state["auth_browser_clear"] = True
            st.session_state["auth_error"] = None
            _clear_auth_sync_query_params()
            return False

    if refresh_token and not access_token:
        try:
            result = _restore_supabase_refresh(refresh_token=str(refresh_token))
            set_auth_user(
                result.user,
                access_token=result.access_token,
                refresh_token=result.refresh_token,
            )
            _clear_auth_sync_query_params()
            return True
        except AnalysisError:
            st.session_state["auth_browser_clear"] = True
            st.session_state["auth_error"] = None
            _clear_auth_sync_query_params()
            return False

    dev_blob = st.query_params.get("ps_dev_user")
    if dev_blob:
        try:
            raw = base64.b64decode(str(dev_blob).encode("ascii"), validate=True)
            user = _restore_dev_user(json.loads(raw.decode("utf-8")))
            set_auth_user(user)
            _clear_auth_sync_query_params()
            return True
        except AnalysisError:
            st.session_state["auth_browser_clear"] = True
            st.session_state["auth_error"] = None
            _clear_auth_sync_query_params()
            return False

    _clear_auth_sync_query_params()
    return False


def install_auth_sync_bridge() -> None:
    """Keep browser cookie/localStorage in sync and restore sessions in other tabs."""
    settings = get_auth_settings()
    if not settings.auth_required:
        return

    payload = build_browser_auth_payload()
    payload_json = json.dumps(payload)
    cookie_name = json.dumps(AUTH_COOKIE_NAME)
    clear_browser_auth = bool(st.session_state.pop("auth_browser_clear", False))

    components.html(
        f"""
        <script>
        (function () {{
            const win = window.parent;
            const doc = win.document;
            const STORAGE_KEY = {json.dumps(STORAGE_KEY)};
            const COOKIE_NAME = {cookie_name};
            const serverAuth = {payload_json};
            const clearBrowserAuth = {json.dumps(clear_browser_auth)};
            const secure = win.location.protocol === "https:";

            function readStored() {{
                try {{
                    const raw = win.localStorage.getItem(STORAGE_KEY);
                    return raw ? JSON.parse(raw) : null;
                }} catch (error) {{
                    return null;
                }}
            }}

            function writeStored(data) {{
                try {{
                    if (!data) {{
                        win.localStorage.removeItem(STORAGE_KEY);
                        return;
                    }}
                    win.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
                }} catch (error) {{
                    /* localStorage may be unavailable in strict browser modes */
                }}
            }}

            function toBase64Url(value) {{
                return btoa(unescape(encodeURIComponent(value)))
                    .replace(/\\+/g, "-")
                    .replace(/\\//g, "_")
                    .replace(/=+$/, "");
            }}

            function writeCookie(data) {{
                const base = "path=/; SameSite=Lax" + (secure ? "; Secure" : "");
                if (!data) {{
                    doc.cookie = COOKIE_NAME + "=; " + base + "; max-age=0";
                    return;
                }}
                const encoded = toBase64Url(JSON.stringify(data));
                doc.cookie = COOKIE_NAME + "=" + encodeURIComponent(encoded) + "; " + base + "; max-age=2592000";
            }}

            function authPayloadsMatch(left, right) {{
                return JSON.stringify(left) === JSON.stringify(right);
            }}

            function buildRestoreUrl(stored) {{
                const params = new URLSearchParams(win.location.search);
                params.set("ps_auth_sync", "1");
                params.delete("access_token");
                params.delete("refresh_token");
                if (stored.refresh_token && stored.provider === "supabase") {{
                    params.set("refresh_token", stored.refresh_token);
                    return win.location.pathname + "?" + params.toString();
                }}
                if (stored.provider === "dev" && stored.user_id && stored.email) {{
                    const devUser = JSON.stringify({{
                        user_id: stored.user_id,
                        email: stored.email,
                        display_name: stored.display_name || null,
                    }});
                    params.set("ps_dev_user", btoa(unescape(encodeURIComponent(devUser))));
                    return win.location.pathname + "?" + params.toString();
                }}
                return null;
            }}

            const params = new URLSearchParams(win.location.search);
            if (params.get("ps_logout") === "1" || clearBrowserAuth) {{
                writeStored(null);
                writeCookie(null);
                return;
            }}

            if (params.get("ps_auth_sync") === "1") {{
                return;
            }}

            if (serverAuth) {{
                const stored = readStored();
                if (!authPayloadsMatch(stored, serverAuth)) {{
                    writeStored(serverAuth);
                }}
                writeCookie(serverAuth);
                return;
            }}

            const stored = readStored();
            if (stored) {{
                const restoreUrl = buildRestoreUrl(stored);
                if (restoreUrl && params.get("ps_auth_sync") !== "1") {{
                    win.location.replace(restoreUrl);
                    return;
                }}
                return;
            }}
        }})();

        (function () {{
            const win = window.parent;
            const doc = win.document;
            const STORAGE_KEY = {json.dumps(STORAGE_KEY)};
            const COOKIE_NAME = {cookie_name};
            if (win.__psAuthSyncInstalled) {{
                return;
            }}
            win.__psAuthSyncInstalled = true;

            win.addEventListener("storage", (event) => {{
                if (event.key !== STORAGE_KEY) {{
                    return;
                }}

                const params = new URLSearchParams(win.location.search);
                if (params.get("ps_auth_sync") === "1" || params.get("ps_logout") === "1") {{
                    return;
                }}

                if (!event.newValue) {{
                    doc.cookie = COOKIE_NAME + "=; path=/; max-age=0; SameSite=Lax";
                    win.location.replace(win.location.pathname + "?ps_logout=1");
                    return;
                }}

                win.location.reload();
            }});
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
