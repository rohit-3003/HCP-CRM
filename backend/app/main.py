from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.db.seed import seed_db

app = FastAPI(title="AI-First CRM API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
def on_startup():
    try:
        seed_db()
    except Exception as e:
        print(f"Error seeding database: {e}")

@app.get("/")
def read_root():
    return {"message": "AI-First CRM API is running. Check /docs for documentation."}
