# Site World Model Tests

Run these commands from the repository root:

```bash
python scripts/site_world_model_tools.py validate examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py summarize examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py graphml examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py checklist examples/anonymized_site_001/site_world_model_bundle.json
python scripts/site_world_model_tools.py report examples/anonymized_site_001/site_world_model_bundle.json
```

Expected behavior:

- Validation prints `PASS`.
- Summary reports observations, predictions, risks, verification tasks, interventions, and design scenarios.
- GraphML generation writes `site_model.generated.graphml` next to the bundle.
- Checklist generation writes `field_visit_checklist.generated.md`.
- Report generation writes `client_report.generated.md`.

Failure cases to test later:

- A prediction that references a missing evidence ID should fail validation.
- A prediction requiring verification but lacking tasks should fail validation.
- A high-risk water/foundation/utility intervention without verification should fail validation.
- A generated client report containing guarantee language should fail before being used.
