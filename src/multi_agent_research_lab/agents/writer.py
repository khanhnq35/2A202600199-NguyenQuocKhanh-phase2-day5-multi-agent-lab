"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Synthesize final answer from notes."""
        
        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.observability.tracing import trace_span
        from multi_agent_research_lab.services.llm_client import LLMClient
        
        with trace_span("writer_run") as span:
            llm_client = LLMClient()

            system_prompt = (
                "You are a professional writer. Synthesize a clear, structured "
                "response from research and analysis notes. Include citations "
                "or references to provided sources."
            )
            user_prompt = (
                f"Research Notes:\n{state.research_notes}\n\n"
                f"Analysis:\n{state.analysis_notes}\n\n"
                f"Sources:\n{state.sources}"
            )

            response = llm_client.complete(system_prompt, user_prompt)
            state.final_answer = response.content

            state.agent_results.append(
                AgentResult(
                    agent=AgentName.WRITER,
                    content=response.content,
                    metadata={"cost": response.cost_usd},
                )
            )

            state.add_trace_event("writer_complete", {})
            span["attributes"]["cost"] = response.cost_usd

        return state
