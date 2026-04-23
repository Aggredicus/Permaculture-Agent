# ARCHITECTURE.md

## Purpose
This document describes the intended architecture of the `Permaculture-Agent` repository.

Because the repository is new, this file serves as a **founding architecture brief** rather than a description of a fully implemented system.

Its purpose is to:
- define the system shape early
- reduce architectural drift
- align human and agent contributors
- give future implementation work a coherent frame

---

## Architectural Thesis
`Permaculture-Agent` should become a **hybrid-intelligence, modular, human-steered software system** for permaculture and regenerative design.

The system should support some combination of:
- ecological reasoning
- design assistance
- site planning
- data organization
- simulation
- workflow support
- agent orchestration

The exact feature set may evolve, but the architectural principles should remain stable.

---

## Core Principles

### 1. Human-steered hybrid intelligence
The architecture must support both:
- automated cognition
- human judgment and intervention

The human should remain the governing authority for value-laden, strategic, and irreversible decisions.

### 2. Modular over monolithic
As implementation begins, the codebase should favor clear modules with explicit responsibilities.

### 3. Reality-grounded modeling
Ecological and design features should map to real-world concepts where possible:
- sites
- zones
- sectors
- species
- guilds
- water flow
- access
- implementation phases
- observations

### 4. Explainability over opaque automation
Where practical, the system should expose:
- assumptions
- reasoning outputs
- uncertainty
- source of data (measured vs inferred vs user-provided)

### 5. Local usefulness before platform sprawl
The project should be useful in small, concrete workflows before expanding into a broad platform.

---

## Proposed Top-Level System Layers

### Layer 1 — Domain Core
This layer defines the stable concepts of the system.

Likely responsibilities:
- core entities and types
- ecological relationships
- design constraints
- rule evaluation
- shared utility logic

Possible future modules:
- `core/site`
- `core/species`
- `core/guilds`
- `core/zones`
- `core/sectors`
- `core/interventions`

### Layer 2 — Agent Cognition Layer
This layer implements routing, task decomposition, and hybrid intelligence behavior.

Likely responsibilities:
- task classification
- cognition routing
- tool selection
- interaction protocols
- human escalation logic
- memory integration
- adaptive behavior priors through the cognitive tensor layer
- checklist shaping using active tensor state
- save-state inheritance and mutation policies

Possible future modules:
- `agents/router`
- `agents/implementer`
- `agents/verifier`
- `agents/specialists`
- `agents/tensor`

### Layer 3 — Data and Interchange Layer
This layer handles persistence and external data movement.

Likely responsibilities:
- schemas
- import/export
- JSON contracts
- geospatial data ingest
- observations and records
- file format adapters

Possible future modules:
- `data/schemas`
- `data/importers`
- `data/exporters`
- `data/kml`
- `data/csv`
- `data/json`

### Layer 4 — Simulation / Analysis Layer
This layer supports temporal and scenario reasoning.

Likely responsibilities:
- phased implementation models
- ecological change over time
- scenario comparison
- uncertainty-aware outputs
- coarse simulations that support decisions

Possible future modules:
- `sim/water`
- `sim/growth`
- `sim/phasing`
- `sim/maintenance`
- `sim/scenarios`

### Layer 5 — Human Interface Layer
This layer presents outputs and accepts human input.

Likely responsibilities:
- visual design tools
- workflow interfaces
- command-line tools
- dashboards
- review surfaces
- explanation views

Possible future modules:
- `ui/web`
- `ui/components`
- `ui/cli`
- `ui/reports`

### Layer 6 — Documentation / Governance Layer
This layer preserves reasoning continuity.

Likely responsibilities:
- onboarding
- agent contracts
- architectural guidance
- durable team memory
- design records

Current root docs belong to this layer.

---

## Founding Repository Contract
Until the repo matures, contributors should assume the following root contract:

- `README.md` explains what the project is and how to orient
- `AGENT.md` defines the behavior of AI contributors
- `TEAM_MEMORY.md` stores durable project memory
- `ARCHITECTURE.md` defines intended system structure

These files should evolve together.

---

## Suggested Initial Folder Structure
A reasonable first implementation shape could be:

```text
Permaculture-Agent/
├── README.md
├── AGENT.md
├── TEAM_MEMORY.md
├── ARCHITECTURE.md
├── docs/
├── schemas/
├── examples/
├── state/
├── core/
├── scripts/
└── tests/
```

This is a recommendation, not yet a required final form.

---

## Recommended Initial Build Strategy
Because the repo is new, use a staged build strategy.

### Stage 1 — Foundational contracts
- establish root docs
- define product intent
- choose runtime stack
- define core entities
- establish tensor schema and active state conventions

### Stage 2 — Minimum viable reasoning loop
- create a small domain model
- create a simple agent workflow
- support one practical workflow end-to-end
- allow checklist reweighting from the active tensor state

### Stage 3 — Data + interface grounding
- add import/export formats
- add human-facing workflows
- track measured vs inferred data

### Stage 4 — Simulation and advanced tooling
- add scenario analysis
- add temporal reasoning
- add more specialized ecological logic
- refine tensor evolution and multi-parent inheritance if useful

---

## Architectural Risks to Avoid
- building a large abstract framework before proving a useful workflow
- mixing domain logic, UI logic, and agent logic without boundaries
- hiding uncertainty or provenance
- allowing docs and code to drift apart
- making the repo dependent on unclear, unstable assumptions
- turning “agentic” behavior into opaque, unreviewable behavior

---

## Quality Bar
A good contribution to this repository should improve one or more of:
- clarity
- modularity
- usefulness
- trustworthiness
- ecological realism
- collaboration between human and machine reasoning

A contribution that merely increases complexity without improving those qualities should be viewed skeptically.

---

## Open Architectural Questions
- What is the initial runtime stack?
- What is the first concrete workflow to support?
- Which domain objects should be canonical first?
- What should be simulated, and what should remain human judgment?
- How should external spatial/ecological data be represented?

---

## Revision Policy
When implementation begins, revise this file to reflect reality.
Do not preserve outdated architectural intent once the repo has chosen a different direction.
