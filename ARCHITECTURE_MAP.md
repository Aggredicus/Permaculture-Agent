# ARCHITECTURE_MAP.md

## Purpose
This file is a compact navigation map for `Permaculture-Agent`.

Use it to answer one question quickly:
**If I need to make a change, where do I look first?**

Do not treat this file as a replacement for `ARCHITECTURE.md`.
It exists to reduce search cost and keep agent context small.

---

## Current Repo State
- The repository is still a greenfield project.
- The root docs currently act as the main control plane.
- Implementation modules are not yet established.
- Additions should stay proportional to proven workflow value.
- Do not assume unresolved decisions have already been made.

---

## Canonical Files

| File | Primary job |
|---|---|
| `README.md` | Orientation, purpose, current direction |
| `AGENT.md` | Behavior contract for AI contributors |
| `TEAM_MEMORY.md` | Durable decisions, invariants, open questions |
| `ARCHITECTURE.md` | Long-term structural intent |
| `docs/ARCHITECTURE_MAP.md` | Fast navigation and task-to-file routing |

---

## Task-to-File Routing

### Start here by task type
- **What is this repo trying to do?** → `README.md`
- **How should the agent behave?** → `AGENT.md`
- **What has already been decided?** → `TEAM_MEMORY.md`
- **What system shape are we aiming for?** → `ARCHITECTURE.md`
- **Where should I look first?** → `docs/ARCHITECTURE_MAP.md`

### When making changes
- **Mission / scope / product questions** → `README.md`, then `TEAM_MEMORY.md`
- **Agent workflow or contributor behavior** → `AGENT.md`
- **Architecture or module boundary changes** → `ARCHITECTURE.md`, then `TEAM_MEMORY.md`
- **New durable decision** → update `TEAM_MEMORY.md`
- **Implementation work** → read only the smallest affected module(s) plus the minimum root-doc context needed

---

## Context Loading Rules
- Start with only **1–2 files**, not the whole repo.
- Do **not** read all root docs by default.
- Read `TEAM_MEMORY.md` only when prior decisions matter.
- Read `ARCHITECTURE.md` only when structure or boundaries matter.
- Prefer the smallest relevant file set for implementation work.
- If a task changes architecture, interfaces, assumptions, or workflow, record it in `TEAM_MEMORY.md`.
- If a task is local and reversible, avoid expanding scope.

---

## Current Unresolved Anchors
These are not yet fixed and must not be treated as settled facts:
- first concrete workflow
- initial runtime stack
- canonical core entities
- primary interface shape
- external integration priorities

---

## Future Expansion Rule
Only expand this map when the repo gains real modules or folders that agents need help navigating.

When that happens, add brief entries such as:
- `core/` — domain logic
- `agents/` — orchestration logic
- `data/` — schemas and import/export
- `sim/` — simulation logic
- `ui/` — human-facing interfaces

Until then, keep this file short.
