from __future__ import annotations

import json
import os
import sys
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st


@dataclass(frozen=True)
class TelemetryConfig:
    enabled: bool
    log_dir: Path
    flush_events: int
    flush_seconds: int
    session_flush_seconds: int
    app_version: str


def _str_to_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _default_log_dir() -> Path:
    env_dir = os.environ.get("LOG_DIR")
    if env_dir:
        return Path(env_dir)
    if Path("/.dockerenv").exists() or os.environ.get("RUNNING_IN_DOCKER") == "true":
        return Path("/app/data/logs")
    return Path("data/logs")


def get_config() -> TelemetryConfig:
    return TelemetryConfig(
        enabled=_str_to_bool(os.environ.get("LOGGING_ENABLED"), True),
        log_dir=_default_log_dir(),
        flush_events=int(os.environ.get("LOG_FLUSH_EVENTS", "25")),
        flush_seconds=int(os.environ.get("LOG_FLUSH_SECONDS", "5")),
        session_flush_seconds=int(os.environ.get("LOG_SESSION_FLUSH_SECONDS", "60")),
        app_version=os.environ.get("APP_VERSION", "dev"),
    )


def _safe_mkdir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _get_state() -> dict:
    return st.session_state


def _ensure_session_id() -> str:
    state = _get_state()
    if "telemetry_session_id" not in state:
        state["telemetry_session_id"] = os.urandom(12).hex()
    return state["telemetry_session_id"]


def _get_paths(config: TelemetryConfig, date_str: str | None = None) -> dict[str, Path]:
    date_str = date_str or _today_date()
    events_dir = config.log_dir / "events" / f"date={date_str}"
    sessions_dir = config.log_dir / "sessions" / f"date={date_str}"
    errors_dir = config.log_dir / "errors" / f"date={date_str}"
    _safe_mkdir(events_dir)
    _safe_mkdir(sessions_dir)
    _safe_mkdir(errors_dir)
    return {
        "events": events_dir / "events.jsonl",
        "sessions": sessions_dir / "sessions.parquet",
        "errors": errors_dir / "errors.jsonl",
    }


def _json_dumps(payload: Any) -> str:
    try:
        return json.dumps(payload, default=str)
    except Exception:
        return json.dumps({"payload": str(payload)})


def _append_jsonl(path: Path, lines: list[str]) -> None:
    if not lines:
        return
    try:
        _safe_mkdir(path.parent)
        with open(path, "a", encoding="utf-8") as handle:
            try:
                import fcntl  # type: ignore

                fcntl.flock(handle, fcntl.LOCK_EX)
            except Exception:
                pass
            handle.write("\n".join(lines) + "\n")
            handle.flush()
            try:
                os.fsync(handle.fileno())
            except Exception:
                pass
            try:
                import fcntl  # type: ignore

                fcntl.flock(handle, fcntl.LOCK_UN)
            except Exception:
                pass
    except Exception as exc:
        print(f"Telemetry write failed: {exc}")


def _flush_event_buffer(config: TelemetryConfig) -> None:
    state = _get_state()
    buffer = state.get("telemetry_buffer", [])
    if not buffer:
        return
    paths = _get_paths(config)
    lines = [_json_dumps(event) for event in buffer]
    _append_jsonl(paths["events"], lines)
    state["telemetry_buffer"] = []
    state["telemetry_last_flush"] = time.time()


def _buffer_event(config: TelemetryConfig, event: dict) -> None:
    state = _get_state()
    buffer = state.get("telemetry_buffer")
    if buffer is None:
        buffer = []
        state["telemetry_buffer"] = buffer
    buffer.append(event)
    state["telemetry_event_count"] = int(state.get("telemetry_event_count", 0)) + 1
    state["telemetry_last_page"] = event.get("page", "")
    if event.get("event_type") == "error":
        state["telemetry_error_count"] = int(state.get("telemetry_error_count", 0)) + 1
    if event.get("event_type") == "page_view":
        pages = state.get("telemetry_pages")
        if pages is None:
            pages = set()
        pages.add(event.get("page", ""))
        state["telemetry_pages"] = pages
    now = time.time()
    last_flush = state.get("telemetry_last_flush", 0)
    if len(buffer) >= config.flush_events or (now - last_flush) >= config.flush_seconds:
        _flush_event_buffer(config)
    last_session_flush = state.get("telemetry_last_session_flush", 0)
    if event.get("event_type") == "page_view" or (now - last_session_flush) >= config.session_flush_seconds:
        _write_session_snapshot(config)


