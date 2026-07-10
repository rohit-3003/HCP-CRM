import json
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from app.agent.state import AgentState
from app.agent.prompts.prompts import INTENT_DETECTION_PROMPT, ENTITY_EXTRACTION_PROMPT, RESPONSE_PROMPT
from app.core.config import settings

# Instantiate globally to prevent connection pool memory leaks
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGroq(model="llama-3.1-8b-instant", api_key=settings.GROQ_API_KEY)
    return _llm_instance

def detect_intent_node(state: AgentState):
    llm = get_llm()
    history = "\n".join([m.content for m in state.get("messages", [])[-5:]])
    prompt = INTENT_DETECTION_PROMPT.format(user_input=state["user_input"], history=history)
    
    response = llm.invoke(prompt)
    intent = response.content.strip().replace("'", "").replace('"', "")
    
    # basic validation
    valid_intents = ['log_interaction', 'edit_interaction', 'get_hcp_profile', 'schedule_followup', 'general_chat']
    if intent not in valid_intents:
        intent = "general_chat"
        
    state["intent"] = intent
    state["execution_steps"] = state.get("execution_steps", []) + [f"Detect Intent: {intent}"]
    return state

def extract_entities_node(state: AgentState):
    llm = get_llm()
    # use JSON mode if supported, or prompt heavily for JSON
    history = "\n".join([m.content for m in state.get("messages", [])[-5:]])
    prompt = ENTITY_EXTRACTION_PROMPT.format(intent=state["intent"], user_input=state["user_input"], history=history)
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # clean up markdown code blocks if any
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]
        
    try:
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx:end_idx+1]
            entities = json.loads(json_str)
        else:
            entities = json.loads(content)
    except json.JSONDecodeError:
        entities = {}
        
    state["entities"] = entities
    state["sentiment"] = entities.get("sentiment", "Neutral")
    state["ai_summary"] = entities.get("summary", "")
    state["missing_fields"] = entities.get("missing_fields", [])
    state["confidence_scores"] = entities.get("confidence_scores", {})
    state["execution_steps"] = state.get("execution_steps", []) + ["Extract Entities"]
    return state

def tool_router(state: AgentState):
    return state["intent"]

def response_node(state: AgentState):
    llm = get_llm()
    results = "\n".join([str(r) for r in state.get("tool_results", [])])
    prompt = RESPONSE_PROMPT.format(tool_results=results, user_input=state["user_input"])
    
    response = llm.invoke(prompt)
    state["final_response"] = response.content
    state["messages"] = state.get("messages", []) + [HumanMessage(content=state["user_input"]), response]
    state["execution_steps"] = state.get("execution_steps", []) + ["Generate Response"]
    return state
