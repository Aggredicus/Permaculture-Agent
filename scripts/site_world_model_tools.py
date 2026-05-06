#!/usr/bin/env python3
"""Lean tools for the JEPA-inspired Site World Model.

Commands:
  python scripts/site_world_model_tools.py validate examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py summarize examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py graphml examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py checklist examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py report examples/anonymized_site_001/site_world_model_bundle.json
"""
from __future__ import annotations

import html
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

VALID_CONFIDENCE = {"high", "medium", "low", "unknown"}
VALID_VERIFICATION = {"not_required", "pending", "verified", "contradicted", "revised"}
VALID_CLAIM_TYPES = {
    "observed_fact",
    "client_reported_fact",
    "map_interpreted_feature",
    "image_interpreted_feature",
    "inferred_condition",
    "prediction",
    "design_candidate",
    "design_recommendation",
    "risk",
    "verification_task",
    "assumption",
    "unknown",
    "field_verified_fact",
    "contradicted_prediction",
    "revised_prediction",
}
REQUIRED_SECTIONS = [
    "project",
    "observations",
    "predictions",
    "risks",
    "verification_tasks",
    "interventions",
    "design_scenarios",
]
ITEM_SECTIONS = ["observations", "predictions", "risks", "verification_tasks", "interventions"]
BAD_REPORT_PHRASES = ["guaranteed", "perfect", "will definitely", "no risk"]
HIGH_RISK_WORDS = {"foundation", "utility", "infiltration", "digging", "water", "runoff", "earthwork", "grading"}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def all_items(data: dict[str, Any]):
    for section in ITEM_SECTIONS:
        for item in data.get(section, []):
            yield section, item


def add_ref_errors(errors: list[str], owner_id: str, field: str, refs: list[str], ids: set[str]) -> None:
    for ref in refs:
        if ref not in ids:
            errors.append(f"{owner_id} references missing id in {field}: {ref}")


