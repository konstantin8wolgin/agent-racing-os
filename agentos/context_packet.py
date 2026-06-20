from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ContextPacket:
    domain: str
    task: str
    goal: str
    roadmap: str
    state: str
    protocol: str
    domain_memory: str
    domain_experiments: str

    def render(self) -> str:
        return "\n\n".join(
            [
                "# Context Packet",
                f"## Domain\n{self.domain}",
                f"## Task\n{self.task}",
                f"## Goal\n{self.goal}",
                f"## Roadmap\n{self.roadmap}",
                f"## State\n{self.state}",
                f"## Protocol\n{self.protocol}",
                f"## Domain Memory\n{self.domain_memory}",
                f"## Domain Experiments\n{self.domain_experiments}",
            ]
        )


def _read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required context file is missing: {path}")
    return path.read_text(encoding="utf-8")


def build_context_packet(repo: Path, domain: str, task: str) -> ContextPacket:
    domain_path = repo / "domains" / domain
    return ContextPacket(
        domain=domain,
        task=task,
        goal=_read_required(repo / "GOAL.md"),
        roadmap=_read_required(repo / "ROADMAP.md"),
        state=_read_required(repo / "STATE.md"),
        protocol=_read_required(repo / "AGENT_PROTOCOL.md"),
        domain_memory=_read_required(domain_path / "DOMAIN.md"),
        domain_experiments=_read_required(domain_path / "EXPERIMENTS.md"),
    )

