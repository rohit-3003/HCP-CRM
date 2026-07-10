from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://crm_user:crm_password@localhost:5432/crm_db"
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

    @property
    def sync_database_url(self) -> str:
        # Render provides `postgres://`, but SQLAlchemy requires `postgresql://`
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL

settings = Settings()
