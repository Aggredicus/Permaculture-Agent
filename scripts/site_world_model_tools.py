#!/usr/bin/env python3
"""Tools for the JEPA-inspired Site World Model.

Commands:
  validate <bundle.json>
  privacy-scan <path>
  summarize <bundle.json>
  scenario-review <bundle.json>
  graphml <bundle.json>
  checklist <bundle.json>
  report <bundle.json>
  manifest <bundle.json>
  update-verification <bundle.json> --id ID --status STATUS --note NOTE --out OUT
"""
from __future__ import annotations

import argparse
import copy
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

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
NODE_SECTIONS = ITEM_SECTIONS + ["design_scenarios"]
BAD_REPORT_PHRASES = ["guaranteed", "perfect", "will definitely", "no risk", "solves the problem"]
HIGH_RISK_WORDS = {"foundation", "utility", "infiltration", "digging", "water", "runoff", "earthwork", "grading", "pond", "swale", "berm"}
SAFE_PLACEHOLDERS = {"Client A", "Example Site Address", "Example Homestead Project", "ANON-2026-001", "Designer / Organization"}
KNOWN_UNSAFE_TOKENS = ["Fra" "nk", "Kru" "zel", "KR" "ZL", "129" "55", "495" "44"]
TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".json", ".yml", ".yaml", ".html", ".css", ".js", ".ts", ".xml", ".graphml", ".csv"
}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", ".venv", "venv"}
GENERATED_NAMES = {"site_model.generated.graphml", "field_visit_checklist.generated.md", "client_report.generated.md", "site_model_manifest.generated.json"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def all_items(data: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for section in ITEM_SECTIONS:
        for item in data.get(section, []):
            yield section, item


def node_items(data: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for section in NODE_SECTIONS:
        for item in data.get(section, []):
            yield section, item


def add_ref_errors(errors: list[str], owner_id: str, field: str, refs: list[str], ids: set[str]) -> None:
    for ref in refs:
        if ref not in ids:
            errors.append(f"{owner_id} references missing id in {field}: {ref}")


def scan_text_for_pii(text: str, label: str = "<text>") -> list[str]:
    findings: list[str] = []
    patterns = [
        ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
        ("phone", re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]\d{4}(?!\d)")),
        ("street_address", re.compile(r"\b\d{3,6}\s+[A-Za-z0-9 .'-]+\s(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Way|Boulevard|Blvd|Court|Ct|Circle|Cir)\b", re.IGNORECASE)),
        ("city_state_zip", re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b")),
        ("lat_long", re.compile(r"(?<!\d)-?\d{1,2}\.\d{4,}\s*,\s*-?\d{1,3}\.\d{4,}(?!\d)")),
    ]
    for name, pattern in patterns:
        for match in pattern.finditer(text):
            snippet = match.group(0)
            if snippet in SAFE_PLACEHOLDERS:
                continue
            findings.append(f"{label}: {name}: {snippet[:120]}")
    field_patterns = [
        ("client_name", re.compile(r'"client_name"\s*:\s*"([^"]+)"')),
        ("project_address", re.compile(r'"project_address"\s*:\s*"([^"]+)"')),
        ("prepared_by", re.compile(r'"prepared_by"\s*:\s*"([^"]+)"')),
        ("project_id", re.compile(r'"project_id"\s*:\s*"([^"]+)"')),
    ]
    for name, pattern in field_patterns:
        for match in pattern.finditer(text):
            value = match.group(1).strip()
            if not value or value in SAFE_PLACEHOLDERS:
                continue
            if name == "project_id" and (value.startswith("ANON-") or value.startswith("EXAMPLE-")):
                continue
            findings.append(f"{label}: suspicious_{name}: {value[:120]}")
    for token in KNOWN_UNSAFE_TOKENS:
        if token in text:
            findings.append(f"{label}: known_unsafe_token: {token}")
    return findings


def validate_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in data:
            errors.append(f"missing section: {section}")

    project = data.get("project", {})
    for field in ["project_id", "project_name", "privacy_status"]:
        if not project.get(field):
            errors.append(f"project missing or blank {field}")

    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for section, item in node_items(data):
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
        if item.get("claim_type") == "design_recommendation":
            if item.get("confidence") not in {"high", "medium"}:
                errors.append(f"{section}:{item_id} design_recommendation requires high or medium confidence")
            if item.get("verification_status") not in {"verified", "not_required"}:
                errors.append(f"{section}:{item_id} design_recommendation requires verified or not_required verification_status")
        if item.get("confidence") == "low" and item.get("claim_type") == "design_recommendation":
            errors.append(f"{section}:{item_id} low-confidence claim cannot be a design_recommendation")
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

    privacy_status = str(project.get("privacy_status", "")).lower()
    if "anonym" in privacy_status or "example" in privacy_status:
        pii_findings = scan_text_for_pii(json.dumps(data, sort_keys=True), "bundle")
        if pii_findings:
            errors.extend(f"possible PII in anonymized bundle: {finding}" for finding in pii_findings)

    return errors


def validate(path: Path) -> int:
    try:
        data = load(path)
    except Exception as exc:
        print("FAIL")
        print(f"- JSON parse/load error: {exc}")
        return 1
    errors = validate_data(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: Site World Model bundle validates.")
    return 0


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"README", "LICENSE", ".gitignore"}


def iter_text_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in GENERATED_NAMES or path.name.endswith(".updated.json"):
            continue
        if is_text_candidate(path):
            yield path


def privacy_scan(root: Path) -> int:
    findings: list[str] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            findings.append(f"{path}: read_error: {exc}")
            continue
        findings.extend(scan_text_for_pii(text, str(path)))
    if findings:
        print("FAIL: possible public-repo PII found")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS: privacy scan found no high-confidence PII patterns.")
    return 0


def summarize(path: Path) -> int:
    data = load(path)
    for section in ["observations", "predictions", "risks", "verification_tasks", "interventions", "design_scenarios"]:
        print(f"{section}: {len(data.get(section, []))}")
    print("pending high-priority checks:")
    found = False
    for task in data.get("verification_tasks", []):
        if task.get("priority") == "high" and task.get("status") == "pending":
            found = True
            print(f"- {task['id']}: {task['summary']}")
    if not found:
        print("- none")
    return 0


def edge_relationship(field: str, source_section: str = "") -> str:
    if field in {"verification_tasks", "required_verification", "verification_needed"}:
        return "requires_verification_by"
    if field == "supported_by":
        return "supported_by_observation"
    if field == "based_on":
        return "based_on"
    if field == "evidence_ids":
        return "supported_by_evidence"
    return "related_to"


def node_type_for(section: str) -> str:
    return {
        "observations": "Observation",
        "predictions": "Prediction",
        "risks": "Risk",
        "verification_tasks": "VerificationTask",
        "interventions": "Intervention",
        "design_scenarios": "DesignScenario",
    }.get(section, "Unknown")


def item_label(item: dict[str, Any]) -> str:
    return str(item.get("summary") or item.get("name") or item.get("id") or "")[:160]


def write_graphml(path: Path) -> int:
    data = load(path)
    errors = validate_data(data)
    if errors:
        print("FAIL: refusing to generate GraphML from invalid bundle")
        for error in errors:
            print(f"- {error}")
        return 1
    out = path.with_name("site_model.generated.graphml")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
    ]
    for key in ["label", "type", "claim_type", "confidence", "source", "verification_status", "notes", "relationship"]:
        target = "edge" if key == "relationship" else "all"
        lines.append(f'  <key id="{key}" for="{target}" attr.name="{key}" attr.type="string"/>')
    lines.append('  <graph id="site_world_model_generated" edgedefault="directed">')

    ids: set[str] = set()
    for section, items in ((section, data.get(section, [])) for section in NODE_SECTIONS):
        for item in items:
            item_id = item["id"]
            ids.add(item_id)
            lines.append(f'    <node id="{html.escape(item_id)}">')
            vals = {
                "label": item_label(item),
                "type": node_type_for(section),
                "claim_type": item.get("claim_type", "design_scenario" if section == "design_scenarios" else ""),
                "confidence": item.get("confidence", ""),
                "source": item.get("source", ""),
                "verification_status": item.get("verification_status", ""),
                "notes": item.get("notes", ""),
            }
            for key, value in vals.items():
                lines.append(f'      <data key="{key}">{html.escape(str(value))}</data>')
            lines.append("    </node>")

    edge_count = 1
    ref_fields = ["evidence_ids", "based_on", "supported_by", "verification_tasks", "required_verification", "verification_needed"]
    for section, item in node_items(data):
        for field in ref_fields:
            for ref in item.get(field, []):
                if ref in ids:
                    rel = edge_relationship(field, section)
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
    lines = ["# Generated Field Verification Checklist", "", "Use this as a field-review aid. Human review is required before real-world action.", ""]
    order = {"high": 0, "medium": 1, "low": 2}
    for task in sorted(data.get("verification_tasks", []), key=lambda item: order.get(item.get("priority", "low"), 9)):
        lines.append(f"- [ ] **{task.get('priority', '').upper()}** — {task['summary']}")
        lines.append(f"  - Method: {task.get('method', '')}")
        if task.get("evidence_ids"):
            lines.append(f"  - Related evidence: {', '.join(task.get('evidence_ids', []))}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def blocked_status(data: dict[str, Any], scenario: dict[str, Any]) -> str:
    task_lookup = {task["id"]: task for task in data.get("verification_tasks", []) if task.get("id")}
    for task_id in scenario.get("verification_needed", []):
        task = task_lookup.get(task_id)
        if task and task.get("priority") == "high" and task.get("status") == "pending":
            return "blocked_pending_high_priority_verification"
    return "not_blocked_by_high_priority_tasks"


def scenario_review(path: Path) -> int:
    data = load(path)
    print("Scenario Review")
    print("===============")
    for scenario in data.get("design_scenarios", []):
        print(f"\n- {scenario.get('name', scenario.get('id'))}")
        print(f"  id: {scenario.get('id')}")
        print(f"  confidence: {scenario.get('confidence')}")
        print(f"  benefits: {len(scenario.get('benefits', []))}")
        print(f"  risks: {len(scenario.get('risks', []))}")
        print(f"  unknowns: {len(scenario.get('unknowns', []))}")
        print(f"  verification_tasks: {', '.join(scenario.get('verification_needed', [])) or 'none'}")
        print(f"  maintenance_load: {scenario.get('maintenance_load', 'unknown')}")
        print(f"  implementation_complexity: {scenario.get('implementation_complexity', 'unknown')}")
        print(f"  recommended_phase: {scenario.get('recommended_phase', 'unknown')}")
        print(f"  status: {blocked_status(data, scenario)}")
    return 0


def report(path: Path) -> int:
    data = load(path)
    errors = validate_data(data)
    if errors:
        print("FAIL: refusing to generate report from invalid bundle")
        for error in errors:
            print(f"- {error}")
        return 1
    out = path.with_name("client_report.generated.md")
    project = data.get("project", {})
    lines = [
        "# Generated Preliminary Client Report",
        "",
        "## Project Summary",
        f"**Project:** {project.get('project_name', 'Anonymized site')}",
        f"**Project ID:** {project.get('project_id', 'unknown')}",
        f"**Privacy status:** {project.get('privacy_status', 'unknown')}",
        "",
        "## Important Safety Note",
        "This is a preliminary, evidence-calibrated report. Based on current evidence, the design options below are candidate directions and require field review and human review required before final recommendation or real-world action.",
        "",
        "## What We Know From Current Records",
    ]
    for obs in data.get("observations", []):
        lines.append(f"- **{obs.get('claim_type', 'claim')}** — {obs['summary']} Confidence: {obs['confidence']}. Verification: {obs.get('verification_status', 'unknown')}.")

    lines.append("\n## Candidate Patterns To Verify")
    for pred in data.get("predictions", []):
        tasks = ", ".join(pred.get("verification_tasks", [])) or "none listed"
        lines.append(f"- {pred['summary']} Confidence: {pred['confidence']}. Requires verification: {tasks}. Risk if wrong: {pred.get('risk_if_wrong', 'not specified')}.")

    lines.append("\n## Risk Summary")
    for risk in data.get("risks", []):
        lines.append(f"- **{risk.get('severity', 'unknown').upper()}** — {risk['summary']} Mitigation: {risk.get('mitigation', 'requires review')}.")

    lines.append("\n## Scenario Comparison")
    for scenario in data.get("design_scenarios", []):
        lines.append(f"### {scenario['name']}")
        lines.append(f"{scenario['summary']}")
        lines.append(f"- Confidence: {scenario['confidence']}")
        lines.append(f"- Status: {blocked_status(data, scenario)}")
        lines.append(f"- Verification needed: {', '.join(scenario.get('verification_needed', []))}")
        lines.append(f"- Main benefits: {', '.join(scenario.get('benefits', []))}")
        lines.append(f"- Main risks: {', '.join(scenario.get('risks', []))}")

    lines.append("\n## Candidate Interventions")
    for intervention in data.get("interventions", []):
        lines.append(f"- {intervention['summary']} Required verification: {', '.join(intervention.get('required_verification', []))}.")

    lines.append("\n## Field Verification Checklist")
    for task in data.get("verification_tasks", []):
        lines.append(f"- [ ] {task['summary']} ({task.get('priority', 'unknown')} priority)")

    lines.append("\n## Assumptions and Limits")
    lines.append("- This report does not make legal, engineering, wetland, utility, or safety determinations.")
    lines.append("- Client-reported facts and map/image interpretations remain preliminary until verified.")
    lines.append("- Candidate interventions should be downgraded, revised, or deferred if field verification contradicts the current model.")

    lines.append("\n## Recommended Next Steps")
    lines.append("1. Complete high-priority verification tasks first.")
    lines.append("2. Update the site world model with verified, contradicted, or revised predictions.")
    lines.append("3. Re-run validation, GraphML generation, checklist generation, and report generation.")
    lines.append("4. Review final recommendations with the human designer before client delivery.")

    lines.append("\n## Human Review Required")
    lines.append("Human review required before installation, earthwork, water redirection, plant safety claims, utility-adjacent work, or client-facing final recommendations.")

    text = "\n".join(lines) + "\n"
    lower = text.lower()
    for phrase in BAD_REPORT_PHRASES:
        if phrase in lower:
            raise SystemExit(f"Unsafe report phrase detected: {phrase}")
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def manifest(path: Path) -> int:
    data = load(path)
    errors = validate_data(data)
    out = path.with_name("site_model_manifest.generated.json")
    manifest_data = {
        "manifest_version": "1.0.0",
        "bundle_file": str(path),
        "project_id": data.get("project", {}).get("project_id", "unknown"),
        "project_name": data.get("project", {}).get("project_name", "unknown"),
        "privacy_status": data.get("project", {}).get("privacy_status", "unknown"),
        "generated_at": utc_now(),
        "counts": {section: len(data.get(section, [])) for section in ["observations", "predictions", "risks", "verification_tasks", "interventions", "design_scenarios"]},
        "validation_status": "passed" if not errors else "failed",
        "validation_errors": errors,
        "generated_artifacts": ["site_model.generated.graphml", "field_visit_checklist.generated.md", "client_report.generated.md"],
    }
    write_json(out, manifest_data)
    print(f"Wrote {out}")
    return 0 if not errors else 1


def find_item(data: dict[str, Any], item_id: str) -> tuple[str, dict[str, Any]] | None:
    for section, item in node_items(data):
        if item.get("id") == item_id:
            return section, item
    return None


def update_verification(path: Path, item_id: str, status: str, note: str, out: Path) -> int:
    if status not in VALID_VERIFICATION:
        print(f"FAIL: invalid status {status}")
        return 1
    data = load(path)
    updated = copy.deepcopy(data)
    found = find_item(updated, item_id)
    if not found:
        print(f"FAIL: id not found: {item_id}")
        return 1
    section, item = found
    previous = item.get("verification_status")
    item["verification_status"] = status
    if section == "verification_tasks":
        item["status"] = status
    item.setdefault("verification_history", []).append({
        "timestamp": utc_now(),
        "previous_status": previous,
        "new_status": status,
        "note": note,
    })
    errors = validate_data(updated)
    if errors:
        print("FAIL: updated bundle did not validate")
        for error in errors:
            print(f"- {error}")
        return 1
    write_json(out, updated)
    print(f"Wrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="JEPA-inspired Site World Model tooling")
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ["validate", "privacy-scan", "summarize", "scenario-review", "graphml", "checklist", "report", "manifest"]:
        p = sub.add_parser(cmd)
        p.add_argument("path", type=Path)
    p_update = sub.add_parser("update-verification")
    p_update.add_argument("path", type=Path)
    p_update.add_argument("--id", required=True, dest="item_id")
    p_update.add_argument("--status", required=True)
    p_update.add_argument("--note", required=True)
    p_update.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    commands = {
        "validate": validate,
        "privacy-scan": privacy_scan,
        "summarize": summarize,
        "scenario-review": scenario_review,
        "graphml": write_graphml,
        "checklist": checklist,
        "report": report,
        "manifest": manifest,
    }
    if args.command == "update-verification":
        return update_verification(args.path, args.item_id, args.status, args.note, args.out)
    return commands[args.command](args.path)


if __name__ == "__main__":
    raise SystemExit(main())
