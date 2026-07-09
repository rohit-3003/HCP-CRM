from sqlalchemy.orm import Session
from app.crud import crud

def tool_get_hcp_profile(db: Session, entities: dict):
    """
    Retrieves detailed background info on an HCP.
    """
    try:
        name = entities.get("hcp_name")
        if not name:
            return {"status": "error", "message": "HCP name not provided for search."}
            
        hcp = crud.get_hcp_by_name(db, name)
        
        if hcp:
            return {
                "status": "success",
                "hcp": {
                    "id": hcp.id,
                    "name": hcp.name,
                    "speciality": hcp.speciality,
                    "hospital": hcp.hospital,
                    "city": hcp.city,
                    "preferred_contact": hcp.preferred_contact
                }
            }
        else:
            return {"status": "error", "message": f"HCP '{name}' not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
