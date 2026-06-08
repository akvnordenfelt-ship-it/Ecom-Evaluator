"""Persistent per-account evaluation quota storage."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Protocol

from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT, PROJECT_ROOT, QUOTA_STORE_PATH


class QuotaStore(Protocol):
    def get_used_count(self, user_id: str) -> int: ...

    def increment_used(self, user_id: str) -> int: ...


class FileQuotaStore:
    """JSON file store for development and single-node deployments."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or QUOTA_STORE_PATH
        self._lock = threading.Lock()

    def _load(self) -> dict[str, int]:
        if not self._path.exists():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        if not isinstance(raw, dict):
            return {}
        return {str(k): int(v) for k, v in raw.items() if isinstance(v, (int, float))}

    def _save(self, data: dict[str, int]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_used_count(self, user_id: str) -> int:
        with self._lock:
            return self._load().get(user_id, 0)

    def increment_used(self, user_id: str) -> int:
        with self._lock:
            data = self._load()
            next_count = data.get(user_id, 0) + 1
            data[user_id] = next_count
            self._save(data)
            return next_count


class SupabaseQuotaStore:
    """
    Supabase-backed quota store.

    Expects a `user_evaluations` table:
      user_id text primary key,
      evaluations_used integer not null default 0
    """

    def __init__(self, *, url: str, key: str, table: str = "user_evaluations") -> None:
        self._url = url
        self._key = key
        self._table = table
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError(
                "Supabase quota store requires the `supabase` package. "
                "Install with: pip install supabase"
            ) from exc
        self._client = create_client(self._url, self._key)
        return self._client

    def get_used_count(self, user_id: str) -> int:
        client = self._get_client()
        response = (
            client.table(self._table)
            .select("evaluations_used")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return 0
        return int(rows[0].get("evaluations_used", 0))

    def increment_used(self, user_id: str) -> int:
        client = self._get_client()
        current = self.get_used_count(user_id)
        next_count = current + 1
        if current == 0:
            client.table(self._table).insert(
                {"user_id": user_id, "evaluations_used": next_count}
            ).execute()
        else:
            client.table(self._table).update({"evaluations_used": next_count}).eq(
                "user_id", user_id
            ).execute()
        return next_count


def get_quota_store() -> QuotaStore:
    from ecom_evaluator.auth.providers import get_auth_settings

    settings = get_auth_settings()
    if settings.quota_backend == "supabase":
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise RuntimeError("Supabase URL and anon key are required for quota storage.")
        return SupabaseQuotaStore(url=settings.supabase_url, key=settings.supabase_anon_key)
    return FileQuotaStore()


def evaluations_remaining(*, user_id: str, used_count: int | None = None) -> int:
    used = used_count if used_count is not None else get_quota_store().get_used_count(user_id)
    return max(0, FREE_EVALUATIONS_PER_ACCOUNT - used)


def quota_status_label(*, user_id: str) -> str:
    remaining = evaluations_remaining(user_id=user_id)
    if remaining == 1:
        return "1 free evaluation left on your account"
    if remaining > 1:
        return f"{remaining} free evaluations left on your account"
    return "Free evaluations used — upgrade to Premium"
