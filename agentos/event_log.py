from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Checkpoint:
    id: int
    project: str
    mode: str
    data: dict[str, Any]
    created_at: str


class EventLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(
                """
                create table if not exists runs (
                    id integer primary key autoincrement,
                    project text not null,
                    mode text not null,
                    summary text not null default '',
                    created_at text not null default current_timestamp
                );
                create table if not exists tasks (
                    id integer primary key autoincrement,
                    run_id integer,
                    project text not null,
                    domain text not null,
                    task text not null,
                    status text not null,
                    branch text,
                    created_at text not null default current_timestamp
                );
                create table if not exists agent_calls (
                    id integer primary key autoincrement,
                    run_id integer,
                    role text not null,
                    prompt_path text,
                    context text not null,
                    output text not null,
                    created_at text not null default current_timestamp
                );
                create table if not exists artifacts (
                    id integer primary key autoincrement,
                    run_id integer,
                    kind text not null,
                    path text not null,
                    description text not null default '',
                    created_at text not null default current_timestamp
                );
                create table if not exists decisions (
                    id integer primary key autoincrement,
                    run_id integer,
                    decision text not null,
                    reasoning text not null,
                    created_at text not null default current_timestamp
                );
                create table if not exists state_updates (
                    id integer primary key autoincrement,
                    run_id integer,
                    path text not null,
                    summary text not null,
                    created_at text not null default current_timestamp
                );
                create table if not exists prs (
                    id integer primary key autoincrement,
                    run_id integer,
                    branch text not null,
                    url text,
                    status text not null,
                    merge_decision text,
                    created_at text not null default current_timestamp
                );
                create table if not exists checkpoints (
                    id integer primary key autoincrement,
                    project text not null,
                    mode text not null,
                    data text not null,
                    created_at text not null default current_timestamp
                );
                create table if not exists settings (
                    key text primary key,
                    value text not null
                );
                """
            )

    def create_run(self, project: str, mode: str, summary: str = "") -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "insert into runs (project, mode, summary) values (?, ?, ?)",
                (project, mode, summary),
            )
            return int(cur.lastrowid)

    def record_task(self, run_id: int, project: str, domain: str, task: str, status: str, branch: str | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into tasks (run_id, project, domain, task, status, branch) values (?, ?, ?, ?, ?, ?)",
                (run_id, project, domain, task, status, branch),
            )

    def record_agent_call(self, run_id: int, role: str, prompt_path: str, context: str, output: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into agent_calls (run_id, role, prompt_path, context, output) values (?, ?, ?, ?, ?)",
                (run_id, role, prompt_path, context, output),
            )

    def record_decision(self, run_id: int, decision: str, reasoning: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into decisions (run_id, decision, reasoning) values (?, ?, ?)",
                (run_id, decision, reasoning),
            )

    def record_state_update(self, run_id: int, path: Path, summary: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into state_updates (run_id, path, summary) values (?, ?, ?)",
                (run_id, str(path), summary),
            )

    def save_checkpoint(self, project: str, mode: str, data: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into checkpoints (project, mode, data) values (?, ?, ?)",
                (project, mode, json.dumps(data, sort_keys=True)),
            )

    def latest_checkpoint(self, project: str) -> Checkpoint | None:
        with self._connect() as conn:
            row = conn.execute(
                "select id, project, mode, data, created_at from checkpoints where project = ? order by id desc limit 1",
                (project,),
            ).fetchone()
        if row is None:
            return None
        return Checkpoint(
            id=int(row["id"]),
            project=str(row["project"]),
            mode=str(row["mode"]),
            data=json.loads(str(row["data"])),
            created_at=str(row["created_at"]),
        )

    def set_freeze(self, project: str, frozen: bool) -> None:
        key = f"freeze:{project}"
        value = "true" if frozen else "false"
        with self._connect() as conn:
            conn.execute(
                "insert into settings (key, value) values (?, ?) on conflict(key) do update set value = excluded.value",
                (key, value),
            )

    def is_frozen(self, project: str) -> bool:
        key = f"freeze:{project}"
        with self._connect() as conn:
            row = conn.execute("select value from settings where key = ?", (key,)).fetchone()
        return bool(row and row["value"] == "true")

    def latest_runs(self, limit: int = 5) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "select id, project, mode, summary, created_at from runs order by id desc limit ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

