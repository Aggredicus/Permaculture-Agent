# HTML Form Instructions for Humans and Agents

**Repository:** `Aggredicus/Permaculture-Agent`  
**Primary HTML app:** `Permaculture_Project_Control_Record_v2_0.html`  
**Document version:** `1.1.0-public-safe`  
**Audience:** Human designers, AI coding agents, project-control agents, documentation agents, and future GraphML/state-management agents.

---

## Public Safety Notice

This repository is public-facing. Example client records, filenames, manifests, reports, and GraphML state must use anonymized placeholder data only.

Do not commit:

- real client names
- real site addresses
- phone numbers
- email addresses
- parcel IDs
- precise private locations
- private contract amounts tied to identifiable people
- unredacted form exports
- photographs or map screenshots that reveal a private property without permission

Use placeholders such as:

```text
Client A
Example Homestead Project
ANON-2026-001
Example Site Address
forms/anon_2026_001_phase_1_scope_freeze_v2_0_0_2026-05-05.json
```

Agents must treat any real personal or property identifier as a stop condition for public commits.

---

## 1. Purpose

This document explains how humans and agents should use the **Permaculture Project Control Record HTML form system** inside the `Permaculture-Agent` repository.

The HTML form is a portable, local-first project documentation interface. It produces structured JSON records that can later be reviewed by humans, interpreted by agents, converted into GraphML, and used to generate reports, task lists, risk warnings, scope summaries, maintenance handoffs, and future-phase recommendations.

The core workflow is:

```text
Human fills HTML form locally
-> Human saves JSON record locally
-> Agent reads approved/anonymized JSON
-> Agent validates required fields and evidence status
-> Agent updates GraphML project state
-> Agent produces summaries, warnings, reports, or next actions
-> Human reviews and approves any real-world decision
```

---

## 2. Repository Context

`Permaculture-Agent` is a hybrid-intelligence software system for permaculture and regenerative design. Its root documents define mission, architecture, behavior, memory, and collaboration expectations.

The HTML form app should be treated as an early practical implementation slice of the broader mission: a field-ready workflow that turns permaculture project information into structured memory while preserving human review and ecological caution.

---

## 3. What the HTML Form System Is

The HTML app is a single-file project-control interface for permaculture design and installation work.

It contains 15 forms:

1. Project Intake & Client Goals Form
2. Site Observation Record
3. Base Map Verification Checklist
4. Constraints & Risk Register
5. Design Decision Log
6. Phase 1 Scope Freeze Form
7. Plant & Materials Specification Sheet
8. Installation Work Order
9. Daily Installation Record
10. Deviation / Field Change Log
11. Change Order Form
12. Final Walkthrough & Punch List
13. Client Maintenance Handoff
14. 30-Day Follow-Up Inspection
15. Project Closeout Report

Each form can be filled in, printed, saved as JSON, loaded from JSON later, saved temporarily as a browser draft, and used as structured input for agents.

The app is intended to act like a lightweight **QC Batch Record** for permaculture projects.

---

## 4. What the HTML Form System Is Not

The form system is not a substitute for professional judgment.

It does not automatically verify property boundaries, legal compliance, utility locations, wetland status, hydrologic engineering, structural safety, soil contamination, plant survival, drainage performance, permit requirements, client payment status, or ecological outcomes.

Human review is required before any real-world implementation decision.

Agents must treat form data as **project evidence**, not guaranteed truth.

---

## 5. Core Human Use Pattern

Recommended sequence for a fast design/install project:

```text
01 Intake
-> 02 Site Observation
-> 03 Base Map Verification
-> 04 Risk Register
-> 05 Design Decision Log
-> 06 Scope Freeze
-> 07 Materials Specification
-> 08 Installation Work Order
-> 09 Daily Installation Record
-> 10 Deviation Log, if needed
-> 11 Change Order, if needed
-> 12 Final Walkthrough
-> 13 Maintenance Handoff
-> 14 30-Day Follow-Up
-> 15 Closeout Report
```

For small projects, not every form must be completed immediately. Before installation begins, the recommended minimum record is:

```text
01 Intake
02 Site Observation
04 Constraints & Risk Register
06 Phase 1 Scope Freeze
07 Plant & Materials Specification
08 Installation Work Order
13 Client Maintenance Handoff
```

---

## 6. JSON File Contract

When a user saves a form, the HTML app exports a JSON object with this general structure:

