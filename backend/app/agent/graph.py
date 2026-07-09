from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes.nodes import detect_intent_node, extract_entities_node, tool_router, response_node
from app.agent.tools.log import tool_log_interaction
from app.agent.tools.edit import tool_edit_interaction
from app.agent.tools.hcp import tool_get_hcp_profile
from app.agent.tools.followup import tool_schedule_followup
from app.agent.tools.materials import tool_search_materials
from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
        
def execute_tool_node(state: AgentState):
    intent = state["intent"]
    entities = state.get("entities", {})
    user_input = state["user_input"]
    db = get_db()
    
    result = {}
    try:
        if intent == "log_interaction":
            result = tool_log_interaction(db, entities, raw_chat=user_input)
            if result.get("status") == "success":
                state["current_interaction"] = {"id": result.get("interaction_id")}
                
            # If they also wanted to follow up, maybe extract that (bonus point, but let's stick to one main tool per intent for simplicity, or we can check entities)
            if entities.get("task_title") or entities.get("due_date"):
                followup_res = tool_schedule_followup(db, entities, current_interaction_id=result.get("interaction_id"))
                result["followup"] = followup_res
                
        elif intent == "edit_interaction":
            current_id = state.get("current_interaction", {}).get("id")
            result = tool_edit_interaction(db, entities, current_interaction_id=current_id)
            
        elif intent == "get_hcp_profile":
            result = tool_get_hcp_profile(db, entities)
            
        elif intent == "schedule_followup":
            current_id = state.get("current_interaction", {}).get("id")
            result = tool_schedule_followup(db, entities, current_interaction_id=current_id)
            
        # Optional: check if they discussed something that needs materials
        if entities.get("material_topic"):
            mat_res = tool_search_materials(db, entities)
            if mat_res.get("materials"):
                result["suggested_materials"] = mat_res["materials"]
                
    finally:
        db.close()
        
    state["tool_results"] = state.get("tool_results", []) + [result]
    state["execution_steps"] = state.get("execution_steps", []) + [f"Execute Tool: {intent}"]
    return state


# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("detect_intent", detect_intent_node)
workflow.add_node("extract_entities", extract_entities_node)
workflow.add_node("execute_tool", execute_tool_node)
workflow.add_node("generate_response", response_node)

workflow.add_edge(START, "detect_intent")
workflow.add_edge("detect_intent", "extract_entities")

workflow.add_conditional_edges(
    "extract_entities",
    tool_router,
    {
        "log_interaction": "execute_tool",
        "edit_interaction": "execute_tool",
        "get_hcp_profile": "execute_tool",
        "schedule_followup": "execute_tool",
        "general_chat": "generate_response"
    }
)

workflow.add_edge("execute_tool", "generate_response")
workflow.add_edge("generate_response", END)

app = workflow.compile()
