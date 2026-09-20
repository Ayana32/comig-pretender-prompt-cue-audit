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

The questions, human anchors, prompt conditions, codebook v1, A/B presentation schedule, and core protocol were finalised before any model output was inspected. The following hash identifies that original freeze commit; the README line recording the hash necessarily appears in a later documentation commit:

```text
PRE_DRY_RUN_FREEZE_COMMIT: d4cb1f395d562d463c020b2593f17957ce7fab8a
```

The judge prompt and content-preservation form were subsequently frozen before Q0 model calls. The hash points to the tool-freeze commit; this hash record appears in the following documentation commit:

```text
PRE_Q0_TOOL_FREEZE_COMMIT: 6747f20d0f2710550f3f0ba0c19f1307a9d25b7b
```

Q0 and its anchor may be included in development diagnostics, but Q0 is always displayed separately from the eight-item main results and excluded from main summary statistics.

## Reproducibility limitation

The planned implementation uses free access tiers. Model aliases, backend providers, rate limits, and availability may change over time, so exact reproduction is not guaranteed even when the exposed model identifiers and access dates are recorded.

Judge justifications are constrained to 2 to 4 sentences and approximately 40 to 100 words to limit between-model output variation. Consequently, reported cue frequencies reflect only the cues judges chose to verbalise within that budget, not every cue they may have used internally.

## Current status

Pre-dry-run design frozen. Model-access validation and Q0 dry run are pending.
