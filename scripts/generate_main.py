#!/usr/bin/env python3
"""Generate the frozen Q1-Q8 main corpus through OpenRouter.

The script creates 8 questions x 2 prompt conditions x 3 independent runs.
It saves every successful call immediately and can resume an interrupted run
with --run-dir. The API key is read only from OPENROUTER_API_KEY.
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
    MAX_OUTPUT_TOKENS,
    PRETENDER_MODEL,
    SHARED_BASE,
    STYLE_CLAUSE,
    TEMPERATURE,
    TOP_P,
    extract_content,
    request_completion,
    save_call,
    utc_now,
)

QUESTION_IDS = tuple(f"Q{index}" for index in range(1, 9))
CONDITIONS = ("naive", "style_controlled")
RUN_IDS = ("run_1", "run_2", "run_3")
EXPECTED_CALLS = len(QUESTION_IDS) * len(CONDITIONS) * len(RUN_IDS)


def parse_questions(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r"^## (Q[1-8])\b[^\n]*\n\n> (.+?)(?=\n\n## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    questions = {
        item_id: " ".join(line.removeprefix("> ").strip() for line in body.splitlines())
        for item_id, body in matches
    }
    if tuple(questions) != QUESTION_IDS:
        raise ValueError(
            f"questions.md must contain Q1-Q8 once and in order; found {tuple(questions)}"
        )
    return questions


def prompt_for(question: str, condition: str) -> str:
    prompt = SHARED_BASE.format(question=question)
    if condition == "style_controlled":
        prompt += "\n\n" + STYLE_CLAUSE
    return prompt


def call_path(run_dir: Path, call_id: str) -> Path:
    return run_dir / "calls" / f"{call_id}.json"


def completed_record(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    content = record.get("extracted_content")
    return record if isinstance(content, str) and content.strip() and not record.get("fatal_error") else None


def response_row(record: dict[str, Any]) -> dict[str, Any]:
    call_id = record["call_id"]
    question_id, condition, run_id = call_id.split("__")
    response = record.get("response") or {}
    choices = response.get("choices") or []
    finish_reason = choices[0].get("finish_reason") if choices else None
    return {
        "call_id": call_id,
        "question_id": question_id,
        "condition": condition,
        "run_id": run_id,
        "requested_model": record["request"]["model"],
        "returned_model": response.get("model"),
        "provider": response.get("provider"),
        "finish_reason": finish_reason,
        "text": record["extracted_content"],
        "usage": response.get("usage"),
    }


def write_consolidated(run_dir: Path) -> dict[str, Any]:
    rows = []
    for path in sorted((run_dir / "calls").glob("Q*__*.json")):
        record = completed_record(path)
        if record:
            rows.append(response_row(record))
    rows.sort(key=lambda row: (row["question_id"], row["condition"], row["run_id"]))
    target = run_dir / "responses.jsonl"
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    expected_ids = {
        f"{question_id}__{condition}__{run_id}"
        for question_id in QUESTION_IDS
        for condition in CONDITIONS
        for run_id in RUN_IDS
    }
    actual_ids = {row["call_id"] for row in rows}
    finish_reasons = Counter(str(row["finish_reason"]) for row in rows)
    summary = {
        "completed_at_utc": utc_now(),
        "run_directory": str(run_dir),
        "expected_calls": EXPECTED_CALLS,
        "completed_calls": len(rows),
        "missing_call_ids": sorted(expected_ids - actual_ids),
        "unexpected_call_ids": sorted(actual_ids - expected_ids),
        "finish_reason_counts": dict(sorted(finish_reasons.items())),
        "all_finish_reasons_stop": len(rows) == EXPECTED_CALLS and finish_reasons == {"stop": EXPECTED_CALLS},
        "main_generation_complete": len(rows) == EXPECTED_CALLS and actual_ids == expected_ids,
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions", type=Path, default=Path("questions.md"))
    parser.add_argument("--output-root", type=Path, default=Path("outputs/main_generation"))
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Resume one existing run directory; completed call files are skipped.",
    )
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    questions = parse_questions(args.questions)
    if args.check_config:
        print("Configuration is valid.")
        print(f"Pretender: {PRETENDER_MODEL}")
        print(f"Questions: {', '.join(questions)}")
        print(f"Conditions: {', '.join(CONDITIONS)}")
        print(f"Runs per condition: {len(RUN_IDS)}")
        print(f"Planned successful calls: {EXPECTED_CALLS}")
        print(f"Temperature: {TEMPERATURE}; top_p: {TOP_P}; max_tokens: {MAX_OUTPUT_TOKENS}")
        print("Seed: unsupported/not requested")
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

    event_log = run_dir / "events.jsonl"
    manifest_path = run_dir / "manifest.json"
    manifest = {
        "started_at_utc": utc_now(),
        "purpose": "Q1-Q8 main Pretender corpus generation",
        "pretender_model": PRETENDER_MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "reasoning": None,
        "seed": None,
        "seed_note": "unsupported/not requested",
        "conditions": list(CONDITIONS),
        "run_ids": list(RUN_IDS),
        "designated_run": "run_1",
        "questions": questions,
        "shared_base": SHARED_BASE,
        "style_clause": STYLE_CLAUSE,
        "api_key_recorded": False,
    }
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    failures = []
    for question_id, question in questions.items():
        for condition in CONDITIONS:
            prompt = prompt_for(question, condition)
            for run_id in RUN_IDS:
                call_id = f"{question_id}__{condition}__{run_id}"
                target = call_path(run_dir, call_id)
                if completed_record(target):
                    print(f"Skipping completed {call_id}", flush=True)
                    continue
                print(f"Calling {call_id}...", flush=True)
                payload = {
                    "model": PRETENDER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "max_tokens": MAX_OUTPUT_TOKENS,
                }
                response = None
                try:
                    response = request_completion(api_key, payload, event_log, call_id)
                    content = extract_content(response)
                    save_call(run_dir, call_id, payload, response, content)
                except Exception as exc:
                    error = str(exc)
                    save_call(run_dir, call_id, payload, response, None, fatal_error=error)
                    failures.append({"call_id": call_id, "error": error})
                    print(f"  recorded failure; continuing after {call_id}", flush=True)
                write_consolidated(run_dir)

    summary = write_consolidated(run_dir)
    summary["failures_this_invocation"] = failures
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Results saved to: {run_dir.resolve()}")
    return 0 if summary["main_generation_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
