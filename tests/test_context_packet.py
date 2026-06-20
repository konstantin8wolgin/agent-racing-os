from pathlib import Path

from agentos.context_packet import build_context_packet


def test_context_packet_contains_alignment_and_domain_context(tmp_path: Path) -> None:
    (tmp_path / "GOAL.md").write_text("# Goal\nBuild the game.\n", encoding="utf-8")
    (tmp_path / "ROADMAP.md").write_text("# Roadmap\nM0 - Agent OS Boots\n", encoding="utf-8")
    (tmp_path / "STATE.md").write_text("# State\n## Active Milestone\nM0\n", encoding="utf-8")
    (tmp_path / "AGENT_PROTOCOL.md").write_text("# Agent Protocol\nWorkers create evidence.\n", encoding="utf-8")
    domain_dir = tmp_path / "domains" / "agent_os"
    domain_dir.mkdir(parents=True)
    (domain_dir / "DOMAIN.md").write_text("# Agent OS Domain\nKeep loop aligned.\n", encoding="utf-8")
    (domain_dir / "EXPERIMENTS.md").write_text("# Agent OS Experiments\nNone.\n", encoding="utf-8")

    packet = build_context_packet(tmp_path, "agent_os", "Run one safe cycle")

    assert packet.domain == "agent_os"
    assert packet.task == "Run one safe cycle"
    assert "Build the game" in packet.render()
    assert "Keep loop aligned" in packet.render()
    assert "Workers create evidence" in packet.render()

