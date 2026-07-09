from sqlalchemy.orm import Session
from app.crud import crud

def tool_edit_interaction(db: Session, entities: dict, current_interaction_id: int = None):
    """
    Modifies logged data based on contextual memory.
    """
    try:
        interaction_id = entities.get("interaction_id") or current_interaction_id
        
        if not interaction_id:
            return {"status": "error", "message": "Interaction ID not found in context or entities."}
            
        update_data = {}
        if "duration" in entities:
            update_data["duration"] = entities["duration"]
        if "summary" in entities:
            update_data["discussion_summary"] = entities["summary"]
        if "location" in entities:
            update_data["location"] = entities["location"]
            
        if not update_data:
            return {"status": "success", "message": "No valid fields to update found."}
            
        updated = crud.update_interaction(db, interaction_id, update_data)
        
        if updated:
            return {
                "status": "success",
                "message": f"Interaction {interaction_id} updated successfully.",
                "updated_fields": list(update_data.keys())
            }
        else:
            return {"status": "error", "message": f"Interaction {interaction_id} not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
