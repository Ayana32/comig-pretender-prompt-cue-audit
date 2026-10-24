#!/usr/bin/env python3
"""Extract transparent surface features from an ID-to-text JSON object."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


HEDGES = {
    "approximately", "appear", "appears", "could", "generally", "likely",
    "may", "might", "often", "perhaps", "possibly", "potential", "potentially",
    "seem", "seems", "suggest", "suggests", "tend", "typically",
}
FIRST_PERSON = {"i", "i'd", "i’ll", "i'm", "i’ve", "me", "my", "mine", "we", "our", "ours", "us"}
DISCOURSE_MARKERS = {
    "also", "alternatively", "first", "furthermore", "however", "instead",
    "last", "moreover", "overall", "second", "then", "therefore", "thus",
}


def tokens(text: str) -> list[str]:
    return re.findall(r"\b[\w’'-]+\b", text.lower(), flags=re.UNICODE)


def sentence_count(text: str) -> int:
    chunks = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip())]
    return sum(bool(part) for part in chunks)


def paragraph_count(text: str) -> int:
    return len([part for part in re.split(r"\n\s*\n", text.strip()) if part.strip()])


def list_item_count(text: str) -> int:
    pattern = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", re.MULTILINE)
    return len(pattern.findall(text))


def heading_count(text: str) -> int:
    markdown = re.compile(r"^\s*#{1,6}\s+\S", re.MULTILINE)
    standalone_bold = re.compile(r"^\s*\*\*[^*]+\*\*\s*$", re.MULTILINE)
    return len(markdown.findall(text)) + len(standalone_bold.findall(text))


def count_lexicon(items: list[str], lexicon: set[str]) -> int:
    return sum(item in lexicon for item in items)


def extract(item_id: str, text: str) -> dict[str, object]:
    word_items = tokens(text)
    words = len(word_items)
    sentences = sentence_count(text)
    commas = text.count(",")
    first_person = count_lexicon(word_items, FIRST_PERSON)
    discourse_markers = count_lexicon(word_items, DISCOURSE_MARKERS)
    return {
        "text_id": item_id,
        "word_count": words,
        "sentence_count": sentences,
        "mean_sentence_length": round(words / sentences, 3) if sentences else None,
        "list_item_count": list_item_count(text),
        "heading_count": heading_count(text),
        "paragraph_count": paragraph_count(text),
        "comma_count": commas,
        "comma_density_per_100_words": round(100 * commas / words, 3) if words else None,
        "hedge_count": count_lexicon(word_items, HEDGES),
        "hedge_density_per_100_words": round(
            100 * count_lexicon(word_items, HEDGES) / words, 3
        ) if words else None,
        "first_person_count": first_person,
        "first_person_density_per_100_words": round(
            100 * first_person / words, 3
        ) if words else None,
        "discourse_marker_count": discourse_markers,
        "discourse_marker_density_per_100_words": round(
            100 * discourse_markers / words, 3
        ) if words else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path, help="JSON object mapping text IDs to strings")
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in data.items()
    ):
        raise ValueError("input must be a JSON object mapping string IDs to string texts")

    rows = [extract(item_id, text) for item_id, text in data.items()]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