def validate(path: Path) -> int:
    try:
        data = load(path)
    except Exception as exc:
        print("FAIL")
        print(f"- JSON parse/load error: {exc}")
        return 1

    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in data:
            errors.append(f"missing section: {section}")

    project = data.get("project", {})
    for field in ["project_id", "project_name", "privacy_status"]:
        if field not in project:
            errors.append(f"project missing {field}")

    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for section, item in all_items(data):
        item_id = item.get("id")
        if item_id:
            if item_id in seen:
                duplicates.append(item_id)
            seen[item_id] = section
    for item_id in sorted(set(duplicates)):
        errors.append(f"duplicate id: {item_id}")

    ids = set(seen)
    for section, item in all_items(data):
        item_id = item.get("id", "<missing>")
        for field in ["id", "claim_type", "summary", "source", "confidence", "verification_status"]:
            if field not in item:
                errors.append(f"{section}:{item_id} missing {field}")
        if item.get("claim_type") not in VALID_CLAIM_TYPES:
            errors.append(f"{section}:{item_id} invalid claim_type {item.get('claim_type')}")
        if item.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"{section}:{item_id} invalid confidence {item.get('confidence')}")
        if item.get("verification_status") not in VALID_VERIFICATION:
            errors.append(f"{section}:{item_id} invalid verification_status {item.get('verification_status')}")
        add_ref_errors(errors, item_id, "evidence_ids", item.get("evidence_ids", []), ids)

    task_ids = {item["id"] for item in data.get("verification_tasks", []) if item.get("id")}

    for pred in data.get("predictions", []):
        pred_id = pred.get("id", "<missing>")
        for field in ["based_on", "risk_if_wrong", "verification_required", "verification_tasks"]:
            if field not in pred:
                errors.append(f"prediction {pred_id} missing {field}")
        add_ref_errors(errors, pred_id, "based_on", pred.get("based_on", []), ids)
        add_ref_errors(errors, pred_id, "verification_tasks", pred.get("verification_tasks", []), ids)
        missing_tasks = set(pred.get("verification_tasks", [])) - task_ids
        for task_id in sorted(missing_tasks):
            errors.append(f"prediction {pred_id} verification task does not exist: {task_id}")
        if pred.get("verification_required") and not pred.get("verification_tasks"):
            errors.append(f"prediction {pred_id} requires verification but has no tasks")

    for risk in data.get("risks", []):
        risk_id = risk.get("id", "<missing>")
        for field in ["severity", "likelihood", "mitigation"]:
            if field not in risk:
                errors.append(f"risk {risk_id} missing {field}")

    for task in data.get("verification_tasks", []):
        task_id = task.get("id", "<missing>")
        for field in ["priority", "method", "status"]:
            if field not in task:
                errors.append(f"verification task {task_id} missing {field}")

    for intervention in data.get("interventions", []):
        int_id = intervention.get("id", "<missing>")
        for field in ["status", "supported_by", "benefits", "risks", "required_verification"]:
            if field not in intervention:
                errors.append(f"intervention {int_id} missing {field}")
        if not intervention.get("supported_by"):
            errors.append(f"intervention {int_id} lacks supported_by")
        add_ref_errors(errors, int_id, "supported_by", intervention.get("supported_by", []), ids)
        add_ref_errors(errors, int_id, "required_verification", intervention.get("required_verification", []), ids)
        missing_required = set(intervention.get("required_verification", [])) - task_ids
        for task_id in sorted(missing_required):
            errors.append(f"intervention {int_id} required verification task does not exist: {task_id}")
        joined = " ".join(intervention.get("risks", []) + [intervention.get("summary", "")]).lower()
        risky = any(word in joined for word in HIGH_RISK_WORDS)
        if risky and not set(intervention.get("required_verification", [])).intersection(task_ids):
            errors.append(f"high-risk intervention {int_id} lacks verification")

    for scenario in data.get("design_scenarios", []):
        scenario_id = scenario.get("id", "<missing>")
        for field in ["id", "name", "summary", "benefits", "risks", "unknowns", "verification_needed", "confidence"]:
            if field not in scenario:
                errors.append(f"scenario {scenario_id} missing {field}")
        if scenario.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"scenario {scenario_id} invalid confidence {scenario.get('confidence')}")
        missing = set(scenario.get("verification_needed", [])) - task_ids
        for task_id in sorted(missing):
            errors.append(f"scenario {scenario_id} verification task does not exist: {task_id}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: Site World Model bundle validates.")
    return 0


def summarize(path: Path) -> int:
    data = load(path)
    for section in ["observations", "predictions", "risks", "verification_tasks", "interventions", "design_scenarios"]:
        print(f"{section}: {len(data.get(section, []))}")
    print("pending high-priority checks:")
    for task in data.get("verification_tasks", []):
        if task.get("priority") == "high" and task.get("status") == "pending":
            print(f"- {task['id']}: {task['summary']}")
    return 0


def edge_relationship(field: str) -> str:
    if field in {"verification_tasks", "required_verification"}:
        return "requires_verification_by"
    if field == "supported_by":
        return "supported_by_observation"
    if field == "based_on":
        return "based_on"
    if field == "evidence_ids":
        return "supported_by_evidence"
    return "related_to"


def write_graphml(path: Path) -> int:
    data = load(path)
    out = path.with_name("site_model.generated.graphml")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
    ]
    for key in ["label", "type", "claim_type", "confidence", "source", "verification_status", "relationship"]:
        target = "edge" if key == "relationship" else "all"
        lines.append(f'  <key id="{key}" for="{target}" attr.name="{key}" attr.type="string"/>')
    lines.append('  <graph id="site_world_model_generated" edgedefault="directed">')

    section_type = {
        "observations": "Observation",
        "predictions": "Prediction",
        "risks": "Risk",
        "verification_tasks": "VerificationTask",
        "interventions": "Intervention",
    }
    ids: set[str] = set()
    for section, items in data.items():
        if section not in section_type:
            continue
        for item in items:
            ids.add(item["id"])
            lines.append(f'    <node id="{html.escape(item["id"])}">')
            vals = {
                "label": item["summary"][:120],
                "type": section_type[section],
                "claim_type": item.get("claim_type", ""),
                "confidence": item.get("confidence", ""),
                "source": item.get("source", ""),
                "verification_status": item.get("verification_status", ""),
            }
            for key, value in vals.items():
                lines.append(f'      <data key="{key}">{html.escape(str(value))}</data>')
            lines.append("    </node>")

    edge_count = 1
    ref_fields = ["evidence_ids", "based_on", "supported_by", "verification_tasks", "required_verification"]
    for section, item in all_items(data):
        for field in ref_fields:
            for ref in item.get(field, []):
                if ref in ids:
                    rel = edge_relationship(field)
                    lines.append(f'    <edge id="edge_{edge_count:03d}" source="{html.escape(item["id"])}" target="{html.escape(ref)}">')
                    lines.append(f'      <data key="relationship">{rel}</data>')
                    lines.append("    </edge>")
                    edge_count += 1
    lines += ["  </graph>", "</graphml>"]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ET.parse(out)
    print(f"Wrote {out}")
    return 0