```json
{
  "app": "Permaculture Works Project Control Record",
  "app_version": "2.0.0",
  "form_key": "scopeFreeze",
  "form_title": "06 · Phase 1 Scope Freeze Form",
  "form_slug": "phase_1_scope_freeze",
  "saved_at": "2026-05-05T12:00:00.000Z",
  "values": {
    "project_name": "Example Homestead Project",
    "project_id": "ANON-2026-001",
    "document_name": "phase_1_scope_freeze",
    "document_version": "2.0.0",
    "client_name": "Client A",
    "prepared_by": "Designer / Organization",
    "project_address": "Example Site Address",
    "date_prepared": "2026-05-05"
  }
}
```

Agents must inspect `app`, `app_version`, `form_key`, `form_title`, `form_slug`, `saved_at`, `values.project_name`, `values.project_id`, `values.document_name`, `values.document_version`, `values.client_name`, `values.project_address`, and `values.date_prepared`.

If any are missing, agents should flag the record as incomplete rather than inventing missing metadata.

---

## 7. Filename and Versioning Rules

The HTML app automatically generates JSON filenames using:

```text
ProjectName_DocumentName_vVersion_YYYY-MM-DD.json
```

Public-safe example:

```text
anon_2026_001_phase_1_scope_freeze_v2_0_0_2026-05-05.json
```

Good public-safe names:

```text
example_homestead_project
anon_2026_001
phase_1_scope_freeze
site_observation_record
```

Avoid vague names:

```text
test
new
form1
client_notes
untitled
```

Agents must preserve source filename, document version, and `saved_at` metadata when transforming JSON into reports, summaries, GraphML, CSV, or manifest entries.

Agents should not overwrite previous versions unless explicitly instructed.

---

## 8. Evidence and Certainty Rules

Agents must classify information according to its certainty.

Recommended evidence statuses:

```text
observed
client_reported
assumed
verified
approved
deferred
unknown
needs_review
```

Examples:

| Form entry | Proper interpretation |
|---|---|
| Standing water observed near west edge | Observed site evidence |
| Client reports water pools here every spring | Client-reported evidence |
| Likely clay soil | Assumption unless tested |
| Utility locate complete | Verified only if documented |
| Phase 1 excludes pond excavation | Approved scope exclusion if signed/approved |
| Possible wetland | Needs review; do not treat as confirmed wetland |

Agents should avoid upgrading weak evidence into strong conclusions.

---

## 9. GraphML Model State

The JSON records are form-level documents. The GraphML model is the agent-readable project state.

The GraphML should represent project identity, client/property metadata, goals, site observations, constraints, risks, decisions, approved scope, exclusions, assumptions, materials, work areas, tasks, quality checkpoints, deviations, change orders, maintenance responsibilities, follow-up findings, and closeout lessons.

The GraphML should not store raw form JSON as one giant string. Agents should extract typed nodes and typed relationships.

---

## 10. Recommended GraphML Node Types

Agents may create nodes of these types:

```text
Project
Client
Designer
Property
Document
ProjectPhase
Goal
SuccessCriterion
Constraint
Risk
ControlMeasure
Observation
PhotoEvidence
WaterFlow
WetArea
DryArea
SoilCondition
Microclimate
VegetationFeature
WildlifePressure
InfrastructureFeature
NoDigZone
MapSource
MapLimitation
DesignDecision
Alternative
Evidence
ScopeFreeze
IncludedArea
IncludedWork
Exclusion
Assumption
ClientResponsibility
FuturePhaseIdea
Plant
Material
Supplier
ProtectionMaterial
SeedMix
Task
Tool
CrewMember
QualityCheckpoint
InstallationDay
Issue
Deviation
CorrectiveAction
ChangeOrder
CostImpact
ScheduleImpact
RiskImpact
Approval
PunchListItem
MaintenanceInstruction
InspectionFinding
FuturePhaseOpportunity
CloseoutReport
LessonLearned
```

---

## 11. Recommended GraphML Edge Types

Agents may create relationships such as:

```text
HAS_CLIENT
HAS_DESIGNER
LOCATED_AT
HAS_DOCUMENT
HAS_PHASE
HAS_GOAL
HAS_SUCCESS_CRITERION
LIMITED_BY
DOCUMENTS
SUPPORTS
AFFECTS
CONSTRAINS
CREATES_RISK
MITIGATED_BY
MUST_PRECEDE
BLOCKS
BASED_ON
REJECTED_ALTERNATIVE
APPROVES
INCLUDES
EXCLUDES
ASSIGNED_TO
DEFERRED_FROM
SOURCED_FROM
USED_FOR
HAS_QUALITY_CHECKPOINT
COMPLETED
OBSERVED_DURING
MODIFIES
ADDS
CHANGES
AUTHORIZES
REMAINS_AFTER
TRIGGERS
DERIVED_FROM
CLOSES
```

