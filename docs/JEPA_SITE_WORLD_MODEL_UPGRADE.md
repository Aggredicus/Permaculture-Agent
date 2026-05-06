# JEPA-Inspired Site World Model Upgrade

## Purpose
This document defines the first practical JEPA-inspired upgrade for `Permaculture-Agent`. It does not train a neural JEPA model. Instead, it applies the JEPA pattern of predicting missing or future state representations from partial context through structured JSON, GraphML, agent roles, workflows, safety gates, and field verification loops.

## Core thesis
A permaculture site should be represented as a living world model, not a static chat response.

```text
Client intake / notes / maps / photos
  -> observations
  -> predictions and missing information
  -> GraphML site ontology
  -> safety review
  -> design scenarios
  -> field verification
  -> updated model
```

## Required claim types
- `observed_fact`: directly observed or measured.
- `client_reported_fact`: reported by the client; useful but not independently verified.
- `map_interpreted_feature`: inferred from maps, contours, or GIS.
- `image_interpreted_feature`: inferred from imagery; candidate-only until verified.
- `inferred_condition`: reasoned from evidence but not directly confirmed.
- `prediction`: possible current or future state inferred from context.
- `design_candidate`: option under consideration.
- `design_recommendation`: recommendation that passed safety and evidence checks.
- `risk`: possible harm, failure mode, conflict, or uncertainty.
- `verification_task`: fieldwork needed to resolve uncertainty.
- `assumption`: explicit unverified premise.
- `unknown`: missing information.
- `field_verified_fact`: confirmed through documented fieldwork.
- `contradicted_prediction`: prediction later found wrong.
- `revised_prediction`: prediction updated after new evidence.

## Confidence values
Allowed values are `high`, `medium`, `low`, and `unknown`.

Low-confidence claims may only produce investigation tasks. Medium-confidence claims may support candidate options. High-confidence claims may support recommendations only when safety gates pass.

## Safety gates
1. **Evidence gate:** every recommendation links to evidence, assumptions, or verification results.
2. **Confidence gate:** low-confidence claims cannot become final recommendations.
3. **Verification gate:** high-risk actions require field verification.
4. **Ecological harm gate:** flag invasive species, poison/allergy, erosion, standing water, foundation moisture, utility conflict, permit uncertainty, wildlife conflict, maintenance overload, budget mismatch, and unverified soil assumptions.
5. **Human review gate:** agents assist; humans approve real-world actions.

## Always require verification before final recommendation
Earthworks, swales, berms, ponds, rain gardens, foundation-adjacent water features, shoreline/wetland work, large tree placement, livestock systems, edible/medicinal plant safety claims, utility-adjacent work, runoff redirection, major grading, and safety/access changes.

## Design principles
The agent should feel careful, grounded, ecologically literate, humble, field-aware, and professional. Client-facing outputs must distinguish what is known, what is reported, what is inferred, what is a candidate, what is unknown, and what requires verification.

Use language like: “based on current evidence,” “candidate,” “possible,” “likely,” and “requires verification.” Avoid: “guaranteed,” “perfect,” “will definitely,” “no risk,” and “this solves the problem.”

## MVP roadmap
- **v0.1:** intake JSON -> observations -> predictions -> GraphML -> verification checklist.
- **v0.2:** scenario forecasting with benefits, risks, unknowns, maintenance load, verification needs, and client fit.
- **v0.3:** visual/map grounding with candidate-only image/map claims.
- **v0.4:** feedback loop for predictions marked verified, contradicted, revised, or pending.
- **v1.0:** client-ready agentic design system with validated artifacts, safety review, GraphML state, and versioned package export.

## Non-goals
This release does not train a neural model, replace field observation, make legal or engineering determinations, certify wetlands, guarantee plant survival, or produce construction documents.

## Long-term path
After enough anonymized, verified projects exist, this repository can support real JEPA-style learning: partial site context -> embeddings of verified site features, missing constraints, likely risks, future states, and successful interventions.