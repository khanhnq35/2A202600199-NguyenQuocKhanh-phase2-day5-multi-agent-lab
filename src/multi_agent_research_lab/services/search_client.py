"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents using Tavily or Mock fallback."""
        
        from multi_agent_research_lab.core.config import get_settings
        settings = get_settings()
        
        if settings.tavily_api_key:
            import requests  # type: ignore[import-untyped]
            try:
                response = requests.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": settings.tavily_api_key,
                        "query": query,
                        "max_results": max_results,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                
                return [
                    SourceDocument(
                        title=result["title"],
                        url=result["url"],
                        snippet=result["content"]
                    )
                    for result in data.get("results", [])
                ]
            except Exception as exc:
                import logging

                logging.error("Tavily search failed: %s. Falling back to mock.", exc)

        # Mock fallback
        return [
            SourceDocument(
                title=f"Understanding {query}",
                url=f"https://example.com/research/{query.lower().replace(' ', '-')}",
                snippet=(
                    f"This is a comprehensive guide about {query}. It covers "
                    "state-of-the-art techniques and future directions."
                ),
            ),
            SourceDocument(
                title="Multi-Agent Systems: A Survey",
                url="https://example.com/mas-survey",
                snippet=(
                    "Survey of multi-agent architectures including "
                    "supervisor-worker patterns and hierarchical swarms."
                ),
            ),
        ]