Edges should include source metadata when possible:

```text
source_form
source_file
source_document_version
source_saved_at
confidence
notes
```

---

## 12. JSON-to-GraphML Mapping Guide by Form

### 01 Project Intake & Client Goals
Create or update `Project`, `Client`, `Property`, `Goal`, `SuccessCriterion`, `BudgetConstraint`, `TimelineConstraint`, `MaintenanceCapacity`, `DesiredOutput`, and `KnownConstraint` nodes.

### 02 Site Observation Record
Create or update `Observation`, `PhotoEvidence`, `WaterFlow`, `WetArea`, `DryArea`, `SoilCondition`, `Microclimate`, `VegetationFeature`, `WildlifePressure`, `InfrastructureFeature`, `NoDigZone`, and `UtilityConcern` nodes.

### 03 Base Map Verification Checklist
Create or update `MapSource`, `MapLimitation`, `BoundaryStatus`, `ScaleStatus`, `SlopeConfidence`, `SuitabilityFinding`, and `RequiredCorrection` nodes.

### 04 Constraints & Risk Register
Create or update `Constraint`, `Risk`, `ControlMeasure`, `Owner`, `GoNoGoConcern`, and `RequiredControl` nodes.

### 05 Design Decision Log
Create or update `DesignDecision`, `Alternative`, `Evidence`, `Tradeoff`, `Approval`, and `FuturePhaseDecision` nodes.

### 06 Phase 1 Scope Freeze Form
Create or update `ScopeFreeze`, `ProjectPhase`, `IncludedArea`, `IncludedWork`, `Quantity`, `InstallationMethod`, `EarthworkLimit`, `Exclusion`, `Assumption`, `ClientResponsibility`, `ChangeOrderRule`, `FuturePhaseIdea`, and `Approval` nodes.

### 07 Plant & Materials Specification Sheet
Create or update `Plant`, `Material`, `Supplier`, `ProtectionMaterial`, `SeedMix`, `ProcurementStatus`, `SubstitutionRule`, and `InstalledInventory` nodes.

### 08 Installation Work Order
Create or update `Task`, `Tool`, `CrewMember`, `QualityCheckpoint`, `SafetyNote`, `WeatherConstraint`, `LayoutReference`, and `MaterialStagingArea` nodes.

### 09 Daily Installation Record
Create or update `InstallationDay`, `CompletedTask`, `MaterialUsed`, `PlantInstalled`, `Issue`, `ClientApproval`, `PhotoEvidence`, and `NextDayPriority` nodes.

### 10 Deviation / Field Change Log
Create or update `Deviation`, `FieldChange`, `CorrectiveAction`, `CostImpact`, `ScheduleImpact`, `RiskImpact`, and `Approval` nodes.

### 11 Change Order Form
Create or update `ChangeOrder`, `AddedWork`, `RemovedWork`, `AddedMaterial`, `AddedLabor`, `CostImpact`, `ScheduleImpact`, `RiskImpact`, and `Approval` nodes.

### 12 Final Walkthrough & Punch List
Create or update `Walkthrough`, `CompletionChecklistItem`, `PunchListItem`, `ClientAcceptance`, `RemainingConcern`, and `FollowUpAppointment` nodes.

### 13 Client Maintenance Handoff
Create or update `MaintenanceInstruction`, `WateringSchedule`, `WeedingInstruction`, `MulchCareInstruction`, `NoMowRule`, `ProtectionCheck`, `WarningSign`, `ClientResponsibility`, and `FollowUpDate` nodes.

### 14 30-Day Follow-Up Inspection
Create or update `FollowUpInspection`, `InspectionFinding`, `PlantSurvivalStatus`, `MoistureCondition`, `MulchCondition`, `WeedPressure`, `AnimalDamage`, `CorrectiveAction`, `ReplacementRecommendation`, and `FuturePhaseOpportunity` nodes.

### 15 Project Closeout Report
Create or update `CloseoutReport`, `CompletedScope`, `FinalDeliverable`, `FinalInventorySummary`, `OpenItem`, `ClientFeedback`, `LessonLearned`, `FuturePhaseRecommendation`, and `ArchiveItem` nodes.

