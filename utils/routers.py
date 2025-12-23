from typing import Literal
from langgraph.graph import END
from state import State

def router(state: State) -> Literal["brain_agent", "IngestionAgent" ,"AnalyticsAgent" ,"HealthQAgent" ,"END"]:
    """Router function to determine the next agent in the LangGraph pipeline."""
    next_agent = state.get("next_agent")

    if next_agent == "end" or state.get("task_complete", False):
        return END

    if next_agent in ["brain_agent", "IngestionAgent" ,"AnalyticsAgent" ,"HealthQAgent"]:
        return next_agent
    return "brain_agent"