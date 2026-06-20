from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentos.context_packet import build_context_packet
from agentos.domain_memory import active_domain_from_state, append_experiment, next_move_from_state
from agentos.event_log import EventLog
from agentos.reviewer_runner import LocalReviewerRunner
from agentos.state_machine import Mode
from agentos.worker_runner import LocalWorkerRunner


@dataclass(frozen=True)
class OrchestratorResult:
    run_id: int
    mode: str
    summary_path: Path


class Orchestrator:
    def __init__(self, repo: Path, db_path: Path) -> None:
        self.repo = repo
        self.db_path = db_path
        self.log = EventLog(db_path)

    def run_once(self, project: str = "racing") -> OrchestratorResult:
        self.log.initialize()
        if self.log.is_frozen(project):
            self.log.save_checkpoint(project, Mode.FROZEN, {"reason": "project is frozen"})
            run_id = self.log.create_run(project, Mode.FROZEN, "Project is frozen; no worker spawned.")
            summary_path = self._write_run_summary(run_id, "Project is frozen; no worker spawned.")
            return OrchestratorResult(run_id=run_id, mode=Mode.FROZEN, summary_path=summary_path)

        state_text = (self.repo / "STATE.md").read_text(encoding="utf-8")
        domain = active_domain_from_state(state_text)
        task = next_move_from_state(state_text)
        packet = build_context_packet(self.repo, domain, task)

        run_id = self.log.create_run(project, Mode.PLAN, f"Selected task for {domain}: {task}")
        self.log.record_task(run_id, project, domain, task, "selected")
        self.log.save_checkpoint(project, Mode.PLAN, {"run_id": run_id, "domain": domain, "task": task})

        worker_output = LocalWorkerRunner().run(packet)
        self.log.record_agent_call(run_id, "worker", "prompts/worker.md", packet.render(), worker_output.render())
        self.log.save_checkpoint(project, Mode.BUILD, {"run_id": run_id, "domain": domain, "task": task})

        reviewer_output = LocalReviewerRunner().review(packet, worker_output)
        self.log.record_agent_call(run_id, "reviewer", "prompts/reviewer.md", packet.render(), reviewer_output.render())
        self.log.save_checkpoint(project, Mode.REVIEW, {"run_id": run_id, "domain": domain, "task": task})

        decision = "accept" if reviewer_output.aligned else "revise"
        self.log.record_decision(run_id, decision, reviewer_output.recommendation)
        self.log.save_checkpoint(project, Mode.DECIDE, {"run_id": run_id, "decision": decision})

        summary = self._render_summary(run_id, domain, task, worker_output.render(), reviewer_output.render(), decision)
        summary_path = self._write_run_summary(run_id, summary)
        append_experiment(self.repo, domain, run_id, task, decision, summary_path)
        self._update_state(run_id, domain, task, decision, summary_path)

        self.log.record_state_update(run_id, self.repo / "STATE.md", "Recorded latest orchestrator result.")
        self.log.save_checkpoint(project, Mode.REFLECT, {"run_id": run_id, "summary": str(summary_path)})
        return OrchestratorResult(run_id=run_id, mode=Mode.REFLECT, summary_path=summary_path)

    def _render_summary(self, run_id: int, domain: str, task: str, worker: str, reviewer: str, decision: str) -> str:
        return (
            f"# Run {run_id} Summary\n\n"
            f"Domain: {domain}\n\n"
            f"Task:\n{task}\n\n"
            f"Worker Output:\n{worker}\n\n"
            f"Reviewer Output:\n{reviewer}\n\n"
            f"Orchestrator Decision:\n{decision}\n"
        )

    def _write_run_summary(self, run_id: int, summary: str) -> Path:
        runs_dir = self.repo / "runs"
        runs_dir.mkdir(exist_ok=True)
        path = runs_dir / f"run-{run_id:04d}.md"
        path.write_text(summary, encoding="utf-8")
        return path

    def _update_state(self, run_id: int, domain: str, task: str, decision: str, summary_path: Path) -> None:
        path = self.repo / "STATE.md"
        state = path.read_text(encoding="utf-8").rstrip()
        try:
            display_summary = summary_path.relative_to(self.repo).as_posix()
        except ValueError:
            display_summary = summary_path.as_posix()
        replacement = (
            "## Last Result\n\n"
            f"Run {run_id} in `{domain}` decided `{decision}` for task: {task}\n\n"
            "## Next Intended Move\n\n"
            "Wire the configured external worker backend after the local loop remains stable.\n\n"
            "## Open Questions\n\n"
            f"Review {display_summary} before scaling parallel work.\n"
        )
        marker = "\n## Last Result\n"
        if marker in state:
            before = state.split(marker, 1)[0]
            path.write_text(before.rstrip() + "\n\n" + replacement, encoding="utf-8")
        else:
            path.write_text(state + "\n\n" + replacement, encoding="utf-8")
