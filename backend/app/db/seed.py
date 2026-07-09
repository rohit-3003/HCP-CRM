from sqlalchemy.orm import Session
from app.db.database import engine, Base
from app.models.models import HCP, Material

def seed_db():
    import time
    from sqlalchemy.exc import OperationalError
    max_retries = 5
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError as e:
            print(f"Database not ready, retrying in 3 seconds... ({i+1}/{max_retries})")
            time.sleep(3)
    else:
        print("Failed to connect to the database after multiple retries.")
        return
    with Session(engine) as session:
        # Check if already seeded
        if session.query(HCP).first():
            print("Database already seeded.")
            return

        print("Seeding database...")
        
        # Seed HCPs
        hcps = [
            HCP(name="Dr. Priya Sharma", speciality="Cardiology", hospital="Apollo Hospital", city="New Delhi", phone="+91 9876543210", email="priya.sharma@apollo.in", preferred_contact="Email"),
            HCP(name="Dr. Rajesh Patel", speciality="Endocrinology", hospital="Fortis Hospital", city="Mumbai", phone="+91 9876543211", email="rajesh.patel@fortis.in", preferred_contact="Phone"),
            HCP(name="Dr. Ananya Gupta", speciality="Oncology", hospital="Max Healthcare", city="Bangalore", phone="+91 9876543212", email="ananya.gupta@max.in", preferred_contact="Email")
        ]
        session.add_all(hcps)

        # Seed Materials
        materials = [
            Material(title="CardioPlus Clinical Study", category="Study", description="Detailed clinical trial results for CardioPlus demonstrating a 20% reduction in adverse events.", url="https://example.com/cardioplus-study.pdf"),
            Material(title="Diabetes Management Guide", category="Guide", description="Comprehensive guide for managing type 2 diabetes with our new insulin glargine formulation.", url="https://example.com/diabetes-guide.pdf"),
            Material(title="Hypertension Treatment Brochure", category="Brochure", description="Patient-friendly brochure explaining the benefits of our novel ARB.", url="https://example.com/hypertension-brochure.pdf")
        ]
        session.add_all(materials)
        
        session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
