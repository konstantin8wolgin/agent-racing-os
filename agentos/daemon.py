from __future__ import annotations

import time
from pathlib import Path

from agentos.event_log import EventLog
from agentos.orchestrator import Orchestrator


def run_daemon(repo: Path, db_path: Path, project: str, interval_seconds: int = 300, once: bool = False) -> None:
    EventLog(db_path).initialize()
    while True:
        Orchestrator(repo, db_path).run_once(project=project)
        if once:
            return
        time.sleep(interval_seconds)

