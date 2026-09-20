# Model Access Log

## 2026-09-20 — Initial Pretender candidate temporarily unavailable

Initial request ID: `qwen/qwen3.8-27b:free`  
Catalog canonical slug observed: `qwen/qwen3.8-27b-20260814`

Two separately timed Q0 runs were reported:

| Local run directory timestamp | Target call | Attempts | Outcome |
|---|---|---:|---|
| `20260920T202021Z` | `pretender__naive` | 3 | HTTP 429 on all attempts |
| `20260920T204222Z` | `pretender__naive` | 3 | HTTP 429 on all attempts |

The provider metadata identified an upstream shared-pool rate limit from ModelRun. Both runs occurred in the same evening and used short in-run retry intervals of 10 and 30 seconds. This does not establish persistent endpoint instability, so Qwen remains the candidate pending one separately timed retry several hours later or the next morning.

## Backup candidate — not activated

Replacement request ID: `z-ai/glm-5.2:free`  
Catalog canonical slug observed: `z-ai/glm-5.2-20260616`

GLM is recorded only as a backup and has not replaced Qwen. A replacement decision will be made only after the separately timed Qwen retry. Judge candidates remain unchanged and are tested independently even when the Pretender endpoint fails.

## 2026-09-20 — Independent endpoint diagnostic

Local run directory: `20260920T205014Z`

| Endpoint | Outcome |
|---|---|
| Qwen naive | HTTP 200, but `message.content` was not a string; the old runner failed to retain the raw response after extraction failure |
| Qwen style-controlled | First attempt HTTP 429; second attempt HTTP 200; 41-word visible answer; 799 reasoning tokens; `finish_reason: stop` |
| Gemma Judge | 0/3 calls completed; all exhausted retries with upstream shared-pool HTTP 429 |
| Nemotron Judge | 3/3 calls completed; 3/3 exact-JSON parse and schema validation success |

Because the live naive response was unavailable, both Judges were probed with the frozen diagnostic fixture. Nemotron selected B on all three calls with confidence 88, 80, and 80. These selections are not study findings: the fixture was designed only to exercise the endpoint and schema and is excluded from cue coding and identification analysis.

The run exposed a cross-model configuration problem. Qwen and Nemotron returned substantial reasoning fields, while Gemma's catalog default has reasoning disabled. OpenRouter documents that reasoning tokens usually count against `max_tokens` and can leave empty content. Protocol v1.1 therefore disables reasoning explicitly for all Pretender and Judge calls and reruns Q0. The runner also now retains a raw API response when content extraction or validation fails.
