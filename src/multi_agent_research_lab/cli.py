"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a real single-agent baseline."""

    _init()
    from multi_agent_research_lab.services.llm_client import LLMClient

    request = ResearchQuery(query=query)
    state = ResearchState(request=request)

    client = LLMClient()
    system_prompt = (
        "You are a helpful research assistant. Provide a comprehensive "
        "summary based on the query."
    )

    with console.status("[bold green]Agent working..."):
        response = client.complete(system_prompt, query)
        state.final_answer = response.content
        
        # Log metrics to trace
        state.add_trace_event("baseline_completion", {
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "cost_usd": response.cost_usd
        })

    console.print(Panel(state.final_answer, title="Single-Agent Baseline (Gemini)"))
    console.print(
        "[dim]Cost: "
        f"${response.cost_usd:.6f} | Tokens: {response.input_tokens or 0} in / "
        f"{response.output_tokens or 0} out[/dim]"
    )


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    try:
        result = workflow.run(state)
    except StudentTodoError as exc:
        console.print(Panel.fit(str(exc), title="Expected TODO", style="yellow"))
        raise typer.Exit(code=2) from exc
    console.print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
