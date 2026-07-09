from typing import TypedDict, Annotated, List, Dict, Any
import operator
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    user_input: str
    intent: str
    entities: Dict[str, Any]
    tool_results: List[Dict[str, Any]]
    execution_steps: List[str]
    current_interaction: Dict[str, Any]
    ai_summary: str
    sentiment: str
    missing_fields: List[str]
    confidence_scores: Dict[str, float]
    final_response: str
