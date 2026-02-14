from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _str_to_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class TelemetryConfig:
    enabled: bool
    sink: str
    flush_events: int
    flush_seconds: int
    session_flush_seconds: int
    app_version: str
    max_buffer: int
    spaces_bucket: str
    spaces_region: str
    spaces_endpoint: str
    spaces_access_key_id: str
    spaces_secret_access_key: str
    spaces_prefix: str


def _default_sink() -> str:
    if os.environ.get("SPACES_BUCKET"):
        return "stdout+spaces"
    return "stdout"


def get_config() -> TelemetryConfig:
    return TelemetryConfig(
        enabled=_str_to_bool(os.environ.get("LOGGING_ENABLED"), True),
        sink=os.environ.get("LOG_SINK", _default_sink()),
        flush_events=int(os.environ.get("LOG_FLUSH_EVENTS", "25")),
        flush_seconds=int(os.environ.get("LOG_FLUSH_SECONDS", "5")),
        session_flush_seconds=int(os.environ.get("LOG_SESSION_FLUSH_SECONDS", "60")),
        app_version=os.environ.get("APP_VERSION", "dev"),
        max_buffer=int(os.environ.get("LOG_MAX_BUFFER", "1000")),
        spaces_bucket=os.environ.get("SPACES_BUCKET", ""),
        spaces_region=os.environ.get("SPACES_REGION", ""),
        spaces_endpoint=os.environ.get("SPACES_ENDPOINT", ""),
        spaces_access_key_id=os.environ.get("SPACES_ACCESS_KEY_ID", ""),
        spaces_secret_access_key=os.environ.get("SPACES_SECRET_ACCESS_KEY", ""),
        spaces_prefix=os.environ.get("SPACES_PREFIX", "telemetry/"),
    )
