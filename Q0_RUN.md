# Running the Q0 Gate on macOS

## 1. Enter the project directory

Unzip the project, open Terminal, type `cd ` with a trailing space, drag the unzipped project folder into the Terminal window, and press Return.

## 2. Set the key for the current terminal session

```bash
read -s "OPENROUTER_API_KEY?Paste OpenRouter key: "
export OPENROUTER_API_KEY
echo
```

Do not paste the key into project files or commit it. Closing the terminal session removes this temporary environment variable.

## 3. Check the frozen local configuration

```bash
python3 scripts/q0_gate.py --check-config
```

This makes no API calls. It should report one Pretender, two Judges, and eight planned successful calls.

## 4. Run the gate

```bash
python3 scripts/q0_gate.py
```

The script performs two Pretender calls and six Judge calls. Retryable HTTP failures receive at most two retries with delays. Results are written immediately under a timestamped directory in `outputs/q0_gate/`.

The API key is never included in request records, manifests, raw responses, or summaries.

## 5. Inspect the summary

```bash
cat outputs/q0_gate/*/summary.json
```

The gate passes only when both Pretender calls complete and all six Judge outputs parse as JSON and satisfy the frozen three-field schema. A failed gate is retained rather than silently repaired.

Zip the timestamped output directory and upload it for review. Do not include terminal configuration files or any file containing an API key.