def checklist(path: Path) -> int:
    data = load(path)
    out = path.with_name("field_visit_checklist.generated.md")
    lines = ["# Generated Field Verification Checklist", ""]
    order = {"high": 0, "medium": 1, "low": 2}
    for task in sorted(data.get("verification_tasks", []), key=lambda item: order.get(item.get("priority", "low"), 9)):
        lines.append(f"- [ ] **{task.get('priority', '').upper()}** — {task['summary']}")
        lines.append(f"  - Method: {task.get('method', '')}")
        if task.get("evidence_ids"):
            lines.append(f"  - Related evidence: {', '.join(task.get('evidence_ids', []))}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def report(path: Path) -> int:
    data = load(path)
    out = path.with_name("client_report.generated.md")
    project = data.get("project", {}).get("project_name", "Anonymized site")
    lines = [
        "# Generated Preliminary Client Report",
        "",
        f"**Project:** {project}",
        "",
        "This is a preliminary, evidence-calibrated report. Based on current evidence, the design options below are candidate directions and require field verification before final recommendation.",
        "",
        "## What we know from current records",
    ]
    for obs in data.get("observations", []):
        lines.append(f"- **{obs.get('claim_type', 'claim')}** — {obs['summary']} Confidence: {obs['confidence']}.")

    lines.append("\n## Candidate patterns to verify")
    for pred in data.get("predictions", []):
        tasks = ", ".join(pred.get("verification_tasks", [])) or "none listed"
        lines.append(f"- {pred['summary']} Confidence: {pred['confidence']}. Verification: {tasks}. Risk if wrong: {pred.get('risk_if_wrong', 'not specified')}")

    lines.append("\n## Risk summary")
    for risk in data.get("risks", []):
        lines.append(f"- **{risk.get('severity', 'unknown').upper()}** — {risk['summary']} Mitigation: {risk.get('mitigation', 'requires review')}")

    lines.append("\n## Scenario comparison")
    for scenario in data.get("design_scenarios", []):
        lines.append(f"### {scenario['name']}")
        lines.append(f"{scenario['summary']}")
        lines.append(f"- Confidence: {scenario['confidence']}")
        lines.append(f"- Verification needed: {', '.join(scenario.get('verification_needed', []))}")
        lines.append(f"- Main benefits: {', '.join(scenario.get('benefits', []))}")
        lines.append(f"- Main risks: {', '.join(scenario.get('risks', []))}")

    lines.append("\n## Candidate interventions")
    for intervention in data.get("interventions", []):
        lines.append(f"- {intervention['summary']} Required verification: {', '.join(intervention.get('required_verification', []))}.")

    lines.append("\n## Field-safe next steps")
    for task in data.get("verification_tasks", []):
        lines.append(f"- {task['summary']}")

    text = "\n".join(lines) + "\n"
    lower = text.lower()
    for phrase in BAD_REPORT_PHRASES:
        if phrase in lower:
            raise SystemExit(f"Unsafe report phrase detected: {phrase}")
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    cmd, path = argv[1], Path(argv[2])
    commands = {"validate": validate, "summarize": summarize, "graphml": write_graphml, "checklist": checklist, "report": report}
    if cmd not in commands:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        return 2
    return commands[cmd](path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
