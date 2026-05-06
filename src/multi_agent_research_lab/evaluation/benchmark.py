"""Benchmark skeleton for single-agent vs multi-agent."""

import re
from collections.abc import Callable
from time import perf_counter

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState

Runner = Callable[[str], ResearchState]


def run_benchmark(
    run_name: str,
    query: str,
    runner: Runner,
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency, cost, quality, and citation coverage."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started

    # Calculate Cost
    total_cost = sum(res.metadata.get("cost", 0.0) for res in state.agent_results)

    # Calculate Citation Coverage (basic heuristic: count [Source X] in final answer)
    citations = set(re.findall(r"\[Source \d+\]", state.final_answer or ""))
    citation_coverage = len(citations) / max(len(state.sources), 1)
    
    # Error rate
    error_rate = 1.0 if state.errors else 0.0
    
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=total_cost,
        citation_coverage=citation_coverage,
        error_rate=error_rate,
        notes=f"Iterations: {state.iteration}",
    )
    
    return state, metrics