---

## 13. Agent Roles

### Project Record Agent
Maintains JSON records, project manifests, GraphML state, source metadata, missing-form detection, and project-state summaries.

### Intake Agent
Summarizes client goals, identifies decision-makers, identifies scope risks, prepares site visit agendas, and recommends missing intake questions.

### Site Analysis Agent
Summarizes site observations, extracts land features, identifies evidence gaps, and links observations to risks and design options.

### Risk and Scope Control Agent
Reads risk register and scope freeze records, detects blocked tasks, enforces exclusions, routes new work to change order, and produces go/no-go checklists.

### Procurement Agent
Reads materials specifications, checks plant/material completeness, flags missing protection systems, creates shopping lists, and proposes substitutions for human approval.

### Installation Agent
Reads work orders, sequences tasks, prepares crew briefings, checks quality checkpoints, and compares daily records to approved scope.

### Deviation and Change Control Agent
Reviews daily records and deviation logs, identifies changes needing change orders, summarizes cost/schedule/risk impacts, and preserves original scope history.

### Handoff and Follow-Up Agent
Generates maintenance instructions, summarizes client responsibilities, prepares follow-up inspection summaries, and recommends corrective actions.

### Closeout and Learning Agent
Creates final summaries, extracts lessons learned, identifies future-phase opportunities, and updates templates/team memory when approved.

---

## 14. Validation Checklist for Agents

Before using a JSON file, agents should check:

```text
[ ] JSON parses successfully
[ ] app field matches expected form system
[ ] app_version is recorded
[ ] form_key is recognized
[ ] form_title is present
[ ] saved_at is present
[ ] project_name is present
[ ] document_name is present
[ ] document_version is present
[ ] client_name is present, if client-specific
[ ] project_address is present, if site-specific
[ ] required project fields are not blank
[ ] source filename is preserved
[ ] record is not superseded by a newer version
[ ] public-facing records are anonymized
```

Before generating installation instructions, agents should check:

```text
[ ] Scope freeze exists
[ ] Scope status is approved or ready for approval
[ ] Open high/critical risks are reviewed
[ ] Utility/septic/well constraints are addressed where digging occurs
[ ] Wet-area or pond-edge work is not assumed safe
[ ] Materials are specified
[ ] Plant protection is specified where wildlife pressure is present
[ ] Client responsibilities are documented
[ ] Change orders exist for post-freeze additions
```

---

## 15. Suggested Public-Safe Project Manifest

A project-level manifest should track form files and graph state.

```json
{
  "project_id": "ANON-2026-001",
  "project_name": "Example Homestead Project",
  "client": "Client A",
  "current_phase": "Phase 1 Layout",
  "graphml_file": "graph/project_state.graphml",
  "forms": [
    {
      "form_key": "intake",
      "file": "forms/anon_2026_001_project_intake_client_goals_v2_0_0_2026-05-05.json",
      "version": "2.0.0",
      "status": "complete"
    },
    {
      "form_key": "siteObservation",
      "file": "forms/anon_2026_001_site_observation_record_v2_0_0_2026-05-05.json",
      "version": "2.0.0",
      "status": "complete"
    }
  ],
  "open_risks": 3,
  "approved_scope": false,
  "last_updated": "2026-05-05"
}
```

Agents should update the manifest whenever they ingest a new JSON file or generate a new graph.

---

## 16. Suggested Repository Workflow

A good local workflow is:

```text
1. Open Permaculture_Project_Control_Record_v2_0.html locally
2. Fill the relevant form
3. Save JSON to a private local project folder
4. Anonymize before public commit
5. Run scripts/ingest_form_json.py when available
6. Update graph/project_state.graphml when available
7. Run validation checks
8. Generate reports
9. Human reviews generated outputs
10. Human approves any real-world actions
11. Agent commits only approved, anonymized documentation/code changes
```

Recommended private project folder:

```text
project_records/
└── ANON-2026-001/
    ├── forms/
    ├── graph/
    │   ├── project_state.graphml
    │   ├── project_nodes.csv
    │   ├── project_edges.csv
    │   └── project_manifest.json
    └── reports/
        ├── project_summary.md
        ├── open_risks.md
        └── next_actions.md
```

---

## 17. Human Review Requirements

