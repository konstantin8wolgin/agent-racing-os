from __future__ import annotations

from dataclasses import dataclass

from agentos.context_packet import ContextPacket
from agentos.worker_runner import WorkerOutput


@dataclass(frozen=True)
class ReviewerOutput:
    aligned: bool
    summary: str
    risks: str
    recommendation: str

    def render(self) -> str:
        return (
            f"Aligned: {self.aligned}\n\n"
            f"Summary:\n{self.summary}\n\n"
            f"Risks:\n{self.risks}\n\n"
            f"Recommendation:\n{self.recommendation}\n"
        )


class LocalReviewerRunner:
    def review(self, packet: ContextPacket, worker_output: WorkerOutput) -> ReviewerOutput:
        return ReviewerOutput(
            aligned=True,
            summary=f"The worker result is aligned with the active task: {packet.task}",
            risks="This is a local deterministic reviewer; external model review is a later adapter.",
            recommendation="Accept the result, record evidence, and continue improving the worker backend.",
        )

