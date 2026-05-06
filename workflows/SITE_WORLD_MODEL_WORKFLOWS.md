# Site World Model Workflows

## 01 Intake to observations
Read intake and notes. Extract observed facts, client-reported facts, assumptions, unknowns, and map/image candidates. Output observations JSON or a bundle section named `observations`.

## 02 Observations to GraphML
Create typed nodes and edges. Preserve evidence IDs, confidence, claim type, source, and verification status.

## 03 GraphML to predictions
Infer missing information, likely site patterns, candidate risks, and future states. Include based-on links, confidence, risk-if-wrong, and verification tasks.

## 04 Predictions to design scenarios
Compare scenarios with benefits, risks, unknowns, maintenance load, implementation complexity, verification needs, and client fit.

## 05 Safety review
Audit unsupported claims, high-risk interventions, missing verification, overconfident language, invasive/poison/allergy risks, erosion, standing water, foundation moisture, utilities, permits, wildlife conflict, maintenance overload, and budget mismatch.

## 06 Client report generation
Generate a clear report with known conditions, candidate patterns, risks, verification checklist, phased options, and next steps.

## 07 Field verification update
Update predictions as verified, contradicted, revised, or still pending. Preserve the audit trail rather than overwriting earlier claims.
