"""Authentication domain models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthUser:
    """Authenticated account tracked across sessions for quota enforcement."""

    user_id: str
    email: str
    display_name: str | None = None


@dataclass(frozen=True)
class AuthLoginResult:
    user: AuthUser
    access_token: str | None = None
    refresh_token: str | None = None


@dataclass(frozen=True)
class AuthCredentials:
    email: str
    password: str


@dataclass(frozen=True)
class SignUpRequest:
    email: str
    password: str
    display_name: str | None = None
