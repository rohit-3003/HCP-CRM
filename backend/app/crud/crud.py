from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def get_hcp(db: Session, hcp_id: int):
    return db.query(models.HCP).filter(models.HCP.id == hcp_id).first()

def get_hcp_by_name(db: Session, name: str):
    words = name.replace(".", "").split()
    query = db.query(models.HCP)
    for word in words:
        if word.lower() not in ['dr', 'dr.']:
            query = query.filter(models.HCP.name.ilike(f"%{word}%"))
    return query.first()

def get_hcps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HCP).offset(skip).limit(limit).all()

def create_interaction(db: Session, interaction: schemas.InteractionCreate, raw_chat: str = None):
    db_interaction = models.Interaction(**interaction.model_dump(), raw_chat=raw_chat)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

def get_interactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Interaction).offset(skip).limit(limit).all()

def update_interaction(db: Session, interaction_id: int, update_data: dict):
    db_interaction = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
    if db_interaction:
        for key, value in update_data.items():
            setattr(db_interaction, key, value)
        db.commit()
        db.refresh(db_interaction)
    return db_interaction

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def search_materials(db: Session, query: str):
    # search title and description
    return db.query(models.Material).filter(
        (models.Material.title.ilike(f"%{query}%")) | 
        (models.Material.description.ilike(f"%{query}%")) |
        (models.Material.category.ilike(f"%{query}%"))
    ).all()

def get_analytics(db: Session):
    # Simple analytics for dashboard
    from datetime import datetime, date
    today = date.today()
    today_interactions = db.query(models.Interaction).filter(
        models.Interaction.interaction_date >= today
    ).count()
    
    pending_tasks = db.query(models.Task).filter(models.Task.status == "pending").count()
    
    # Positive sentiment %
    total_interactions = db.query(models.Interaction).count()
    positive = db.query(models.Interaction).filter(models.Interaction.sentiment.ilike("%positive%")).count()
    
    sentiment_pct = (positive / total_interactions * 100) if total_interactions > 0 else 0
    
    return {
        "today_visits": today_interactions,
        "interactions_this_week": total_interactions, # simplified
        "pending_followups": pending_tasks,
        "positive_sentiment_pct": round(sentiment_pct, 1)
    }
