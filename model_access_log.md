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
