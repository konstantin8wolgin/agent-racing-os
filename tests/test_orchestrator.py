from pathlib import Path

from agentos.event_log import EventLog
from agentos.orchestrator import Orchestrator


def write_repo_spine(repo: Path) -> None:
    (repo / "GOAL.md").write_text("# Goal\nBuild a playable UE5 driving game.\n", encoding="utf-8")
    (repo / "ROADMAP.md").write_text("# Roadmap\n## M0 - Agent OS Boots\n", encoding="utf-8")
    (repo / "STATE.md").write_text(
        "# State\n\n"
        "## Active Milestone\nM0 - Agent OS Boots\n\n"
        "## Active Domain\nagent_os\n\n"
        "## Next Intended Move\nRun the first orchestrator cycle.\n",
        encoding="utf-8",
    )
    (repo / "AGENT_PROTOCOL.md").write_text("# Agent Protocol\nThe orchestrator decides.\n", encoding="utf-8")
    domain_dir = repo / "domains" / "agent_os"
    domain_dir.mkdir(parents=True)
    (domain_dir / "DOMAIN.md").write_text("# Agent OS Domain\nKeep the loop aligned.\n", encoding="utf-8")
    (domain_dir / "EXPERIMENTS.md").write_text("# Agent OS Experiments\n", encoding="utf-8")
    (repo / "runs").mkdir()


def test_orchestrator_run_once_records_summary_and_updates_state(tmp_path: Path) -> None:
    write_repo_spine(tmp_path)
    db_path = tmp_path / "data.sqlite"
    EventLog(db_path).initialize()

    result = Orchestrator(tmp_path, db_path).run_once(project="racing")

    assert result.mode == "REFLECT"
    assert result.run_id > 0
    assert result.summary_path.exists()
    assert "Run the first orchestrator cycle" in result.summary_path.read_text(encoding="utf-8")
    state = (tmp_path / "STATE.md").read_text(encoding="utf-8")
    assert "\n\n## Last Result\n" in state
    assert "Review runs/run-" in state
    assert str(tmp_path) not in state
    experiments = (tmp_path / "domains" / "agent_os" / "EXPERIMENTS.md").read_text(encoding="utf-8")
    assert "runs/run-" in experiments
    assert str(tmp_path) not in experiments
