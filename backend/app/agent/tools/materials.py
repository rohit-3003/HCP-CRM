from sqlalchemy.orm import Session
from app.crud import crud

def tool_search_materials(db: Session, entities: dict):
    """
    Queries the seeded Materials table for relevant literature.
    """
    try:
        query = entities.get("material_topic") or entities.get("summary")
        if not query:
            return {"status": "success", "materials": []}
            
        # extract keywords
        keywords = ["cardiology", "diabetes", "hypertension", "study", "guide", "brochure", "oncology"]
        search_term = ""
        for k in keywords:
            if k in query.lower():
                search_term = k
                break
                
        if not search_term:
            search_term = query.split()[0] if query else ""
            
        materials = crud.search_materials(db, search_term)
        
        result = []
        for m in materials:
            result.append({
                "title": m.title,
                "category": m.category,
                "url": m.url
            })
            
        return {
            "status": "success",
            "materials": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
