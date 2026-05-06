from unittest.mock import patch

import pytest

from multi_agent_research_lab.agents import AnalystAgent, ResearcherAgent, WriterAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMResponse


@pytest.fixture
def mock_llm_response() -> LLMResponse:
    return LLMResponse(
        content="Mocked LLM content",
        input_tokens=10,
        output_tokens=20,
        cost_usd=0.001,
    )


@patch("multi_agent_research_lab.services.llm_client.LLMClient.complete")
def test_researcher_agent_populates_state(mock_complete, mock_llm_response):
    mock_complete.return_value = mock_llm_response
    agent = ResearcherAgent()
    state = ResearchState(request=ResearchQuery(query="Test query"))
    
    new_state = agent.run(state)
    
    assert len(new_state.sources) > 0
    assert new_state.research_notes == "Mocked LLM content"
    assert len(new_state.agent_results) == 1
    assert new_state.agent_results[0].agent == "researcher"


@patch("multi_agent_research_lab.services.llm_client.LLMClient.complete")
def test_analyst_agent_populates_state(mock_complete, mock_llm_response):
    mock_complete.return_value = mock_llm_response
    agent = AnalystAgent()
    state = ResearchState(
        request=ResearchQuery(query="Test query"),
        research_notes="Existing research notes"
    )
    
    new_state = agent.run(state)
    
    assert new_state.analysis_notes == "Mocked LLM content"
    assert len(new_state.agent_results) == 1
    assert new_state.agent_results[0].agent == "analyst"


@patch("multi_agent_research_lab.services.llm_client.LLMClient.complete")
def test_writer_agent_populates_state(mock_complete, mock_llm_response):
    mock_complete.return_value = mock_llm_response
    agent = WriterAgent()
    state = ResearchState(
        request=ResearchQuery(query="Test query"),
        research_notes="Notes",
        analysis_notes="Analysis",
    )
    
    new_state = agent.run(state)
    
    assert new_state.final_answer == "Mocked LLM content"
    assert len(new_state.agent_results) == 1
    assert new_state.agent_results[0].agent == "writer"
