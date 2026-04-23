#!/usr/bin/env python3
"""Evolve an agent tensor state with bounded Gaussian mutation."""

from __future__ import annotations
import argparse, copy, json, random
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SIGMA = 0.03
DEFAULT_ETHICAL_FLOOR = {
    "HumanAlignment": 0.90,
    "Truthfulness": 0.90,
    "Accountability": 0.90,
    "LoveAsOrientation": 0.90,
}

def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))

def mutate_weight(value: float, sigma: float) -> float:
    return clamp(value + random.gauss(0.0, sigma))

def evolve_state(parent: dict, new_state_id: str, objective_summary: str | None, feedback: dict | None, sigma: float) -> dict:
    child = copy.deepcopy(parent)
    child["state_id"] = new_state_id
    child["timestamp"] = datetime.now(timezone.utc).isoformat()
    if objective_summary:
        child["objective_summary"] = objective_summary
    parent_id = parent.get("state_id")
    child["parent_state_ids"] = [parent_id] if parent_id else []
    inheritance = child.setdefault("inheritance", {})
    inheritance["parent_state_ids"] = child["parent_state_ids"]
    inheritance["policy"] = "bounded_gaussian"
    inheritance["sigma"] = sigma
    floor = inheritance.setdefault("ethical_floor", copy.deepcopy(DEFAULT_ETHICAL_FLOOR))
    weights = child.get("weights", {})
    for key, old_value in list(weights.items()):
        if not isinstance(old_value, (int, float)):
            continue
        new_value = mutate_weight(float(old_value), sigma)
        if key in floor:
            new_value = max(new_value, float(floor[key]))
        weights[key] = round(new_value, 10)
    if feedback:
        child["fitness_signals"] = feedback
    child.setdefault("new_columns_added", [])
    child.setdefault("columns_deprecated", [])
    return child

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--state-id", required=True)
    parser.add_argument("--objective-summary", default=None)
    parser.add_argument("--sigma", type=float, default=DEFAULT_SIGMA)
    parser.add_argument("--feedback", default=None)
    parser.add_argument("--set-weight", action="append", default=[])
    parser.add_argument("--add-column", action="append", default=[])
    args = parser.parse_args()

    parent = json.loads(Path(args.input).read_text(encoding="utf-8"))
    feedback = json.loads(args.feedback) if args.feedback else None
    child = evolve_state(parent, args.state_id, args.objective_summary, feedback, args.sigma)

    for entry in args.add_column:
        key, value = entry.split("=", 1)
        child.setdefault("weights", {})[key] = round(clamp(float(value)), 10)
        child.setdefault("new_columns_added", []).append(key)

    for entry in args.set_weight:
        key, value = entry.split("=", 1)
        v = clamp(float(value))
        floor = child.get("inheritance", {}).get("ethical_floor", {})
        if key in floor:
            v = max(v, float(floor[key]))
        child.setdefault("weights", {})[key] = round(v, 10)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(child, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")

if __name__ == "__main__":
    main()
