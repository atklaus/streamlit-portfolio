import os
from pathlib import Path

import pandas as pd
import streamlit as st

from app.layout.header import page_header
from shared.logging import get_config

page_header("Telemetry Admin", page_name=os.path.basename(__file__))

st.markdown("## Telemetry Overview")
config = get_config()
log_dir = config.log_dir

st.caption(f"Log dir: {log_dir}")

events_glob = str(log_dir / "events" / "date=*" / "events.jsonl")
sessions_glob = str(log_dir / "sessions" / "date=*" / "sessions.parquet")

try:
    import duckdb
except Exception as exc:
    st.error(f"DuckDB not available: {exc}")
    st.stop()

con = duckdb.connect()

has_events = list(Path(log_dir / "events").glob("date=*/events.jsonl"))
has_sessions = list(Path(log_dir / "sessions").glob("date=*/sessions.parquet"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Sessions per day**")
    if has_sessions:
        df_sessions = con.execute(
            """
            SELECT date, COUNT(*) AS sessions
            FROM read_parquet(? )
            GROUP BY date
            ORDER BY date DESC
            """,
            [sessions_glob],
        ).df()
        st.dataframe(df_sessions, use_container_width=True, hide_index=True)
    else:
        st.caption("No session snapshots yet.")

with col2:
    st.markdown("**Page views per day**")
    if has_events:
        df_views = con.execute(
            """
            SELECT CAST(ts_utc AS DATE) AS day, COUNT(*) AS page_views
            FROM read_json_auto(? )
            WHERE event_type = 'page_view'
            GROUP BY day
            ORDER BY day DESC
            """,
            [events_glob],
        ).df()
        st.dataframe(df_views, use_container_width=True, hide_index=True)
    else:
        st.caption("No events yet.")

with col3:
    st.markdown("**Errors per day**")
    if has_events:
        df_errors = con.execute(
            """
            SELECT CAST(ts_utc AS DATE) AS day, COUNT(*) AS errors
            FROM read_json_auto(? )
            WHERE event_type = 'error'
            GROUP BY day
            ORDER BY day DESC
            """,
            [events_glob],
        ).df()
        st.dataframe(df_errors, use_container_width=True, hide_index=True)
    else:
        st.caption("No errors logged.")

st.markdown("---")
st.markdown("### Recent events")
if has_events:
    df_recent = con.execute(
        """
        SELECT ts_utc, page, event_type, duration_ms
        FROM read_json_auto(? )
        ORDER BY ts_utc DESC
        LIMIT 50
        """,
        [events_glob],
    ).df()
    st.dataframe(df_recent, use_container_width=True, hide_index=True)
else:
    st.caption("No events yet.")
