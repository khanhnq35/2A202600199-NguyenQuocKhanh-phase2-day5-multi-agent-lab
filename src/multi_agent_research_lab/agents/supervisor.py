"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Decide the next step based on current state."""
        
        # Guardrail: Check iterations
        from multi_agent_research_lab.core.config import get_settings
        settings = get_settings()
        
        if state.iteration >= settings.max_iterations:
            state.record_route("done")
            state.add_trace_event(
                "supervisor_decision",
                {"next": "done", "reason": "max_iterations_reached"},
            )
            return state

        # Routing Logic
        next_agent = "done"
        reason = "all_tasks_completed"

        if not state.research_notes:
            next_agent = "researcher"
            reason = "missing_research_notes"
        elif not state.analysis_notes:
            next_agent = "analyst"
            reason = "missing_analysis_notes"
        elif not state.final_answer:
            next_agent = "writer"
            reason = "missing_final_answer"
        
        state.record_route(next_agent)
        state.add_trace_event("supervisor_decision", {"next": next_agent, "reason": reason})
        
        return state
