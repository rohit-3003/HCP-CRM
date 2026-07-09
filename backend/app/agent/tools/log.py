from sqlalchemy.orm import Session
from app.crud import crud
from app.schemas import schemas
from datetime import datetime

def tool_log_interaction(db: Session, entities: dict, raw_chat: str):
    """
    Captures interaction data.
    """
    try:
        hcp_id = entities.get("hcp_id")
        duration = entities.get("duration", 15)
        summary = entities.get("summary", "No summary provided.")
        sentiment = entities.get("sentiment", "Neutral")
        location = entities.get("location", "Clinic")

        if not hcp_id:
            # Try finding HCP by name if ID isn't present
            name = entities.get("hcp_name")
            if name:
                hcp = crud.get_hcp_by_name(db, name)
                if hcp:
                    hcp_id = hcp.id
        
        if not hcp_id:
            return {"status": "error", "message": f"HCP not found or not specified (name searched: {entities.get('hcp_name')})"}

        interaction = schemas.InteractionCreate(
            hcp_id=hcp_id,
            duration=duration,
            location=location,
            discussion_summary=summary,
            sentiment=sentiment,
            status="completed"
        )
        
        db_interaction = crud.create_interaction(db, interaction, raw_chat=raw_chat)
        
        return {
            "status": "success",
            "interaction_id": db_interaction.id,
            "message": f"Interaction logged successfully with ID {db_interaction.id}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
