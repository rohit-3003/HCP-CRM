from sqlalchemy.orm import Session
from app.crud import crud
from app.schemas import schemas
from datetime import datetime, timedelta

def tool_schedule_followup(db: Session, entities: dict, current_interaction_id: int = None):
    """
    Schedules a follow-up task.
    """
    try:
        interaction_id = entities.get("interaction_id") or current_interaction_id
        if not interaction_id:
            return {"status": "error", "message": "Cannot schedule follow-up: No associated interaction found."}
            
        task_title = entities.get("task_title", "Follow-up meeting")
        
        # Simple date parsing logic (can be enhanced)
        date_str = entities.get("due_date")
        due_date = datetime.utcnow() + timedelta(days=7) # Default 1 week
        
        if date_str:
            if "tomorrow" in date_str.lower():
                due_date = datetime.utcnow() + timedelta(days=1)
            elif "next week" in date_str.lower():
                due_date = datetime.utcnow() + timedelta(days=7)
                
        task = schemas.TaskCreate(
            interaction_id=interaction_id,
            title=task_title,
            due_date=due_date
        )
        
        db_task = crud.create_task(db, task)
        return {
            "status": "success",
            "message": f"Scheduled task: '{task_title}' for {due_date.strftime('%Y-%m-%d')}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