Human approval is required before sending a client-facing report, changing approved scope, starting excavation or earthwork, recommending a legal/regulatory conclusion, finalizing plant substitutions, committing cost or schedule changes, marking high-risk items closed, publishing case studies, or altering source forms/schemas/GraphML state logic.

Agents should draft and validate; humans decide.

---

## 18. Safety and Scope-Control Rules

Agents must follow these rules:

1. Do not invent missing site facts.
2. Do not treat client-reported claims as verified unless documented.
3. Do not treat maps as survey-grade unless explicitly verified.
4. Do not approve earthwork when utilities, septic, wetland, overflow, or erosion risks are unresolved.
5. Do not add excluded or future-phase work into installation instructions.
6. Do not treat a design idea as an approved scope item.
7. Do not guarantee plant survival.
8. Do not guarantee legal compliance.
9. Do not guarantee drainage performance.
10. Do not recommend invasive, illegal, or ecologically risky species.
11. Do not overwrite previous records without preserving version history.
12. Do not hide uncertainty.
13. Do not commit real client/property identifiers to public branches.

---

## 19. Minimum GraphML Attributes

Every generated GraphML node should include, when possible:

```text
id
type
label
status
confidence
source_form
source_file
source_document_version
source_saved_at
created_at
updated_at
notes
```

Every generated GraphML edge should include, when possible:

```text
source
target
relationship
status
confidence
source_form
source_file
source_document_version
source_saved_at
notes
```

---

## 20. Example Agent Update Procedure

When ingesting a new JSON form:

```text
1. Parse JSON.
2. Validate top-level fields.
3. Identify project_id and project_name.
4. Check whether this document version already exists.
5. Extract entities from values.
6. Classify evidence status where possible.
7. Create or update GraphML nodes.
8. Create or update GraphML edges.
9. Preserve source filename and version metadata.
10. Update project_manifest.json.
11. Run validation checks.
12. Generate a human-readable change summary.
13. Ask for human approval if real-world decisions are affected.
14. Confirm anonymization before public commit.
```

---

## 21. Example Agent Summary Format

After ingesting a public-safe example form, agents should report:

```markdown
## Ingest Summary

**Source file:** anon_2026_001_phase_1_scope_freeze_v2_0_0_2026-05-05.json  
**Form:** 06 · Phase 1 Scope Freeze Form  
**Project:** Example Homestead Project  
**Version:** 2.0.0  

### Added / Updated Nodes
- ScopeFreeze: Phase 1 Scope Freeze
- IncludedArea: North Field
- IncludedWork: Swale/Berm Layout
- Exclusion: Pond Excavation
- ClientResponsibility: Watering

### Added / Updated Relationships
- ScopeFreeze INCLUDES North Field
- ScopeFreeze EXCLUDES Pond Excavation
- Watering ASSIGNED_TO Client

### Open Questions
- Utility locate status is not documented.
- Earthwork overflow route needs confirmation.

### Agent Recommendation
Do not generate excavation work orders until utility status and overflow route are verified.
```

---

## 22. How This Fits the Repo Philosophy

This form system supports the repository’s founding philosophy:

- Human cognition remains first-class.
- Ecological logic stays grounded in reality.
- Important decisions are documented.
- AI contributes structure, synthesis, validation, and memory.
- Uncertainty is surfaced honestly.
- Architecture remains modular and understandable.
- Hybrid intelligence increases human agency rather than replacing it.

The HTML form app is the human interface.  
The JSON files are durable project records.  
The GraphML file is the shared semantic project state.  
The agents are assistants that maintain coherence, flag risks, and help generate useful outputs.  
The human designer remains the accountable decision-maker.

---

## 23. Recommended Next Build Steps

1. Keep public examples anonymized.
2. Create `examples/project_control_record/` with public-safe sample JSON exports.
3. Create `schemas/project_control_record.schema.json`.
4. Create `scripts/ingest_form_json.py`.
5. Create `scripts/build_project_graph.py`.
6. Create `scripts/validate_project_graph.py`.
7. Create `scripts/summarize_project_state.py`.
8. Create `graph/project_manifest.example.json`.
9. Add a short section to `AGENT.md` instructing agents to follow this document when working with form JSON or GraphML project state.
10. Add a privacy scan/check before public commits.

---

## 24. Final Operating Rule

The Project Control Record should always answer five questions:

```text
What do we know?
How do we know it?
What is approved?
What is blocked?
What should happen next?
```

Any agent working with this system should preserve those answers clearly while protecting private client and property information.
