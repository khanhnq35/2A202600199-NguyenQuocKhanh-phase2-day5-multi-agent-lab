"""Optional critic agent for final answer validation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append lightweight review findings."""

        final_answer = state.final_answer or ""
        cited_sources = 0
        for source in state.sources:
            if source.url and source.url in final_answer:
                cited_sources += 1
        citation_coverage = cited_sources / max(len(state.sources), 1)
        finding = {
            "has_final_answer": bool(final_answer.strip()),
            "source_count": len(state.sources),
            "citation_coverage": citation_coverage,
        }

        if not final_answer.strip():
            state.errors.append("Critic found missing final answer.")

        state.add_trace_event("critic_review", finding)
        return state
