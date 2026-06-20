# Agent Racing OS

Agent Racing OS is the VPS orchestration repo for building a smoothly playable, realistic, exciting car-only driving game in a Gaussian-splat city world.

Python is only the orchestration layer. The game itself targets Unreal Engine 5 with C++/Blueprints/plugins as needed.

## VPS Quick Start

```bash
git clone <repo-url> agent-racing-os
cd agent-racing-os
./ops/vps_bootstrap.sh
agentos start project racing
```

After startup, the daemon can run under systemd:

```bash
systemctl --user start agent-racing-os
```

## Commands

```bash
agentos start project racing
agentos daemon --project racing
agentos status
agentos freeze
agentos resume
agentos stop
agentos logs
```

## Operating Model

The repo is the source of truth:

- `GOAL.md` defines the north star.
- `ROADMAP.md` defines the playable milestone ladder.
- `STATE.md` defines the current strategic truth.
- `AGENT_PROTOCOL.md` defines how autonomous agents work.
- `domains/*/DOMAIN.md` and `domains/*/EXPERIMENTS.md` preserve public domain memory.

The orchestrator chooses one strategic direction at a time. Fresh workers execute bounded tasks. Fresh reviewers evaluate results. Durable learning is promoted into state and domain memory.

## Local Development

Global pytest plugins can interfere with this workspace, so run tests with plugin autoload disabled:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
```

