# Agent Racing OS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the initial Agent Racing OS repo skeleton and a minimal Python CLI/daemon that can initialize, checkpoint, freeze/resume, assemble context packets, and run one orchestrator cycle.

**Architecture:** The repo uses Markdown alignment files and domain cells for durable public memory, SQLite for evidence/checkpoints, and a Python CLI for VPS operation. The game is not Python; Python only orchestrates autonomous work around the future UE5 game.

**Tech Stack:** Python 3.11+, SQLite standard library, pytest, argparse, systemd shell scaffolding.

## Global Constraints

- Keep V1 small and operational.
- The game target remains UE5, not Python.
- The orchestrator is the only component that updates durable state.
- Workers and reviewers are fresh-context execution/evaluation roles.
- Domain memory is public Markdown, compact, and evidence-linked.

---

### Task 1: Repo Spine and Domain Files

**Files:**
- Create: `README.md`, `GOAL.md`, `ROADMAP.md`, `STATE.md`, `AGENT_PROTOCOL.md`
- Create: `domains/*/DOMAIN.md`, `domains/*/EXPERIMENTS.md`
- Create: `prompts/*.md`, `game/README.md`

**Interfaces:**
- Produces the repo context consumed by `agentos.context_packet.build_context_packet`.

- [x] **Step 1: Create alignment and domain files**

Use the approved design text from the brainstorming session.

- [x] **Step 2: Review for Python/game ambiguity**

Confirm `README.md` and `GOAL.md` explicitly state Python is only orchestration and the game target is UE5.

### Task 2: Tests First for Core Runtime

**Files:**
- Create: `tests/test_context_packet.py`
- Create: `tests/test_event_log.py`
- Create: `tests/test_orchestrator.py`

**Interfaces:**
- Consumes future APIs:
  - `build_context_packet(repo: Path, domain: str, task: str) -> ContextPacket`
  - `EventLog(path: Path).initialize()`
  - `EventLog.save_checkpoint(project, mode, data)`
  - `Orchestrator(repo: Path, db_path: Path).run_once()`

- [x] **Step 1: Write failing tests**

Tests assert context packet contents, checkpoint persistence, freeze/resume status, and one orchestrator cycle summary.

- [x] **Step 2: Run tests and verify they fail**

Run: `pytest -q`

Expected: import failures because production code does not exist yet.

### Task 3: Minimal Python Runtime

**Files:**
- Create: `pyproject.toml`
- Create: `agentos/__init__.py`, `agentos/cli.py`, `agentos/config.py`
- Create: `agentos/context_packet.py`, `agentos/event_log.py`, `agentos/state_machine.py`
- Create: `agentos/orchestrator.py`, `agentos/domain_memory.py`, `agentos/gitops.py`
- Create: `agentos/worker_runner.py`, `agentos/reviewer_runner.py`, `agentos/daemon.py`

**Interfaces:**
- Produces CLI command `agentos`.

- [x] **Step 1: Implement minimal code to pass tests**

Implement only local deterministic behavior. External Codex/GitHub workers are adapter placeholders for later work.

- [x] **Step 2: Run tests**

Run: `pytest -q`

Expected: all tests pass.

### Task 4: VPS Ops Skeleton

**Files:**
- Create: `ops/vps_bootstrap.sh`
- Create: `ops/env.example`
- Create: `ops/systemd/agent-racing-os.service`

**Interfaces:**
- Supports `agentos start project racing`, `agentos status`, `agentos freeze`, `agentos resume`, `agentos daemon --project racing`.

- [x] **Step 1: Add bootstrap and systemd files**

Keep scripts safe and explicit; no secrets are embedded.

- [x] **Step 2: Run CLI smoke checks**

Run: `python -m agentos.cli status`

Expected: a readable status message using local default paths.

