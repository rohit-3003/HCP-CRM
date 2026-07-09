from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import crud
from app.schemas import schemas
from app.agent.graph import app as agent_app
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter()

# In-memory session storage for simplicity in this assignment
# In production, this would be Redis or the database
sessions = {}

@router.post("/chat")
def chat_with_agent(chat_req: schemas.ChatRequest):
    session_id = chat_req.session_id
    
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "current_interaction": {},
            "execution_steps": []
        }
        
    state = {
        "messages": sessions[session_id]["messages"],
        "user_input": chat_req.message,
        "current_interaction": sessions[session_id]["current_interaction"],
        "execution_steps": [],
        "tool_results": []
    }
    
    # Run the graph
    try:
        result = agent_app.invoke(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # Update session
    sessions[session_id]["messages"] = result.get("messages", [])
    sessions[session_id]["current_interaction"] = result.get("current_interaction", {})
    
    return {
        "response": result.get("final_response"),
        "intent": result.get("intent"),
        "entities": result.get("entities"),
        "sentiment": result.get("sentiment"),
        "missing_fields": result.get("missing_fields"),
        "confidence_scores": result.get("confidence_scores"),
        "execution_steps": result.get("execution_steps")
    }

@router.get("/hcps", response_model=list[schemas.HCP])
def get_hcps(db: Session = Depends(get_db)):
    return crud.get_hcps(db)

@router.get("/interactions", response_model=list[schemas.Interaction])
def get_interactions(db: Session = Depends(get_db)):
    return crud.get_interactions(db)

@router.post("/interactions", response_model=schemas.Interaction)
def log_manual_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, interaction)

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    return crud.get_analytics(db)
