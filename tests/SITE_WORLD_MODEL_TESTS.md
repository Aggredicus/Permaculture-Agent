# Site World Model Tests

The Site World Model v1.0 workflow uses one standard-library Python tool plus automated unit tests.

Run these commands from the repository root:

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

Expected behavior:

- Validation prints `PASS`.
- Privacy scan reports no high-confidence PII patterns in the current public-safe branch files.
- Summary reports observations, predictions, risks, verification tasks, interventions, and design scenarios.
- Scenario review prints blocked/not-blocked status for each design scenario.
- GraphML generation writes `site_model.generated.graphml` next to the bundle.
- Checklist generation writes `field_visit_checklist.generated.md`.
- Report generation writes `client_report.generated.md`.
- Manifest generation writes `site_model_manifest.generated.json`.
- Update verification writes a copied updated bundle and preserves the original file.
- Unit tests pass with Python standard library `unittest`.

Failure cases covered by automated tests:

- A bad claim type fails validation.
- Duplicate IDs fail validation.
- A prediction that references a missing evidence ID fails validation.
- A high-risk water/foundation/utility intervention without verification fails validation.
- Privacy scan flags intentionally unsafe sample text generated inside a temporary test directory.
- Generated reports avoid banned overclaiming language.
- Generated GraphML parses as XML.
- Generated manifest parses as JSON.
- Verification updates preserve the original bundle and write an updated copy.
