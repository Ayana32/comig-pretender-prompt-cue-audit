# Running the pipeline

These steps repeat the model calls. They need an OpenRouter API key and incur API costs. To check the published statistics without an API key, run `python3 scripts/reproduce_statistics.py` instead.

Set the key for the current shell session only. Never write it to a file or commit it.

```bash
read -s "OPENROUTER_API_KEY?Paste OpenRouter key: "
export OPENROUTER_API_KEY
```

Repeated calls may not reproduce identical text: seeds were unsupported, sampling is stochastic, and hosted endpoints can change.

## Main generation

Validate the frozen configuration without making an API call:

```bash
python3 scripts/generate_main.py --check-config
```

Generate the 48 main responses. Each call is saved immediately under a new timestamped directory in `outputs/main_generation/`:

```bash
python3 scripts/generate_main.py
```

If the run is interrupted or any calls fail, resume the same directory rather than starting a new experiment:

```bash
python3 scripts/generate_main.py --run-dir outputs/main_generation/TIMESTAMP
```

The generation gate passes when `summary.json` reports `completed_calls: 48`, no missing or unexpected call IDs, and all observed `finish_reason` values are recorded. A `length` finish reason is retained and flagged; that response is excluded only from word-count and mean-sentence-length condition summaries.

After generation, build the 48-response feature table, all-nine-anchor feature table, question-level condition summaries, completeness QA, and the prefilled run-1 content-check worksheet:

```bash
python3 scripts/analyse_generation.py outputs/main_generation/TIMESTAMP
```

The analysis is written to `analysis/main/TIMESTAMP/`. Complete `content_check_run1.md` manually using the frozen rules in `content_check.md`; confounded pairs are marked, not regenerated or removed.

## Judge audit

Validate the 16 designated-run inputs and frozen 64-call configuration without
making an API call:

```bash
python3 scripts/run_judge_audit.py \
  outputs/main_generation/GENERATION_TIMESTAMP \
  --check-config
```

Run the audit. Raw outputs are saved after every call; a failed endpoint does
not stop later cells:

```bash
python3 scripts/run_judge_audit.py \
  outputs/main_generation/GENERATION_TIMESTAMP
```

If interrupted or if API failures remain, resume the exact Judge run directory:

```bash
python3 scripts/run_judge_audit.py \
  outputs/main_generation/GENERATION_TIMESTAMP \
  --run-dir outputs/judge_audit/JUDGE_TIMESTAMP
```

After all calls, generate structural QA without displaying justification text:

```bash
python3 scripts/analyse_judge_audit.py \
  outputs/judge_audit/JUDGE_TIMESTAMP
```

The output under `analysis/judge_audit/JUDGE_TIMESTAMP/` compares the selected
underlying response identity across original and swapped orders. A flipped pair
is consistent with position sensitivity but cannot separate position effects
from run-to-run model variability when each order is called once. Cue coding is
a later, separately blinded manual stage.
