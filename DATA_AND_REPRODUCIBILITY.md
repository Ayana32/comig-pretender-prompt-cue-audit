# Data and reproducibility

## Directory map

| Path | Role |
|---|---|
| `data/raw/main_generation/20260922T173531Z/` | 48 Pretender API outputs, call records, manifest, and run summary |
| `data/raw/judge_audit/20260923T182840Z/` | 64 Judge API outputs, call records, manifest, and run summary |
| `data/processed/main/` | Surface features, condition summaries, content checks, and generation QA |
| `data/processed/judge_audit/` | Position-case table and structural QA |
| `results/COMIG_blind_justification_coding.xlsx` | Canonical coded workbook and formatted results summary |
| `results/csv/` | Machine-readable exports of the final workbook |
| `results/reproduced_metrics.json` | Headline statistics recalculated from the CSV exports |

## Recalculate headline statistics

The public results can be checked without an API key or third-party Python package:

```bash
python3 scripts/reproduce_statistics.py
```

The script joins final coding with the unblinding key and recalculates:

- sample sizes;
- primary cue-family counts;
- Wilson confidence intervals;
- exact two-sided McNemar result;
- Pretender-as-human selections;
- original–swapped stability by Judge;
- cue events per justification; and
- `UNSPECIFIED`-only justification counts.

## Repeat model calls

Set `OPENROUTER_API_KEY` in the shell. Never commit the key. Then follow the generation and Judge commands in `RUNNING.md`. Repeating the calls incurs API costs and may not yield identical text because sampling is stochastic and provider routing or aliases may change.

## Data boundaries

The repository contains model outputs and the researcher's fixed anchors. It contains no external participant data, credentials, or sensitive personal information. The unblinding key is public because coding was completed before unblinding and no participant identities exist in this pilot.

## Reproducibility levels

- **Result reproduction:** supported from the committed CSV files.
- **Pipeline reproduction:** supported by the committed scripts and frozen prompts.
- **Exact output reproduction:** not guaranteed because seeds were unsupported and hosted endpoints can change.
