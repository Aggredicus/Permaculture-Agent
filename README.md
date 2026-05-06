# Permaculture-Agent

`Permaculture-Agent` is a new repository for building a **hybrid-intelligence software system** for permaculture and regenerative design.

Its goal is to combine:
- human ecological judgment
- AI-assisted reasoning and software execution
- durable project memory
- modular architecture
- ethically governed collaboration

This repository is currently at the **foundational scaffolding stage**.

---

## Purpose
The long-term purpose of this project is to support practical work such as:
- permaculture site planning
- ecological design reasoning
- design workflow support
- spatial and geospatial reasoning
- data organization and import/export
- phased implementation planning
- simulation and scenario comparison
- hybrid human + AI collaboration

This repo is meant to become a trustworthy tool-building environment, not just a collection of prompts or code fragments.

---

## Founding Root Documents
This repository begins with four root documents that act as its cognition scaffold:

### `README.md`
Orientation for humans and agents.
Explains the repository’s purpose and how the core docs fit together.

### `AGENT.md`
Defines how AI contributors should behave.
Encodes the repo’s hybrid-intelligence operating model.

### `TEAM_MEMORY.md`
Stores durable project memory.
Preserves important decisions, assumptions, lessons, and open questions.

### `ARCHITECTURE.md`
Defines the intended system structure.
Provides a coherent architectural frame for future implementation work.

Together these four files establish:
- orientation
- behavior
- memory
- structure

---

## Cognitive Tensor Extension
The repository may optionally enable a mutable cognitive tensor layer for adaptive agent behavior.

Supporting files:
- `docs/AGENT_EVOLUTION_WEIGHTS.md`
- `schemas/agent_tensor_state.schema.json`
- `examples/agent_tensor_state.example.json`
- `state/active_agent_tensor_state.json`
- `scripts/evolve_agent_state.py`

This layer allows agents to:
- inherit weighted cognitive traits from prior save states
- reorder build checklists dynamically
- mutate and add new columns over time
- preserve a human-aligned ethical floor while evolving

---

## JEPA-Inspired Site World Model v1.0
This repository includes a lean JEPA-inspired Site World Model subsystem for safer, evidence-grounded permaculture design assistance.

This is **not** a trained neural JEPA model. It is a structured reasoning architecture that applies the JEPA pattern of predicting missing or future site-state representations from partial context using JSON, GraphML-oriented ontology rules, agent roles, workflows, safety gates, privacy scanning, automated tests, CI, and field verification loops.

### What it does

```text
Client/site intake -> observations -> predictions -> risks -> verification tasks -> candidate interventions -> design scenarios -> generated GraphML/checklist/report -> field verification -> updated model
```

The JSON bundle is the editable source of truth. Generated GraphML, checklists, reports, and manifests are reproducible working artifacts.

### What it does not do

It does not approve real-world work, replace field observation, make legal or engineering determinations, certify wetlands, guarantee plant survival, or train a neural JEPA model.

### Public and private data rule

- `examples/` is for public-safe anonymized examples.
- `project_records/` and `private_records/` are for local private work and are ignored by Git.
- Run `privacy-scan` before public commits.

### Primary files
- `docs/JEPA_SITE_WORLD_MODEL_UPGRADE.md`
- `agents/SITE_WORLD_MODEL_AGENT_TEAM.md`
- `ontology/site_world_model_ontology.md`
- `workflows/SITE_WORLD_MODEL_WORKFLOWS.md`
- `prompts/site_world_model_prompts.md`
- `schemas/site_world_model.schema.json`
- `examples/anonymized_site_001/site_world_model_bundle.json`
- `scripts/site_world_model_tools.py`
- `tests/SITE_WORLD_MODEL_TESTS.md`
- `tests/test_site_world_model_tools.py`
- `.github/workflows/site-world-model-ci.yml`

### Quickstart

```bash
python scripts/site_world_model_tools.py validate examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py privacy-scan .
python scripts/site_world_model_tools.py summarize examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py scenario-review examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py graphml examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py checklist examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py report examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py manifest examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py update-verification examples/anonymized_site_001/site_world_model_bundle.json --id pred_001 --status verified --note "Example verification update." --out /tmp/site_world_model_bundle.updated.json
python -m unittest discover -s tests -p "test_*.py"
```

Generated outputs such as `site_model.generated.graphml`, `field_visit_checklist.generated.md`, `client_report.generated.md`, `site_model_manifest.generated.json`, and `*.updated.json` are local working artifacts and should not be committed unless intentionally promoted to reviewed examples.

Safety principle:

> Predictions are never facts. Every inferred condition, future state, risk, or intervention should preserve evidence, confidence, verification status, and field-review requirements.

---

## Working Philosophy
`Permaculture-Agent` is founded on several principles:
- human cognition should remain first-class
- ecological logic should stay grounded in reality
- software architecture should be modular and understandable
- important decisions should be documented
- hybrid intelligence should increase human agency, not replace it
- uncertainty should be surfaced honestly

---

## Current State
At the moment, this repository is effectively a greenfield project with one early practical workflow scaffold: the JEPA-inspired Site World Model.

That means the current priority is to define:
- mission
- architecture
- scope
- workflow
- initial module boundaries
- first practical use case

Before scaling, the project should prove value through one or more small, useful workflows.

---

## Recommended Next Steps
A sensible next sequence is:

1. Test the Site World Model subsystem against additional anonymized examples.
2. Build an importer from approved/anonymized HTML form JSON into the Site World Model bundle.
3. Improve client-report formatting and optional export formats.
4. Add richer GraphML ontology support only after the current workflow proves useful.

---

## Suggested Future Repository Shape

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
├── tests/
└── scripts/
```

This is a planning suggestion, not yet a fixed contract.

---

## How Humans and Agents Should Work Together
### Humans
Humans should provide:
- mission
- acceptance criteria
- ecological judgment
- strategic direction
- ethical boundaries
- final decisions on major tradeoffs

### Agents
Agents should provide:
- structured reasoning
- implementation assistance
- verification support
- synthesis across files and ideas
- memory reinforcement through documentation
- careful surfacing of tradeoffs and uncertainty

The project is strongest when both forms of cognition are used intentionally.

---

## Contribution Expectations
A good contribution should improve one or more of:
- usefulness
- clarity
- ecological relevance
- architectural coherence
- maintainability
- trust between human and machine collaborators

Contributions should avoid:
- unnecessary abstraction
- undocumented assumptions
- architecture drift
- opaque decision-making

---

## License
Add a license once the project direction is confirmed.

---

## Status
Foundational scaffold established.
Implementation direction now includes the lean JEPA-inspired Site World Model as the first practical evidence-and-verification workflow.
