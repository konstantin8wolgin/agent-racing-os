# Agent Racing OS Design

## Summary

Agent Racing OS is a GitHub-ready autonomous project repo for building a smoothly playable, realistic, exciting car-only Gaussian-splat driving game. Python is used only for the VPS orchestration layer. The game target is Unreal Engine 5 with C++/Blueprint/plugins as needed.

The system uses one strategic orchestrator, persistent public domain memory, fresh tactical workers, fresh reviewers, compact context packets, an append-only event log, and GitHub-visible state.

## Architecture

- The orchestrator owns strategy and updates durable state.
- Domain cells are folders with `DOMAIN.md` and `EXPERIMENTS.md`; they preserve public experience without permanent private chat agents.
- Workers execute one precise task in fresh context and return evidence.
- Reviewers inspect worker output, goal alignment, foundation quality, and risks.
- Memory compactors turn raw logs into compact domain lessons.
- The event log stores raw history, but agents receive small context packets by default.

## Operating Loop

The orchestrator cycles through `PLAN -> BUILD -> REVIEW -> DECIDE -> MERGE -> REFLECT`. It can enter `STUCK` for diagnosis or `FROZEN` for exact pause/resume.

V1 starts with one active strategic task plus one reviewer or research task. Parallelism scales only after memory quality, reviewer discipline, state coherence, and branch/PR quality remain healthy.

## Alignment

The repo has a compact alignment spine:

- `GOAL.md`: north-star target, human-approved changes only.
- `ROADMAP.md`: playable milestone ladder.
- `STATE.md`: current truth, active milestone/domain, blocker, next move.
- `AGENT_PROTOCOL.md`: role contracts and operating policies.

Strategic progress means improving the playable game, removing its biggest blocker, reducing important uncertainty, strengthening weak foundations, or simplifying future work.

## VPS Workflow

A VPS clone should support:

```bash
./ops/vps_bootstrap.sh
agentos start project racing
```

The daemon should run continuously under systemd, recover from restart, checkpoint state, push visible progress to GitHub when configured, and freeze/resume exactly.

