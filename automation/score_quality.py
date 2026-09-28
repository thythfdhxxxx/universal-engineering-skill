#!/usr/bin/env python3
"""Score a documented engineering assessment using the portable rubric."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assessment", type=Path, required=True)
    parser.add_argument("--rubric", type=Path, default=Path(__file__).with_name("quality-rubric.json"))
    args = parser.parse_args()
    try:
        assessment = json.loads(args.assessment.read_text(encoding="utf-8"))
        rubric = json.loads(args.rubric.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"cannot parse assessment or rubric: {exc}", file=sys.stderr)
        return 2
    dimensions = assessment.get("dimensions")
    rubric_dimensions = rubric.get("dimensions", [])
    if not isinstance(dimensions, dict) or not isinstance(rubric_dimensions, list):
        print("assessment.dimensions and rubric.dimensions are required", file=sys.stderr)
        return 2
    total_weight = sum(float(item.get("weight", 0)) for item in rubric_dimensions)
    if total_weight <= 0:
        print("rubric weights must be positive", file=sys.stderr)
        return 2
    results = []
    weighted_total = 0.0
    blockers: list[str] = []
    for item in rubric_dimensions:
        dimension_id = item.get("id")
        entry = dimensions.get(dimension_id)
        if not isinstance(entry, dict):
            print(f"missing dimension: {dimension_id}", file=sys.stderr)
            return 2
        score = entry.get("score")
        if not isinstance(score, (int, float)) or not 0 <= score <= 5:
            print(f"invalid score for {dimension_id}: {score!r}", file=sys.stderr)
            return 2
        evidence = entry.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            print(f"dimension has no evidence: {dimension_id}", file=sys.stderr)
            return 2
        entry_blockers = entry.get("blockers", [])
        if isinstance(entry_blockers, list):
            blockers.extend(f"{dimension_id}: {value}" for value in entry_blockers)
        weight = float(item.get("weight", 0))
        weighted_total += (float(score) / 5.0) * weight
        results.append({"id": dimension_id, "score": score, "weight": weight, "evidence": evidence})
    score = round(weighted_total / total_weight * 100, 2)
    level = "Unknown"
    for item in rubric.get("levels", []):
        if item.get("min", 0) <= score <= item.get("max", 100):
            level = item.get("name", "Unknown")
            break
    status = "BLOCKED" if blockers else "PASS"
    report = {
        "project": assessment.get("project"),
        "change_id": assessment.get("change_id"),
        "score": score,
        "level": level,
        "status": status,
        "blockers": blockers,
        "dimensions": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
