from __future__ import annotations

from dataclasses import dataclass

from agentos.context_packet import ContextPacket


@dataclass(frozen=True)
class WorkerOutput:
    summary: str
    evidence: str
    blocked: str
    suggested_next_task: str

    def render(self) -> str:
        return (
            f"Summary:\n{self.summary}\n\n"
            f"Evidence:\n{self.evidence}\n\n"
            f"Blocked:\n{self.blocked}\n\n"
            f"Suggested next task:\n{self.suggested_next_task}\n"
        )


class LocalWorkerRunner:
    def run(self, packet: ContextPacket) -> WorkerOutput:
        return WorkerOutput(
            summary=f"Prepared and validated a local execution plan for task: {packet.task}",
            evidence="Context packet assembled from GOAL, ROADMAP, STATE, AGENT_PROTOCOL, and domain memory.",
            blocked="External Codex/GitHub worker execution is not wired in this local V1 runner.",
            suggested_next_task="Wire the configured Codex worker backend after the local loop stays stable.",
        )

