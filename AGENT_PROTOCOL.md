# Agent Protocol

## Core Rule

Workers and reviewers produce evidence. The orchestrator decides.

The system exists to improve the playable game or remove blockers to improving it.

## Orchestrator

The orchestrator:

- reads `GOAL.md`, `ROADMAP.md`, `STATE.md`, relevant domain files, and recent run summaries
- chooses one main task per cycle
- creates compact context packets
- spawns workers and reviewers
- decides whether to accept, retry, revise, mark stuck, or schedule foundation work
- updates `STATE.md` and domain memory
- manages branches, PRs, auto-merge, freeze, and resume

## Workers

Workers:

- receive one precise task
- work in an isolated branch or worktree
- inspect the context packet and referenced files first
- produce evidence
- suggest next steps
- do not update `STATE.md` directly
- do not change `GOAL.md`

## Reviewers

Reviewers:

- receive fresh context
- inspect worker output, diffs, logs, and artifacts
- judge alignment with `GOAL.md` and the active milestone
- check whether foundation quality was harmed
- produce a foundation report when needed
- suggest memory updates
- do not update `STATE.md` directly

## Domain Memory

Each domain has:

- `DOMAIN.md`
- `EXPERIMENTS.md`

`DOMAIN.md` stores durable lessons, current blockers, and useful next tasks.

`EXPERIMENTS.md` records compact evidence-backed experiment history.

Raw logs are not memory. Durable memory must be compact and evidence-linked.

## Context Packets

Every spawned agent receives:

- north-star goal
- active milestone
- relevant `STATE.md` excerpt
- relevant domain memory excerpt
- exact task
- expected evidence
- files or artifacts to inspect first
- output format

Long history is not included by default.

## Output Contract

Workers return:

- what changed or was learned
- evidence
- what became easier
- what remains blocked
- suggested next task

Reviewers return:

- whether the result aligns with the goal
- evidence for that judgment
- risks or foundation concerns
- suggested memory updates
- recommended orchestrator decision

## Task Selection Policy

Each cycle, the orchestrator chooses one main task.

It prefers tasks that:

1. improve the playable game directly
2. remove the current biggest blocker
3. reduce an important uncertainty
4. strengthen the foundation when weak foundations limit future progress
5. simplify code, architecture, or workflows so future changes become easier
6. improve the agent loop only when the loop blocks game progress

The orchestrator records why the chosen task is higher leverage than the obvious alternatives.

## Foundation Review

Foundation quality matters when it affects future progress.

After meaningful feature work, reviewers may report:

- whether the change made future work harder
- whether the issue is local or architectural
- whether cleanup can happen without removing the feature
- the smallest useful foundation task

Prefer stabilize, simplify, refactor, replace.

## Parallelism

V1 starts conservative:

- one active strategic domain task
- plus one reviewer or research task when useful

Parallelism is for execution, not strategy.

Scale only after domain memory, reviewers, `STATE.md`, branches, and PRs stay coherent.

## Auto-Merge

A PR may auto-merge when:

- it serves `GOAL.md`, `ROADMAP.md`, or `STATE.md`
- worker and reviewer outputs agree it is aligned
- required checks pass
- the orchestrator records why merging is better than waiting
- it does not change `GOAL.md`

## Freeze and Resume

When frozen:

- no new workers are spawned
- no PRs are merged
- current mode, task, branch, run id, and pending decisions are checkpointed

When resumed:

- reload checkpoint
- check whether repo or GitHub state changed
- continue or re-plan from the saved state

## Stuck Recovery

When repeated runs produce no new evidence, the orchestrator switches to diagnosis.

Prefer:

1. smaller experiment
2. fresh reviewer audit
3. research task
4. simpler implementation path
5. domain switch if another domain blocks progress

Every stuck recovery records what should not be retried unchanged.

