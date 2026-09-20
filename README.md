# COMIG Pretender Prompt and Cue Audit

## Motivation

COMIG organisers construct the prompt used by the LLM Pretender. If that prompt systematically produces surface artifacts, identification may rely on stylistic shortcuts rather than evidence of domain competence. This project audits that risk before involving participants and prepares a transparent cue-coding scheme for later human validation.

## Research question

> Before exposing participants to COMIG, does the organiser's pretender prompt introduce surface artifacts that could shortcut identification, and can those cues be captured with a transparent coding scheme for later human validation?

## What this pilot does

- Compares a paper-inspired naive prompt with a style-controlled prompt.
- Uses three generations per question and condition to observe run-to-run variation.
- Extracts surface features from all generated responses.
- Checks whether style control also changes substantive content.
- Audits LLM-judge justifications using a pre-specified qualitative codebook.

## What this pilot does not do

- Estimate human identification accuracy.
- Claim that human judges use the same cues as LLM judges.
- Treat one researcher's anchors as representative of a social world.
- Treat the anchors as gold-standard expert answers.
- Treat manual or automated coding as ground truth.

## Pre-generation freeze

The questions, human anchors, prompt conditions, codebook v1, A/B presentation schedule, and core protocol were finalised before any model output was inspected. The pre-dry-run freeze commit is recorded in the following documentation commit:

```text
PRE_DRY_RUN_FREEZE_COMMIT: to_be_recorded_after_first_commit
```

## Reproducibility limitation

The planned implementation uses free access tiers. Model aliases, backend providers, rate limits, and availability may change over time, so exact reproduction is not guaranteed even when the exposed model identifiers and access dates are recorded.

## Current status

Pre-dry-run design frozen. Model-access validation and Q0 dry run are pending.

