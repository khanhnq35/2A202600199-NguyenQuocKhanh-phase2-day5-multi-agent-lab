"""LangGraph workflow skeleton."""

from typing import Any, Protocol, cast

from multi_agent_research_lab.core.state import ResearchState


class RunnableGraph(Protocol):
    """Minimal protocol for compiled LangGraph app."""

    def invoke(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Invoke compiled graph and return final state mapping."""


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> RunnableGraph:
        """Create a LangGraph graph."""
        from langgraph.graph import END, START, StateGraph

        from multi_agent_research_lab.agents import (
            AnalystAgent,
            ResearcherAgent,
            SupervisorAgent,
            WriterAgent,
        )

        # Initialize agents
        supervisor = SupervisorAgent()
        researcher = ResearcherAgent()
        analyst = AnalystAgent()
        writer = WriterAgent()

        # Create Graph
        builder = StateGraph(ResearchState)

        # Add Nodes
        builder.add_node("supervisor", supervisor.run)
        builder.add_node("researcher", researcher.run)
        builder.add_node("analyst", analyst.run)
        builder.add_node("writer", writer.run)

        # Set Entry Point
        builder.add_edge(START, "supervisor")

        # Add Conditional Edges
        def route(state: ResearchState) -> str:
            next_step = state.route_history[-1] if state.route_history else "supervisor"
            if next_step == "done":
                return END
            return next_step

        builder.add_conditional_edges(
            "supervisor",
            route,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                END: END
            }
        )

        # Edges back to supervisor
        builder.add_edge("researcher", "supervisor")
        builder.add_edge("analyst", "supervisor")
        builder.add_edge("writer", "supervisor")

        return cast(RunnableGraph, builder.compile())

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        # langgraph's invoke returns the final state dict
        # we need to cast or update our Pydantic object
        final_state_dict = app.invoke(state.model_dump())
        return ResearchState(**final_state_dict)
