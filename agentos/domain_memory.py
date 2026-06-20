from __future__ import annotations

import re
from pathlib import Path


def active_domain_from_state(state_text: str, default: str = "agent_os") -> str:
    match = re.search(r"## Active Domain\s+([a-zA-Z0-9_\-]+)", state_text)
    if match:
        return match.group(1).strip()
    return default


def next_move_from_state(state_text: str, default: str = "Run one orchestrator cycle.") -> str:
    match = re.search(r"## Next Intended Move\s+(.+?)(?:\n## |\Z)", state_text, flags=re.S)
    if match:
        value = match.group(1).strip()
        if value:
            return value
    return default


def append_experiment(repo: Path, domain: str, run_id: int, title: str, result: str, evidence: Path) -> None:
    path = repo / "domains" / domain / "EXPERIMENTS.md"
    existing = path.read_text(encoding="utf-8")
    try:
        evidence_ref = evidence.relative_to(repo).as_posix()
    except ValueError:
        evidence_ref = evidence.as_posix()
    entry = (
        f"\n\n## Run {run_id} - {title}\n\n"
        f"Goal:\n{title}\n\n"
        f"Result:\n{result}\n\n"
        f"Evidence:\n{evidence_ref}\n\n"
        "Consequence:\nUse this run as evidence for the next orchestrator decision.\n"
    )
    path.write_text(existing.rstrip() + entry + "\n", encoding="utf-8")
