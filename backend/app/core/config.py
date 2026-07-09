from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://crm_user:crm_password@localhost:5432/crm_db"
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
