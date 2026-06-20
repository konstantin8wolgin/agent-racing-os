from __future__ import annotations

import argparse
from pathlib import Path

from agentos.config import load_config
from agentos.daemon import run_daemon
from agentos.event_log import EventLog
from agentos.gitops import current_branch, has_remote
from agentos.orchestrator import Orchestrator
from agentos.state_machine import Mode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentos")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("kind", choices=["project"])
    start.add_argument("name")
    start.add_argument("--once", action="store_true")

    daemon = sub.add_parser("daemon")
    daemon.add_argument("--project", default="racing")
    daemon.add_argument("--interval", type=int, default=300)
    daemon.add_argument("--once", action="store_true")

    sub.add_parser("status")
    sub.add_parser("freeze")
    sub.add_parser("resume")
    sub.add_parser("stop")
    sub.add_parser("logs")

    args = parser.parse_args(argv)
    project = getattr(args, "name", None) or getattr(args, "project", "racing")
    config = load_config(Path.cwd(), project)
    log = EventLog(config.db_path)
    log.initialize()

    if args.command == "start":
        log.save_checkpoint(project, Mode.PLAN, {"project": project, "command": "start"})
        print(f"Starting project {project} in {config.repo}")
        print(f"Database: {config.db_path}")
        print("Python is orchestration only; game target is UE5.")
        if args.once:
            result = Orchestrator(config.repo, config.db_path).run_once(project=project)
            print(f"Completed one cycle: run {result.run_id}, mode {result.mode}, summary {result.summary_path}")
        else:
            print("Use systemd or `agentos daemon --project racing` for continuous 24/7 operation.")
        return 0

    if args.command == "daemon":
        run_daemon(config.repo, config.db_path, project, interval_seconds=args.interval, once=args.once)
        return 0

    if args.command == "status":
        checkpoint = log.latest_checkpoint(project)
        frozen = log.is_frozen(project)
        print(f"Project: {project}")
        print(f"Repo: {config.repo}")
        print(f"Branch: {current_branch(config.repo)}")
        print(f"Remote origin configured: {has_remote(config.repo)}")
        print(f"Frozen: {frozen}")
        if checkpoint:
            print(f"Last checkpoint: {checkpoint.mode} at {checkpoint.created_at}")
        else:
            print("Last checkpoint: none")
        return 0

    if args.command == "freeze":
        log.set_freeze(project, True)
        log.save_checkpoint(project, Mode.FROZEN, {"command": "freeze"})
        print(f"Frozen project {project}. No new autonomous work should start.")
        return 0

    if args.command == "resume":
        log.set_freeze(project, False)
        log.save_checkpoint(project, Mode.PLAN, {"command": "resume"})
        print(f"Resumed project {project}.")
        return 0

    if args.command == "stop":
        log.set_freeze(project, True)
        log.save_checkpoint(project, Mode.FROZEN, {"command": "stop"})
        print(f"Stopped project {project} by freezing it.")
        return 0

    if args.command == "logs":
        for row in log.latest_runs():
            print(f"run {row['id']} [{row['mode']}] {row['created_at']}: {row['summary']}")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

