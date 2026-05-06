"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown.

    Includes latency, estimated cost, citation coverage, error status, and notes.
    """

    lines = [
        "# Benchmark Report",
        "",
        "| Run | Latency (s) | Cost (USD) | Citations | Errors | Notes |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in metrics:
        cost = f"${item.estimated_cost_usd:.4f}" if item.estimated_cost_usd else "$0.00"
        citations = f"{item.citation_coverage * 100:.1f}%" if item.citation_coverage else "0%"
        errors = "❌" if item.error_rate and item.error_rate > 0 else "✅"
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | "
            f"{citations} | {errors} | {item.notes} |"
        )
    return "\n".join(lines) + "\n"
