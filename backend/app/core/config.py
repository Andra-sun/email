from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Lê variáveis de ambiente do arquivo .env
    """
    
    APP_NAME: str = "Email"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    API_V1_STR: str = "/api/v1"
    
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1",
    ]
    
    HF_API_URL: str = "https://api-inference.huggingface.co/models/MoritzLaurer/DeBERTa-v3-large-mnli-fever-docnli-ling-2c"
    HF_TOKEN: Optional[str] = None
    
    SPACY_MODEL: str = "pt_core_news_sm"
    
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".txt"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()