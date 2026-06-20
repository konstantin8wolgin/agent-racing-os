from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    repo: Path
    db_path: Path
    project: str
    automerge: bool


def load_config(repo: Path | None = None, project: str = "racing") -> Config:
    root = repo or Path(os.environ.get("AGENTOS_WORKDIR", ".")).resolve()
    db_path = Path(os.environ.get("AGENTOS_DB", root / "data" / "agentos.sqlite")).resolve()
    automerge = os.environ.get("AGENTOS_AUTOMERGE", "true").lower() == "true"
    return Config(repo=root, db_path=db_path, project=project, automerge=automerge)

