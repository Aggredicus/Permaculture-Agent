import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "site_world_model_tools.py"


def base_bundle():
    return {
        "project": {
            "project_id": "ANON-2026-001",
            "project_name": "Example Homestead Project",
            "privacy_status": "anonymized_example_no_private_identifiers",
        },
        "observations": [
            {
                "id": "obs_001",
                "claim_type": "client_reported_fact",
                "summary": "Client reports seasonal standing water near a driveway edge.",
                "source": "intake",
                "evidence_ids": [],
                "confidence": "medium",
                "verification_status": "pending",
                "notes": "Inspect after rainfall.",
            }
        ],
        "predictions": [
            {
                "id": "pred_001",
                "claim_type": "prediction",
                "summary": "Water may concentrate near the driveway edge.",
                "source": "observations",
                "evidence_ids": ["obs_001"],
                "confidence": "medium",
                "verification_status": "pending",
                "based_on": ["obs_001"],
                "risk_if_wrong": "A water feature could be misplaced.",
                "verification_required": True,
                "verification_tasks": ["verify_001"],
                "notes": "Candidate only.",
            }
        ],
        "risks": [
            {
                "id": "risk_001",
                "claim_type": "risk",
                "summary": "Standing water risk if infiltration is poor.",
                "source": "predictions",
                "evidence_ids": ["pred_001"],
                "confidence": "medium",
                "verification_status": "pending",
                "severity": "high",
                "likelihood": "unknown",
                "mitigation": "Perform infiltration testing.",
                "notes": "Blocks final water recommendation.",
            }
        ],
        "verification_tasks": [
            {
                "id": "verify_001",
                "claim_type": "verification_task",
                "summary": "Perform infiltration test.",
                "source": "safety_gate",
                "evidence_ids": ["pred_001"],
                "confidence": "high",
                "verification_status": "pending",
                "priority": "high",
                "method": "Field infiltration test.",
                "status": "pending",
                "notes": "Required before final water intervention.",
            }
        ],
        "interventions": [
            {
                "id": "int_001",
                "claim_type": "design_candidate",
                "summary": "Candidate native rain garden near runoff zone.",
                "source": "predictions",
                "evidence_ids": ["pred_001"],
                "confidence": "medium",
                "verification_status": "pending",
                "status": "candidate",
                "supported_by": ["pred_001", "obs_001"],
                "benefits": ["reduce runoff"],
                "risks": ["poor infiltration", "water/foundation risk if poorly placed"],
                "required_verification": ["verify_001"],
                "maintenance_load": "medium",
                "implementation_complexity": "medium",
                "client_fit": "high",
                "notes": "Do not finalize until checked.",
            }
        ],
        "design_scenarios": [
            {
                "id": "scenario_001",
                "name": "Observation-first stabilization",
                "summary": "Delay final water features until verification.",
                "benefits": ["lowest risk"],
                "risks": ["slower visible progress"],
                "unknowns": ["infiltration rate"],
                "verification_needed": ["verify_001"],
                "maintenance_load": "low",
                "implementation_complexity": "low",
                "recommended_phase": "Phase 1",
                "confidence": "high",
            }
        ],
    }


class SiteWorldModelToolTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def write_bundle(self, directory: Path, bundle=None):
        path = directory / "bundle.json"
        path.write_text(json.dumps(bundle or base_bundle(), indent=2), encoding="utf-8")
        return path

    def test_valid_bundle_passes_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_bundle(Path(tmp))
            result = self.run_tool("validate", path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bad_claim_type_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = base_bundle()
            bundle["observations"][0]["claim_type"] = "bad_type"
            path = self.write_bundle(Path(tmp), bundle)
            result = self.run_tool("validate", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid claim_type", result.stdout)

    def test_duplicate_ids_fail_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = base_bundle()
            bundle["observations"][0]["id"] = "pred_001"
            path = self.write_bundle(Path(tmp), bundle)
            result = self.run_tool("validate", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate id", result.stdout)

    def test_missing_evidence_reference_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = base_bundle()
            bundle["predictions"][0]["evidence_ids"] = ["obs_missing"]
            path = self.write_bundle(Path(tmp), bundle)
            result = self.run_tool("validate", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("references missing", result.stdout)

    def test_high_risk_intervention_without_verification_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = base_bundle()
            bundle["interventions"][0]["required_verification"] = []
            path = self.write_bundle(Path(tmp), bundle)
            result = self.run_tool("validate", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("high-risk intervention", result.stdout)

    def test_privacy_scan_flags_unsafe_sample_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unsafe = (
                "Fra" + "nk" + " " + "Kru" + "zel" + " lives at "
                + "129" + "55" + " 3rd Ave NW, Grand Rapids, MI " + "495" + "44"
            )
            (root / "unsafe.md").write_text(unsafe, encoding="utf-8")
            result = self.run_tool("privacy-scan", root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("possible public-repo PII", result.stdout)

    def test_report_generation_avoids_banned_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_bundle(Path(tmp))
            result = self.run_tool("report", path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = path.with_name("client_report.generated.md").read_text(encoding="utf-8").lower()
            for phrase in ["guaranteed", "perfect", "will definitely", "no risk", "solves the problem"]:
                self.assertNotIn(phrase, report)

    def test_graphml_generation_creates_parseable_xml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_bundle(Path(tmp))
            result = self.run_tool("graphml", path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            ET.parse(path.with_name("site_model.generated.graphml"))

    def test_manifest_generation_creates_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_bundle(Path(tmp))
            result = self.run_tool("manifest", path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads(path.with_name("site_model_manifest.generated.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["validation_status"], "passed")
            self.assertEqual(manifest["counts"]["predictions"], 1)

    def test_update_verification_writes_copy_and_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self.write_bundle(root)
            out = root / "bundle.updated.json"
            result = self.run_tool(
                "update-verification",
                path,
                "--id",
                "pred_001",
                "--status",
                "verified",
                "--note",
                "Example verification update.",
                "--out",
                out,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            original = json.loads(path.read_text(encoding="utf-8"))
            updated = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(original["predictions"][0]["verification_status"], "pending")
            self.assertEqual(updated["predictions"][0]["verification_status"], "verified")
            self.assertIn("verification_history", updated["predictions"][0])


if __name__ == "__main__":
    unittest.main()
