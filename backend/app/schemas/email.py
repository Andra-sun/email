from pydantic import BaseModel
from typing import Optional


class EmailRequest(BaseModel):
    """
    Esquema para receber email do frontend.
    """
    sender: Optional[str] = None
    subject: Optional[str] = None
    message: str
    
    class Config:
        example = {
            "sender": "joao@example.com",
            "subject": "Reunião importante",
            "message": "Gostaria de agendar uma reunião para discutir o projeto"
        }


class ClassificationResponse(BaseModel):
    """
    Esquema para resposta de classificação.
    """
    classification: str
    confidence: float
    suggested_response: str
    sender: Optional[str] = None
    subject: str
    processing_time: float
    
    class Config:
        example = {
            "classification": "Produtivo",
            "confidence": 0.95,
            "suggested_response": "Obrigado pelo seu email sobre 'Reunião importante Joao'...",
            "sender": "joao@example.com",
            "subject": "Reunião importante",
            "processing_time": 0.523
        }


class FileUploadRequest(BaseModel):
    """
    Esquema para upload de arquivo.
    """
    filename: str
    content: bytes
    
    class Config:
        example = {
            "filename": "documento.pdf",
            "content": b"PDF content here"
        }