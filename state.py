from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    input: str
    intent: Optional[str]
    plan: Optional[str]
    memory: Optional[dict]

    search_query: Optional[str]
    search_results: Optional[str]
    step: Optional[str]