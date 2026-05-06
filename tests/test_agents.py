
from multi_agent_research_lab.agents import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState


def test_supervisor_routing_logic() -> None:
    """Test that supervisor correctly routes based on state."""
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    
    # 1. Start: should route to researcher
    new_state = SupervisorAgent().run(state)
    assert new_state.route_history[-1] == "researcher"
    
    # 2. After research: should route to analyst
    new_state.research_notes = "Some research notes"
    new_state = SupervisorAgent().run(new_state)
    assert new_state.route_history[-1] == "analyst"
    
    # 3. After analysis: should route to writer
    new_state.analysis_notes = "Some analysis"
    new_state = SupervisorAgent().run(new_state)
    assert new_state.route_history[-1] == "writer"
    
    # 4. After final answer: should be done
    new_state.final_answer = "Final answer"
    new_state = SupervisorAgent().run(new_state)
    assert new_state.route_history[-1] == "done"


def test_supervisor_max_iterations_guard() -> None:
    """Test that supervisor stops after reaching max iterations."""
    from multi_agent_research_lab.core.config import get_settings
    settings = get_settings()
    
    state = ResearchState(request=ResearchQuery(query="Test iterations"))
    state.iteration = settings.max_iterations
    
    new_state = SupervisorAgent().run(state)
    assert new_state.route_history[-1] == "done"
    assert new_state.trace[-1]["payload"]["reason"] == "max_iterations_reached"
