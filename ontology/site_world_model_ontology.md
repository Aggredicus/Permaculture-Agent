# Site World Model GraphML Ontology

## Node types
Site, Zone, Sector, Structure, AccessPath, SlopeArea, FlowPath, LowPoint, HighPoint, SoilArea, Microclimate, WaterSource, ExistingPlant, DesiredPlant, PlantGuild, ClientGoal, DesignConstraint, Observation, Prediction, Risk, VerificationTask, Intervention, FutureState, MaintenanceTask.

## Edge types
contains, adjacent_to, upslope_of, downslope_of, drains_to, shades, exposed_to, supports, conflicts_with, requires, mitigates, increases_risk_of, decreases_risk_of, predicted_to_cause, requires_verification_by, supported_by_observation, contradicted_by_observation, preferred_by_client, constrained_by.

## Fields
Nodes and edges should include `label`, `type`, `claim_type`, `confidence`, `source`, `verification_status`, and `notes`.

## ID style
Use stable IDs such as `obs_001`, `pred_001`, `risk_001`, `verify_001`, and `int_001`. Do not encode private addresses or client names in IDs.
