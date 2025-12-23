from typing import TypedDict, Optional, Dict, Any


class State(TypedDict):
    """
    Shared state across all agents in the LangGraph pipeline.
    This is the single source of truth for agent communication.
    """

    user_query: str
    sidebar_input: Dict[str, Any]
    user_id: Optional[str]

    next_agent: str
    task_complete: bool

    final_response: Optional[str]