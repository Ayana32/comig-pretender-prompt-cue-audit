#!/usr/bin/env python3
"""Recalculate the headline pilot statistics from the public CSV exports."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "results" / "csv"
OUTPUT = ROOT / "results" / "reproduced_metrics.json"

STYLE = {"STYLE_FORMAT", "STYLE_REGISTER", "LANGUAGE_FORM", "AI_STEREOTYPE"}
SUBSTANTIVE = {
    "TECHNICAL_SUBSTANCE",
    "CONTEXT_SENSITIVITY",
    "EPISTEMIC_STYLE",
    "EXPERIENTIAL_TACIT",
    "SOCIAL_MEMBERSHIP",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (CSV_DIR / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float]:
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    half_width = z * math.sqrt(
        (proportion * (1 - proportion) + z * z / (4 * total)) / total
    ) / denominator
    return [centre - half_width, centre + half_width]


def exact_mcnemar_two_sided(left: int, right: int) -> float:
    discordant = left + right
    lower = min(left, right)
    tail = sum(math.comb(discordant, k) for k in range(lower + 1)) / (2**discordant)
    return min(1.0, 2 * tail)


coding = read_csv("justification_coding.csv")
events = read_csv("cue_events.csv")
key = read_csv("unblinding_key.csv")
key_by_id = {row["Blind ID"]: row for row in key}

for row in coding:
    row.update(key_by_id[row["Blind ID"]])
for row in events:
    row.update(key_by_id[row["Blind ID"]])

primary = defaultdict(Counter)
for row in coding:
    family = "style_form" if row["Primary cue"] in STYLE else "substantive_practical"
    primary[row["Condition"]][family] += 1

paired = defaultdict(dict)
for row in coding:
    unit = (row["Question"], row["Judge"], row["Order"])
    paired[unit][row["Condition"]] = row["Primary cue"] in STYLE
style_to_nonstyle = sum(v["naive"] and not v["style_controlled"] for v in paired.values())
nonstyle_to_style = sum(not v["naive"] and v["style_controlled"] for v in paired.values())

selections = defaultdict(Counter)
for row in key:
    selections[row["Condition"]][row["Selected identity"]] += 1

position_groups = defaultdict(list)
for row in key:
    position_groups[(row["Question"], row["Condition"], row["Judge"])].append(row)
position_cases = Counter()
position_by_judge = defaultdict(Counter)
for (_, condition, judge), rows in position_groups.items():
    identities = {row["Selected identity"] for row in rows}
    if len(identities) > 1:
        case = "flipped"
    elif next(iter(identities)) == "pretender":
        case = "stable_pretender"
    else:
        case = "stable_human"
    position_cases[(condition, case)] += 1
    position_by_judge[judge][case] += 1

events_by_condition = defaultdict(Counter)
directions_by_justification = defaultdict(list)
for row in events:
    family = "style_form" if row["Cue code"] in STYLE else "substantive_practical"
    events_by_condition[row["Condition"]][family] += 1
    directions_by_justification[row["Blind ID"]].append(row["Signal direction"])

metrics = {
    "dataset": {
        "justifications": len(coding),
        "cue_events": len(events),
        "paired_condition_cells": len(paired),
        "original_swapped_pairs": len(position_groups),
    },
    "primary_cue_family": {},
    "mcnemar": {
        "style_to_nonstyle": style_to_nonstyle,
        "nonstyle_to_style": nonstyle_to_style,
        "exact_two_sided_p": exact_mcnemar_two_sided(style_to_nonstyle, nonstyle_to_style),
    },
    "pretender_selected_as_human": {},
    "position_cases_by_judge": {judge: dict(counts) for judge, counts in position_by_judge.items()},
    "cue_events_per_justification": {},
    "unspecified_only_justifications": {},
}

for condition in ("naive", "style_controlled"):
    total = sum(primary[condition].values())
    style_count = primary[condition]["style_form"]
    selected = selections[condition]["pretender"]
    calls = sum(selections[condition].values())
    metrics["primary_cue_family"][condition] = {
        "style_form": style_count,
        "substantive_practical": primary[condition]["substantive_practical"],
        "total": total,
        "style_form_share": style_count / total,
        "style_form_wilson_95": wilson(style_count, total),
    }
    metrics["pretender_selected_as_human"][condition] = {
        "selected": selected,
        "calls": calls,
        "share": selected / calls,
        "wilson_95": wilson(selected, calls),
    }
    metrics["cue_events_per_justification"][condition] = {
        family: count / total for family, count in events_by_condition[condition].items()
    }
    ids = [row["Blind ID"] for row in coding if row["Condition"] == condition]
    metrics["unspecified_only_justifications"][condition] = sum(
        set(directions_by_justification[blind_id]) == {"UNSPECIFIED"} for blind_id in ids
    )

OUTPUT.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(metrics, indent=2, sort_keys=True))
print(f"Wrote {OUTPUT.relative_to(ROOT)}")
