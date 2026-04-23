# TEAM_MEMORY.md

This file stores durable project memory for the `Permaculture-Agent` repository.

It is not a transcript log. It is a compact memory layer for preserving:
- architectural decisions
- project invariants
- lessons from implementation
- failed experiments
- naming choices
- open questions
- roadmap direction

The goal is to reduce repeated confusion and allow both humans and agents to build from prior understanding.

---

## Memory Protocol

### What belongs here
Store information that future work is likely to depend on:
- structural design decisions
- core modeling assumptions
- interface contracts
- patterns worth repeating
- mistakes worth avoiding
- unresolved questions that shape future work

### What does not belong here
Do not turn this into a verbose daily log.
Avoid storing:
- trivial edits
- full transcripts
- low-signal status chatter
- repetitive implementation minutiae

### Update rule
Update this file when a change materially affects:
- architecture
- interfaces
- ecological assumptions
- team workflow
- project direction
- terminology

---

## Project Identity
- **Repository:** `Permaculture-Agent`
- **Intent:** build a hybrid-intelligence software project for permaculture and regenerative design work
- **Governance style:** human-steered, agent-assisted, explicit, modular, ethically aware

---

## Current Foundational Decisions

### Decision 001 — Founding root-doc scaffold
**Status:** accepted

The repository begins with four root documents:
- `README.md`
- `AGENT.md`
- `TEAM_MEMORY.md`
- `ARCHITECTURE.md`

**Rationale**
This gives the project a foundational cognition scaffold:
- README = orientation
- AGENT = behavior contract
- TEAM_MEMORY = durable memory
- ARCHITECTURE = system structure

**Implication**
Future repo growth should stay aligned with these documents unless intentionally revised.

---

### Decision 002 — Human cognition is first-class
**Status:** accepted

The project formally treats human judgment as a core subsystem rather than a final approval gate.

**Rationale**
Permaculture work depends on:
- field realism
- stakeholder values
- real-world constraints
- ethical and strategic judgment

These are not fully reducible to automated optimization.

---

### Decision 003 — Modular architecture over monolith by default
**Status:** accepted

This repository should evolve as a modular system rather than a single unstructured file when implementation begins.

**Rationale**
The repo is intended to support hybrid intelligence, ecological modeling, and likely multiple workflows.
A modular structure will improve maintainability and agent effectiveness.

**Constraint**
Avoid overengineering. Modularity should remain practical.

---

### Decision 004 — Tensor layer adopted as optional adaptive behavior substrate
**Status:** accepted

The repository may use a mutable cognitive tensor layer to shape checklist prioritization, reasoning tendencies, and save-state inheritance across agent runs.

**Artifacts**
- `docs/AGENT_EVOLUTION_WEIGHTS.md`
- `schemas/agent_tensor_state.schema.json`
- `examples/agent_tensor_state.example.json`
- `state/active_agent_tensor_state.json`
- `scripts/evolve_agent_state.py`

**Rationale**
This enables adaptive yet structured evolution of agent behavior while preserving a human-aligned ethical floor.

**Current policy**
- default mutation policy: `bounded_gaussian`
- default range: `[0.0, 1.0]`
- protected minimum columns:
  - `HumanAlignment`
  - `Truthfulness`
  - `Accountability`
  - `LoveAsOrientation`

---

## Current Invariants
- The project should preserve human agency.
- Important decisions should be explainable.
- Ecological features should remain grounded in real-world logic where possible.
- Architecture should be understandable by future contributors.
- Documentation is part of the system, not an afterthought.
- The cognitive tensor layer may evolve, but it must not silently erode the ethical floor without explicit human direction.

---

## Known Unknowns
These are questions not yet resolved.

### Product scope
- Is `Permaculture-Agent` primarily:
  - a coding-agent repo,
  - a planning engine,
  - a simulation framework,
  - a design assistant,
  - or a unified platform?

### Runtime stack
- What is the intended initial stack?
  - TypeScript / Node?
  - Python?
  - HTML-first local tools?
  - Hybrid frontend + backend?

### Primary interface
- CLI?
- web app?
- local-first desktop workflow?
- Cursor-oriented internal toolkit?

### Data model
- What are the core entities?
  - sites
  - zones
  - sectors
  - species
  - guilds
  - interventions
  - tasks
  - observations
  - maps
  - simulations

### External integrations
- GIS data?
- Google Earth / KML?
- drone imagery?
- spreadsheets?
- JSON scenario files?

---

## Initial Architecture Hints
Until the repo is further defined, future contributors should assume a likely module family such as:
- `core/` for domain models and reasoning kernels
- `agents/` for agent logic and orchestration
- `sim/` for simulations and temporal/ecological models
- `data/` for schemas and import/export
- `ui/` for human-facing interfaces
- `docs/` for durable project documentation

This is directional guidance, not yet a hard contract.

---

## Open Research / Design Questions
- How should ecological uncertainty be represented?
- How should the agent distinguish measured data from inferred data?
- What makes a useful minimum viable permaculture agent?
- Which tasks are best handled by humans, and which by software?
- How much simulation fidelity is actually valuable to end users?

---

## Future Update Template
Use this structure for meaningful additions:

```md
### Decision NNN — Short title
**Status:** proposed | accepted | revised | deprecated

**Context**
Why this decision mattered.

**Decision**
What was chosen.

**Rationale**
Why it was chosen.

**Implications**
What future contributors should assume.
```
