#!/usr/bin/env python3
"""Perform structural QA on a completed Judge audit without showing rationales."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

CAVEAT = (
    "A flipped original-swapped pair is consistent with position sensitivity, "
    "but does not isolate position bias from stochastic run-to-run variability "
    "because each order is evaluated once."
)


def read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_cases(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = {}
    for row in rows:
        key = (row["question_id"], row["condition"], row["judge_id"])
        grouped.setdefault(key, {})[row["order"]] = row

    cases = []
    for (qid, condition, judge), orders in sorted(grouped.items()):
        original = orders.get("original")
        swapped = orders.get("swapped")
        if not original or not swapped:
            status = "incomplete"
        elif not original["schema_valid"] or not swapped["schema_valid"]:
            status = "invalid"
        elif original["selected_identity"] != swapped["selected_identity"]:
            status = "flipped"
        elif original["selected_identity"] == "human_anchor":
            status = "stable_human"
        else:
            status = "stable_pretender"
        c1 = original.get("confidence") if original else None
        c2 = swapped.get("confidence") if swapped else None
        cases.append({
            "question_id": qid,
            "condition": condition,
            "judge_id": judge,
            "original_selected_label": original.get("selected_label") if original else None,
            "original_selected_identity": original.get("selected_identity") if original else None,
            "original_confidence": c1,
            "swapped_selected_label": swapped.get("selected_label") if swapped else None,
            "swapped_selected_identity": swapped.get("selected_identity") if swapped else None,
            "swapped_confidence": c2,
            "absolute_confidence_difference": abs(c1 - c2) if isinstance(c1, int) and isinstance(c2, int) else None,
            "position_case_status": status,
            "interpretation_caveat": CAVEAT if status == "flipped" else "",
        })
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("judge_run_dir", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path("analysis/judge_audit"))
    args = parser.parse_args()

    rows = read_rows(args.judge_run_dir / "judge_outputs.jsonl")
    stamp = args.judge_run_dir.name
    if not stamp or stamp == ".":
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.output_root / stamp
    out.mkdir(parents=True, exist_ok=True)

    cases = build_cases(rows)
    fields = list(cases[0]) if cases else [
        "question_id", "condition", "judge_id", "position_case_status"
    ]
    with (out / "position_cases.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(cases)

    call_status = Counter(
        "schema_valid" if row.get("schema_valid") else "schema_invalid" for row in rows
    )
    case_status = Counter(case["position_case_status"] for case in cases)
    by_judge = Counter(
        (case["judge_id"], case["position_case_status"]) for case in cases
    )
    summary = {
        "source_run": str(args.judge_run_dir),
        "expected_calls": 64,
        "observed_api_outputs": len(rows),
        "call_status_counts": dict(sorted(call_status.items())),
        "expected_original_swapped_pairs": 32,
        "observed_pairs": len(cases),
        "position_case_counts": dict(sorted(case_status.items())),
        "position_case_counts_by_judge": {
            f"{judge}|{status}": count
            for (judge, status), count in sorted(by_judge.items())
        },
        "identity_basis": "selected response identity, not raw A/B label",
        "flipped_case_caveat": CAVEAT,
        "justification_text_inspected_by_this_script": False,
    }
    (out / "structural_qa.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    readme = f"""# Judge audit structural QA

This directory reports execution completeness, schema validity, response-identity
consistency across original and swapped orders, and confidence differences. It
does not display or code Judge justifications.

## Interpretation boundary

{CAVEAT}

The position table compares the selected underlying response identity rather
than raw A/B labels. Justification coding is a separate, subsequently blinded
manual stage.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Structural QA saved to: {out.resolve()}")
    complete = len(rows) == 64 and call_status == {"schema_valid": 64} and len(cases) == 32
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
