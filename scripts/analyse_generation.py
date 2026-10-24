#!/usr/bin/env python3
"""Build generation QA, feature tables, and the manual content-check worksheet."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from extract_surface_features import extract

QUESTION_IDS = tuple(f"Q{index}" for index in range(1, 9))
CONDITIONS = ("naive", "style_controlled")
RUN_IDS = ("run_1", "run_2", "run_3")
EXPECTED = 48


def load_responses(run_dir: Path) -> list[dict[str, Any]]:
    path = run_dir / "responses.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"missing consolidated responses: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_anchors(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r"^## (Q[0-8])(?:[^\n]*)\n\n> (.+?)(?=\n\nWord count:)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    anchors = {
        item_id: " ".join(line.removeprefix("> ").strip() for line in body.splitlines())
        for item_id, body in matches
    }
    if tuple(anchors) != tuple(f"Q{index}" for index in range(9)):
        raise ValueError(f"human_anchors.md must contain Q0-Q8 once and in order; found {tuple(anchors)}")
    return anchors


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_content_worksheet(
    path: Path,
    questions: dict[str, str],
    response_lookup: dict[tuple[str, str, str], str],
) -> None:
    parts = [
        "# Content-Preservation Check — Designated Run 1\n",
        "Use the frozen definitions and allowed values in `content_check.md`. Do not regenerate confounded cases.\n",
    ]
    for question_id in QUESTION_IDS:
        parts.extend(
            [
                f"## {question_id}\n",
                f"**Question:** {questions[question_id]}\n",
                "### Naive, run 1\n",
                response_lookup[(question_id, "naive", "run_1")] + "\n",
                "### Style-controlled, run 1\n",
                response_lookup[(question_id, "style_controlled", "run_1")] + "\n",
                "| Field | Entry |\n|---|---|\n",
                "| `CORE_CLAIM_PRESERVED` |  |\n",
                "| `TECHNICAL_ERROR_DIFFERENCE` |  |\n",
                "| `IMPORTANT_CONTENT_OMISSION` |  |\n",
                "| `ADDITIONAL_CLAIM` |  |\n",
                "| `OVERALL_COMPARABILITY` |  |\n",
                "| `evidence_note` |  |\n",
            ]
        )
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--anchors", type=Path, default=Path("human_anchors.md"))
    parser.add_argument("--questions", type=Path, default=Path("questions.md"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    responses = load_responses(args.run_dir)
    output_dir = args.output_dir or Path("analysis/main") / args.run_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    anchors = parse_anchors(args.anchors)

    response_features = []
    response_lookup = {}
    for row in responses:
        key = (row["question_id"], row["condition"], row["run_id"])
        response_lookup[key] = row["text"]
        response_features.append({
            "source": "pretender",
            "question_id": row["question_id"],
            "condition": row["condition"],
            "run_id": row["run_id"],
            "finish_reason": row.get("finish_reason"),
            **extract(row["call_id"], row["text"]),
        })

    anchor_features = [
        {
            "source": "human_anchor",
            "question_id": question_id,
            "condition": "anchor",
            "run_id": "frozen",
            "finish_reason": "not_applicable",
            **extract(f"{question_id}__anchor", text),
        }
        for question_id, text in anchors.items()
    ]
    all_features = response_features + anchor_features
    write_csv(output_dir / "surface_features_all.csv", all_features)

    numeric_features = [
        key for key in response_features[0]
        if key not in {"source", "question_id", "condition", "run_id", "finish_reason", "text_id"}
    ]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in response_features:
        grouped[(row["question_id"], row["condition"])].append(row)
    summaries = []
    for (question_id, condition), rows in sorted(grouped.items()):
        summary: dict[str, Any] = {
            "question_id": question_id,
            "condition": condition,
            "n_runs": len(rows),
            "n_output_limit_truncated": sum(row["finish_reason"] == "length" for row in rows),
        }
        for feature in numeric_features:
            eligible_rows = (
                [row for row in rows if row["finish_reason"] != "length"]
                if feature in {"word_count", "mean_sentence_length"}
                else rows
            )
            values = [float(row[feature]) for row in eligible_rows if row[feature] is not None]
            summary[f"{feature}__n"] = len(values)
            summary[f"{feature}__mean"] = round(statistics.fmean(values), 3) if values else None
            summary[f"{feature}__min"] = min(values) if values else None
            summary[f"{feature}__max"] = max(values) if values else None
        summaries.append(summary)
    write_csv(output_dir / "question_condition_summary.csv", summaries)

    expected_keys = {
        (question_id, condition, run_id)
        for question_id in QUESTION_IDS for condition in CONDITIONS for run_id in RUN_IDS
    }
    actual_keys = set(response_lookup)
    finish_counts = Counter(str(row.get("finish_reason")) for row in responses)
    qa = {
        "expected_responses": EXPECTED,
        "observed_responses": len(responses),
        "unique_response_keys": len(actual_keys),
        "missing_keys": [list(key) for key in sorted(expected_keys - actual_keys)],
        "unexpected_keys": [list(key) for key in sorted(actual_keys - expected_keys)],
        "finish_reason_counts": dict(sorted(finish_counts.items())),
        "all_finish_reasons_stop": finish_counts == {"stop": EXPECTED},
        "main_generation_complete": len(responses) == EXPECTED and actual_keys == expected_keys,
        "anchor_count": len(anchors),
        "main_anchor_count": sum(question_id != "Q0" for question_id in anchors),
        "q0_anchor_separated_from_main": True,
    }
    (output_dir / "generation_qa.json").write_text(
        json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    question_text = {}
    raw_questions = args.questions.read_text(encoding="utf-8")
    for question_id in QUESTION_IDS:
        match = re.search(rf"^## {question_id}\b[^\n]*\n\n> (.+?)(?=\n\n## |\Z)", raw_questions, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValueError(f"could not parse {question_id} from {args.questions}")
        question_text[question_id] = " ".join(line.removeprefix("> ").strip() for line in match.group(1).splitlines())
    if qa["main_generation_complete"]:
        make_content_worksheet(output_dir / "content_check_run1.md", question_text, response_lookup)

    print(json.dumps(qa, ensure_ascii=False, indent=2))
    print(f"Analysis saved to: {output_dir.resolve()}")
    return 0 if qa["main_generation_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
