from pathlib import Path

from agentos.event_log import EventLog


def test_event_log_persists_checkpoints_and_freeze_state(tmp_path: Path) -> None:
    db_path = tmp_path / "agentos.sqlite"
    log = EventLog(db_path)
    log.initialize()

    log.save_checkpoint("racing", "PLAN", {"task": "choose next move"})
    checkpoint = log.latest_checkpoint("racing")

    assert checkpoint is not None
    assert checkpoint.mode == "PLAN"
    assert checkpoint.data["task"] == "choose next move"

    log.set_freeze("racing", True)
    assert log.is_frozen("racing") is True

    log.set_freeze("racing", False)
    assert log.is_frozen("racing") is False

