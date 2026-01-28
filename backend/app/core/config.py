from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    
    APP_NAME: str = "Email Classifier"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    API_V1_STR: str = "/api/v1"
    
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8080",
        "https://email-nine-xi.vercel.app",
    ]
    
    HF_API_URL: str = "https://router.huggingface.co/v1"
    HF_TOKEN: str = ""
    
    SPACY_MODEL: str = "pt_core_news_sm"
    
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS: list = [".pdf", ".txt"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()