def _write_session_snapshot(config: TelemetryConfig) -> None:
    state = _get_state()
    session_id = _ensure_session_id()
    pages = sorted(state.get("telemetry_pages", set()))
    now = time.time()
    started = state.get("telemetry_started_ts", now)
    total_runtime_ms = int((now - started) * 1000)
    row = {
        "ts_utc": _utc_now_iso(),
        "date": _today_date(),
        "session_id": session_id,
        "pages_visited": ",".join(pages),
        "event_count": int(state.get("telemetry_event_count", 0)),
        "error_count": int(state.get("telemetry_error_count", 0)),
        "total_runtime_ms": total_runtime_ms,
        "app_version": config.app_version,
        "last_page": state.get("telemetry_last_page", ""),
    }
    try:
        import pandas as pd

        df = pd.DataFrame([row])
        paths = _get_paths(config)
        path = paths["sessions"]
        try:
            import duckdb

            duckdb.from_df(df).write_parquet(
                str(path),
                compression="zstd",
                append=path.exists(),
            )
        except Exception:
            df.to_parquet(path, index=False)
    except Exception as exc:
        print(f"Telemetry session snapshot failed: {exc}")
    state["telemetry_last_session_flush"] = time.time()


def ensure_session_started(page: str) -> None:
    config = get_config()
    if not config.enabled:
        return
    state = _get_state()
    _ensure_session_id()
    if "telemetry_started" not in state:
        state["telemetry_started"] = True
        state["telemetry_started_ts"] = time.time()
        state["telemetry_pages"] = set()
        state["telemetry_event_count"] = 0
        state["telemetry_error_count"] = 0
        event = {
            "ts_utc": _utc_now_iso(),
            "session_id": _ensure_session_id(),
            "page": page,
            "event_type": "session_start",
            "duration_ms": None,
            "payload": {},
            "app_version": config.app_version,
        }
        _buffer_event(config, event)


def log_event(
    event_type: str,
    page: str,
    payload: dict | None = None,
    duration_ms: int | None = None,
) -> None:
    config = get_config()
    if not config.enabled:
        return
    try:
        ensure_session_started(page)
        event = {
            "ts_utc": _utc_now_iso(),
            "session_id": _ensure_session_id(),
            "page": page,
            "event_type": event_type,
            "duration_ms": duration_ms,
            "payload": payload or {},
            "app_version": config.app_version,
        }
        _buffer_event(config, event)
    except Exception as exc:
        print(f"Telemetry log_event failed: {exc}")


def log_page_view(page: str) -> None:
    log_event("page_view", page, payload={})


def log_error(page: str, exc: BaseException) -> None:
    config = get_config()
    if not config.enabled:
        return
    try:
        stack = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        log_event(
            "error",
            page,
            payload={
                "error": str(exc),
                "traceback": stack,
            },
        )
        paths = _get_paths(config)
        _append_jsonl(paths["errors"], [_json_dumps({"ts_utc": _utc_now_iso(), "error": stack})])
    except Exception as err:
        print(f"Telemetry log_error failed: {err}")


@contextmanager
def track_timing(page: str, payload: dict | None = None):
    start = time.time()
    try:
        yield
    finally:
        duration_ms = int((time.time() - start) * 1000)
        log_event("pipeline_run", page, payload=payload or {}, duration_ms=duration_ms)


def install_excepthook(page: str) -> None:
    config = get_config()
    if not config.enabled:
        return
    state = _get_state()
    if state.get("telemetry_excepthook_installed"):
        return

    def _hook(exc_type, exc, tb):
        try:
            stack = "".join(traceback.format_exception(exc_type, exc, tb))
            log_event(
                "error",
                page,
                payload={
                    "error": str(exc),
                    "traceback": stack,
                },
            )
        except Exception as err:
            print(f"Telemetry excepthook failed: {err}")
        return sys.__excepthook__(exc_type, exc, tb)

    sys.excepthook = _hook
    state["telemetry_excepthook_installed"] = True


def instrument_page(page: str) -> None:
    ensure_session_started(page)
    install_excepthook(page)
    log_page_view(page)
