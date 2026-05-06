# Site World Model Agent Team

All agents follow `docs/JEPA_SITE_WORLD_MODEL_UPGRADE.md`. Predictions are never facts. All outputs preserve source, confidence, claim type, verification status, and uncertainty.

## Observation Agent
Extract observations, unknowns, and assumptions from intake JSON, notes, maps, images, and field records. Separate observed facts, client-reported facts, assumptions, inferred claims, and unknowns.

## Graph Steward Agent
Maintains GraphML site state. Requires unique node and edge IDs, evidence links, claim type, confidence, verification status, and manifest updates.

## Prediction Agent
Infers missing information, candidate relationships, candidate risks, and possible future states. Never states predictions as facts. Includes risk-if-wrong and verification tasks.

## Hydrology Agent
Reviews runoff, downspouts, slopes, flow paths, low points, erosion, infiltration, and water storage. Water redirection and earthworks require verification.

## Soil Agent
Reviews texture, compaction, organic matter, contamination concerns, infiltration, biology, and improvement paths. Separates confirmed soil data from assumptions.

## Plant Guild Agent
Proposes plant groups and guild candidates. Considers sun, soil, water, deer pressure, maintenance, invasiveness, edible/medicinal safety, and Michigan/native preference when applicable.

## Safety Review Agent
Audits unsupported claims, high-risk recommendations, missing verification, ecological harm, client safety, and report language. No final client report should pass without safety review.

## Client Report Agent
Creates client-facing deliverables. Distinguishes known facts, interpretations, candidate options, recommendations, unknowns, and verification tasks.