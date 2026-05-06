"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Analyze research notes and extract insights."""
        
        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.observability.tracing import trace_span
        from multi_agent_research_lab.services.llm_client import LLMClient
        
        with trace_span("analyst_run") as span:
            llm_client = LLMClient()

            system_prompt = (
                "You are a professional analyst. Extract key claims, compare "
                "viewpoints, and flag weak evidence from research notes."
            )
            user_prompt = f"Research Notes:\n{state.research_notes}"

            response = llm_client.complete(system_prompt, user_prompt)
            state.analysis_notes = response.content

            state.agent_results.append(
                AgentResult(
                    agent=AgentName.ANALYST,
                    content=response.content,
                    metadata={"cost": response.cost_usd},
                )
            )

            state.add_trace_event("analyst_complete", {})
            span["attributes"]["cost"] = response.cost_usd

        return state
