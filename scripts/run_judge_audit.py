#!/usr/bin/env python3
"""Run the frozen 64-call Q1-Q8 LLM Judge audit through OpenRouter.

The script evaluates designated Pretender run_1 only: 8 questions x 2 prompt
conditions x 2 Judge models x 2 A/B orders. It stores each raw response
immediately, continues after failures, and resumes an existing run with
--run-dir. It never prints justification text to the terminal.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from q0_gate import (
    JUDGE_MODELS,
    JUDGE_TEMPLATE,
    MAX_OUTPUT_TOKENS,
    REASONING_CONFIG,
    TEMPERATURE,
    TOP_P,
    extract_content,
    request_completion,
    save_call,
    utc_now,
    validate_judge_json,
)

QUESTION_IDS = tuple(f"Q{i}" for i in range(1, 9))
CONDITIONS = ("naive", "style_controlled")
JUDGES = ("judge_1", "judge_2")
ORDERS = ("original", "swapped")
EXPECTED_CALLS = 64
ORIGINAL_HUMAN_POSITION = {
    "Q1": "B", "Q2": "A", "Q3": "B", "Q4": "B",
    "Q5": "A", "Q6": "A", "Q7": "B", "Q8": "A",
}


def parse_questions(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r"^## (Q[1-8])\b[^\n]*\n\n> (.+?)(?=\n\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    values = {
        qid: " ".join(line.removeprefix("> ").strip() for line in body.splitlines())
        for qid, body in matches
    }
    if tuple(values) != QUESTION_IDS:
        raise ValueError(f"expected Q1-Q8 once and in order; found {tuple(values)}")
    return values


def parse_anchors(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r"^## (Q[1-8])\b[^\n]*\n\n> (.+?)(?=\n\nWord count:)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    values = {
        qid: " ".join(line.removeprefix("> ").strip() for line in body.splitlines())
        for qid, body in matches
    }
    if tuple(values) != QUESTION_IDS:
        raise ValueError(f"expected anchors Q1-Q8 once and in order; found {tuple(values)}")
    return values


def load_pretenders(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("run_id") != "run_1":
                continue
            key = (row.get("question_id"), row.get("condition"))
            if key in rows:
                raise ValueError(f"duplicate designated-run response: {key}")
            rows[key] = row
    expected = {(q, c) for q in QUESTION_IDS for c in CONDITIONS}
    if set(rows) != expected:
        raise ValueError(f"designated-run keys differ: missing={sorted(expected-set(rows))}")
    for key, row in rows.items():
        if not isinstance(row.get("text"), str) or not row["text"].strip():
            raise ValueError(f"empty designated-run response: {key}")
    return rows


def positions(question_id: str, order: str) -> tuple[str, str]:
    human = ORIGINAL_HUMAN_POSITION[question_id]
    if order == "swapped":
        human = "B" if human == "A" else "A"
    return human, "B" if human == "A" else "A"


def completed_api_record(path: Path) -> dict[str, Any] | None:
    """Return a completed primary cell, including a schema-invalid output.

    A successful API output is never silently repeated. Fatal transport/API
    failures remain resumable because no usable model output was returned.
    """
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    content = record.get("extracted_content")
    if record.get("fatal_error") or not isinstance(content, str) or not content.strip():
        return None
    return record


def row_from_record(record: dict[str, Any]) -> dict[str, Any]:
    metadata = record["study_metadata"]
    response = record.get("response") or {}
    validation = record.get("validation") or {}
    parsed = validation.get("parsed") if validation.get("schema_valid") else None
    selection = parsed.get("selected_human_response") if parsed else None
    identity = None
    if selection == "A":
        identity = metadata["response_a_identity"]
    elif selection == "B":
        identity = metadata["response_b_identity"]
    return {
        "call_id": record["call_id"],
        **metadata,
        "requested_model": record["request"]["model"],
        "returned_model": response.get("model"),
        "provider": response.get("provider"),
        "parse_valid": bool(validation.get("parse_valid")),
        "schema_valid": bool(validation.get("schema_valid")),
        "failure_reasons": validation.get("failure_reasons", []),
        "selected_label": selection,
        "selected_identity": identity,
        "confidence": parsed.get("confidence") if parsed else None,
        "justification": parsed.get("justification") if parsed else None,
        "raw_content": record.get("extracted_content"),
    }


def save_study_call(
    run_dir: Path,
    call_id: str,
    payload: dict[str, Any],
    metadata: dict[str, Any],
    response: dict[str, Any] | None,
    content: str | None,
    validation: dict[str, Any] | None = None,
    fatal_error: str | None = None,
) -> None:
    save_call(run_dir, call_id, payload, response, content, validation, fatal_error)
    target = run_dir / "calls" / f"{call_id}.json"
    record = json.loads(target.read_text(encoding="utf-8"))
    record["study_metadata"] = metadata
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")


def consolidate(run_dir: Path) -> dict[str, Any]:
    rows = []
    fatal_ids = []
    for path in sorted((run_dir / "calls").glob("Q*__judge_*__*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if completed_api_record(path):
            rows.append(row_from_record(record))
        elif record.get("fatal_error"):
            fatal_ids.append(record.get("call_id", path.stem))
    rows.sort(key=lambda r: (r["question_id"], r["condition"], r["judge_id"], r["order"]))
    with (run_dir / "judge_outputs.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    expected = {
        f"{q}__{c}__{j}__{o}" for q in QUESTION_IDS for c in CONDITIONS
        for j in JUDGES for o in ORDERS
    }
    actual = {r["call_id"] for r in rows}
    valid = sum(r["schema_valid"] for r in rows)
    invalid = [r["call_id"] for r in rows if not r["schema_valid"]]
    counts = Counter((r["judge_id"], str(r["schema_valid"])) for r in rows)
    summary = {
        "completed_at_utc": utc_now(),
        "run_directory": str(run_dir),
        "expected_calls": EXPECTED_CALLS,
        "completed_api_outputs": len(rows),
        "schema_valid_outputs": valid,
        "missing_call_ids": sorted(expected - actual),
        "schema_invalid_call_ids": sorted(invalid),
        "fatal_call_ids_last_attempt": sorted(fatal_ids),
        "counts_by_judge_and_schema_valid": {
            f"{j}|{v}": n for (j, v), n in sorted(counts.items())
        },
        "primary_execution_complete": actual == expected,
        "full_schema_gate_passed": actual == expected and valid == EXPECTED_CALLS,
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generation_run_dir", type=Path)
    parser.add_argument("--questions", type=Path, default=Path("questions.md"))
    parser.add_argument("--anchors", type=Path, default=Path("human_anchors.md"))
    parser.add_argument("--output-root", type=Path, default=Path("outputs/judge_audit"))
    parser.add_argument("--run-dir", type=Path, help="Resume an existing Judge run.")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    questions = parse_questions(args.questions)
    anchors = parse_anchors(args.anchors)
    pretenders = load_pretenders(args.generation_run_dir / "responses.jsonl")

    if args.check_config:
        print("Configuration is valid.")
        print(f"Generation source: {args.generation_run_dir}")
        print("Designated Pretender responses: 16")
        print(f"Judges: {JUDGE_MODELS[0]}, {JUDGE_MODELS[1]}")
        print(f"Planned primary calls: {EXPECTED_CALLS}")
        print(f"Temperature: {TEMPERATURE}; top_p: {TOP_P}; max_tokens: {MAX_OUTPUT_TOKENS}")
        print("Reasoning: explicitly disabled; response format: json_object")
        print("Each question-condition-Judge-order cell is called once.")
        return 0

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY is not set.", file=sys.stderr)
        return 2

    if args.run_dir:
        run_dir = args.run_dir
        if not run_dir.is_dir():
            print(f"ERROR: resume directory does not exist: {run_dir}", file=sys.stderr)
            return 2
    else:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = args.output_root / stamp
        run_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = run_dir / "manifest.json"
    manifest = {
        "started_at_utc": utc_now(),
        "purpose": "Q1-Q8 designated-run LLM Judge audit",
        "generation_run_dir": str(args.generation_run_dir),
        "judge_models": dict(zip(JUDGES, JUDGE_MODELS)),
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "reasoning": REASONING_CONFIG,
        "response_format": {"type": "json_object"},
        "calls_per_cell": 1,
        "expected_calls": EXPECTED_CALLS,
        "orders": list(ORDERS),
        "original_human_position": ORIGINAL_HUMAN_POSITION,
        "api_key_recorded": False,
    }
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    event_log = run_dir / "events.jsonl"
    for qid in QUESTION_IDS:
        for condition in CONDITIONS:
            pretender = pretenders[(qid, condition)]["text"]
            for judge_index, (judge_id, model) in enumerate(zip(JUDGES, JUDGE_MODELS), start=1):
                for order in ORDERS:
                    call_id = f"{qid}__{condition}__{judge_id}__{order}"
                    target = run_dir / "calls" / f"{call_id}.json"
                    if completed_api_record(target):
                        print(f"Skipping completed {call_id}", flush=True)
                        continue
                    human_position, pretender_position = positions(qid, order)
                    response_a = anchors[qid] if human_position == "A" else pretender
                    response_b = anchors[qid] if human_position == "B" else pretender
                    metadata = {
                        "question_id": qid,
                        "condition": condition,
                        "judge_id": judge_id,
                        "judge_index": judge_index,
                        "order": order,
                        "human_position": human_position,
                        "pretender_position": pretender_position,
                        "response_a_identity": "human_anchor" if human_position == "A" else "pretender",
                        "response_b_identity": "human_anchor" if human_position == "B" else "pretender",
                        "pretender_run_id": "run_1",
                    }
                    prompt = JUDGE_TEMPLATE.format(
                        question=questions[qid], response_a=response_a, response_b=response_b
                    )
                    payload = {
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": TEMPERATURE,
                        "top_p": TOP_P,
                        "max_tokens": MAX_OUTPUT_TOKENS,
                        "reasoning": REASONING_CONFIG,
                        "response_format": {"type": "json_object"},
                    }
                    print(f"Calling {call_id} ({model})...", flush=True)
                    response = None
                    try:
                        response = request_completion(api_key, payload, event_log, call_id)
                        content = extract_content(response)
                        validation = validate_judge_json(content)
                        save_study_call(run_dir, call_id, payload, metadata, response, content, validation)
                    except Exception as exc:
                        save_study_call(
                            run_dir, call_id, payload, metadata, response, None, fatal_error=str(exc)
                        )
                        print(f"  recorded failure; continuing after {call_id}", flush=True)
                    consolidate(run_dir)

    summary = consolidate(run_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Results saved to: {run_dir.resolve()}")
    return 0 if summary["full_schema_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
