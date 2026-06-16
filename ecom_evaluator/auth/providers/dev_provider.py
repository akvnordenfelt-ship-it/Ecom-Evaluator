"""Local development auth provider (replace with Supabase in production)."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
from pathlib import Path

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.exceptions import AnalysisError


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def _hash_password(password: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
    return digest


class DevAuthProvider:
    """File-backed email/password auth for local testing only."""

    def __init__(self, *, users_path: str | Path) -> None:
        self._path = Path(users_path)

    def provider_label(self) -> str:
        return "Development auth"

    def _load_users(self) -> dict[str, dict[str, str]]:
        if not self._path.exists():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return raw if isinstance(raw, dict) else {}

    def _save_users(self, users: dict[str, dict[str, str]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(users, indent=2), encoding="utf-8")

    def sign_up(self, request: SignUpRequest) -> AuthLoginResult:
        email = _normalize_email(request.email)
        if not _valid_email(email):
            raise AnalysisError("Enter a valid email address.")
        if len(request.password) < 8:
            raise AnalysisError("Password must be at least 8 characters.")

        users = self._load_users()
        if email in users:
            raise AnalysisError("An account with this email already exists. Log in instead.")

        user_id = secrets.token_hex(12)
        salt = secrets.token_hex(8)
        users[email] = {
            "user_id": user_id,
            "email": email,
            "display_name": (request.display_name or email.split("@")[0]).strip(),
            "salt": salt,
            "password_hash": _hash_password(request.password, salt),
        }
        self._save_users(users)
        return AuthLoginResult(
            user=AuthUser(user_id=user_id, email=email, display_name=users[email]["display_name"])
        )

    def login(self, credentials: AuthCredentials) -> AuthLoginResult:
        email = _normalize_email(credentials.email)
        users = self._load_users()
        record = users.get(email)
        if not record:
            raise AnalysisError("No account found for that email. Create an account first.")
        expected = record.get("password_hash", "")
        salt = record.get("salt", "")
        if _hash_password(credentials.password, salt) != expected:
            raise AnalysisError("Incorrect email or password.")

        return AuthLoginResult(
            user=AuthUser(
                user_id=record["user_id"],
                email=record["email"],
                display_name=record.get("display_name"),
            )
        )
