# Model Access Log

## 2026-09-20 — Initial Pretender candidate rejected

Initial request ID: `qwen/qwen3.8-27b:free`  
Catalog canonical slug observed: `qwen/qwen3.8-27b-20260814`

Two separately timed Q0 runs were reported:

| Local run directory timestamp | Target call | Attempts | Outcome |
|---|---|---:|---|
| `20260920T202021Z` | `pretender__naive` | 3 | HTTP 429 on all attempts |
| `20260920T204222Z` | `pretender__naive` | 3 | HTTP 429 on all attempts |

The provider metadata identified an upstream shared-pool rate limit from ModelRun. The failure occurred before any Pretender response or Judge call was obtained. The candidate was therefore rejected for access instability in this free-tier pilot, not for model quality.

## Replacement candidate

Replacement request ID: `z-ai/glm-5.2:free`  
Catalog canonical slug observed: `z-ai/glm-5.2-20260616`

GLM remains a candidate until it completes both Q0 Pretender conditions. Judge candidates remain unchanged. If GLM also fails the access gate, that failure will be retained and a further replacement will require another documented protocol update.
