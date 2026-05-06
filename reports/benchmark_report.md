# Benchmark Report

| Run | Latency (s) | Cost (USD) | Citations | Errors | Notes |
|---|---:|---:|---:|---:|---|
| Baseline Q1 | 18.96 | $0.0008 | 0% | ✅ | Iterations: 0 |
| Multi-Agent Q1 | 45.15 | $0.0024 | 0% | ✅ | Iterations: 4 |
| Baseline Q2 | 20.48 | $0.0008 | 0% | ✅ | Iterations: 0 |
| Multi-Agent Q2 | 49.84 | $0.0027 | 80.0% | ✅ | Iterations: 4 |
| Baseline Q3 | 18.05 | $0.0007 | 0% | ✅ | Iterations: 0 |
| Multi-Agent Q3 | 47.34 | $0.0027 | 0% | ✅ | Iterations: 4 |

## Failure Mode Analysis

| Failure mode | Observed risk | Mitigation |
|---|---|---|
| Citation format mismatch | Q1 and Q3 multi-agent produced valid answers but citation coverage is 0% because heuristic only counts `[Source X]`. | Standardize Writer prompt to always use `[Source N]` citations and improve parser. |
| Higher latency | Multi-agent latency is ~2.3x baseline due to Researcher → Analyst → Writer sequence. | Use parallel retrieval, smaller prompts, caching, or skip Analyst for simple queries. |
| Higher cost | Multi-agent cost is ~3x baseline due to multiple LLM calls. | Add routing policy to choose baseline for simple queries and multi-agent for complex ones. |
| Search dependency | Tavily/API/network failure can break grounding. | Keep mock fallback and log whether source is real or fallback. |
| Supervisor loop | Incorrect state update can cause repeated routing. | `MAX_ITERATIONS=6` stops loop and tests verify guard behavior. |
| Trace upload failure | LangSmith may fail if DNS/network unavailable. | Export local JSON trace to `reports/traces/benchmark_traces.json`. |

## Trace Export

Local trace JSON was exported to:

```text
reports/traces/benchmark_traces.json
```
