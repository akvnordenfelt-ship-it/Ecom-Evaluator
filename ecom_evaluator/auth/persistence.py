"""Browser-local auth persistence for cross-tab login sync."""

from __future__ import annotations

import base64
import json
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.auth.models import AuthLoginResult, AuthUser
from ecom_evaluator.auth.providers.base import get_auth_settings
from ecom_evaluator.auth.providers.supabase_provider import user_from_supabase_record
from ecom_evaluator.exceptions import AnalysisError

STORAGE_KEY = "productscore_auth"
_AUTH_SYNC_QUERY_KEYS = (
    "ps_auth_sync",
    "ps_logout",
    "ps_dev_user",
    "access_token",
    "refresh_token",
)


def build_browser_auth_payload() -> dict[str, Any] | None:
    """Serialize the current server session for localStorage."""
    user = st.session_state.get("auth_user")
    if not isinstance(user, AuthUser):
        return None

    settings = get_auth_settings()
    payload: dict[str, Any] = {
        "provider": settings.provider,
        "user_id": user.user_id,
        "email": user.email,
        "display_name": user.display_name,
    }
    access_token = st.session_state.get("auth_access_token")
    refresh_token = st.session_state.get("auth_refresh_token")
    if access_token and refresh_token:
        payload["access_token"] = str(access_token)
        payload["refresh_token"] = str(refresh_token)
    return payload


def _clear_auth_sync_query_params() -> None:
    for key in _AUTH_SYNC_QUERY_KEYS:
        if key in st.query_params:
            del st.query_params[key]


def _restore_dev_user(encoded: str) -> AuthUser:
    settings = get_auth_settings()
    if settings.provider != "dev":
        raise AnalysisError("Cross-tab sign-in is only supported for the active auth provider.")

    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, json.JSONDecodeError) as exc:
        raise AnalysisError("Saved sign-in data could not be restored.") from exc

    if not isinstance(data, dict) or not data.get("user_id") or not data.get("email"):
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
        raise AnalysisError("Cross-tab sign-in is only supported for the active auth provider.")

    provider = SupabaseAuthProvider(url=settings.supabase_url, anon_key=settings.supabase_anon_key)
    user = provider.complete_session_tokens(access_token=access_token, refresh_token=refresh_token)
    return AuthLoginResult(user=user, access_token=access_token, refresh_token=refresh_token)


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

    from ecom_evaluator.auth.session import set_auth_error, set_auth_user

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
        except AnalysisError as exc:
            set_auth_error(str(exc))
            _clear_auth_sync_query_params()
            return False

    dev_blob = st.query_params.get("ps_dev_user")
    if dev_blob:
        try:
            user = _restore_dev_user(str(dev_blob))
            set_auth_user(user)
            _clear_auth_sync_query_params()
            return True
        except AnalysisError as exc:
            set_auth_error(str(exc))
            _clear_auth_sync_query_params()
            return False

    _clear_auth_sync_query_params()
    return False


def install_auth_sync_bridge() -> None:
    """Keep localStorage in sync and restore sessions in new tabs."""
    settings = get_auth_settings()
    if not settings.auth_required:
        return

    payload = build_browser_auth_payload()
    payload_json = json.dumps(payload)

    components.html(
        f"""
        <script>
        (function () {{
            const win = window.parent;
            const STORAGE_KEY = {json.dumps(STORAGE_KEY)};
            const serverAuth = {payload_json};

            function readStored() {{
                try {{
                    const raw = win.localStorage.getItem(STORAGE_KEY);
                    return raw ? JSON.parse(raw) : null;
                }} catch (error) {{
                    return null;
                }}
            }}

            function writeStored(data) {{
                if (!data) {{
                    win.localStorage.removeItem(STORAGE_KEY);
                    return;
                }}
                win.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
            }}

            function authPayloadsMatch(left, right) {{
                return JSON.stringify(left) === JSON.stringify(right);
            }}

            function buildRestoreUrl(stored) {{
                const params = new URLSearchParams();
                params.set("ps_auth_sync", "1");
                if (stored.access_token && stored.refresh_token) {{
                    params.set("access_token", stored.access_token);
                    params.set("refresh_token", stored.refresh_token);
                    return win.location.pathname + "?" + params.toString();
                }}
                if (stored.provider === "dev" && stored.user_id && stored.email) {{
                    const devUser = JSON.stringify({{
                        user_id: stored.user_id,
                        email: stored.email,
                        display_name: stored.display_name || null,
                    }});
                    params.set(
                        "ps_dev_user",
                        btoa(unescape(encodeURIComponent(devUser)))
                    );
                    return win.location.pathname + "?" + params.toString();
                }}
                return null;
            }}

            const params = new URLSearchParams(win.location.search);
            if (params.get("ps_auth_sync") === "1" || params.get("ps_logout") === "1") {{
                return;
            }}

            if (serverAuth) {{
                const stored = readStored();
                if (!authPayloadsMatch(stored, serverAuth)) {{
                    writeStored(serverAuth);
                }}
                return;
            }}

            const stored = readStored();
            if (!stored) {{
                return;
            }}

            const restoreUrl = buildRestoreUrl(stored);
            if (restoreUrl) {{
                win.location.replace(restoreUrl);
            }}
        }})();

        (function () {{
            const win = window.parent;
            const STORAGE_KEY = {json.dumps(STORAGE_KEY)};
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
                    win.location.replace(win.location.pathname + "?ps_logout=1");
                    return;
                }}

                let stored = null;
                try {{
                    stored = JSON.parse(event.newValue);
                }} catch (error) {{
                    return;
                }}

                const nextParams = new URLSearchParams();
                nextParams.set("ps_auth_sync", "1");
                if (stored.access_token && stored.refresh_token) {{
                    nextParams.set("access_token", stored.access_token);
                    nextParams.set("refresh_token", stored.refresh_token);
                    win.location.replace(win.location.pathname + "?" + nextParams.toString());
                    return;
                }}
                if (stored.provider === "dev" && stored.user_id && stored.email) {{
                    const devUser = JSON.stringify({{
                        user_id: stored.user_id,
                        email: stored.email,
                        display_name: stored.display_name || null,
                    }});
                    nextParams.set(
                        "ps_dev_user",
                        btoa(unescape(encodeURIComponent(devUser)))
                    );
                    win.location.replace(win.location.pathname + "?" + nextParams.toString());
                }}
            }});
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
