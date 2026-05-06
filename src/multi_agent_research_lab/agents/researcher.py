"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Collect sources and summarize findings."""
        
        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.observability.tracing import trace_span
        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.services.search_client import SearchClient
        
        with trace_span("researcher_run", {"query": state.request.query}) as span:
            search_client = SearchClient()
            llm_client = LLMClient()
            
            # 1. Search
            sources = search_client.search(state.request.query)
            state.sources.extend(sources)
            
            # 2. Summarize findings
            source_text = "\n".join(f"- {s.title}: {s.snippet}" for s in sources)
            system_prompt = (
                "You are a professional researcher. Summarize provided sources "
                "into concise research notes."
            )
            user_prompt = f"Topic: {state.request.query}\n\nSources:\n{source_text}"

            response = llm_client.complete(system_prompt, user_prompt)
            state.research_notes = response.content

            # 3. Record result
            state.agent_results.append(
                AgentResult(
                    agent=AgentName.RESEARCHER,
                    content=response.content,
                    metadata={
                        "sources_found": len(sources),
                        "cost": response.cost_usd,
                    },
                )
            )

            state.add_trace_event(
                "researcher_complete",
                {"sources_count": len(sources)},
            )
            span["attributes"]["cost"] = response.cost_usd

        return state
