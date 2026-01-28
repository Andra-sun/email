from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional, Tuple
import time
import logging
import re

from app.schemas.email import EmailRequest, ClassificationResponse, FileUploadRequest
from app.services.nlp import preprocess_text
from app.services.ai import classify_email, generate_response
from app.services.text_extractor import extract_text_from_file
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/email",
    tags=["email"],
    responses={404: {"description": "Not found"}},
)


def extract_subject_and_sender(text: str) -> Tuple[str, Optional[str]]:
    """Extrai subject e sender do texto com IA"""
    sender = None
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    if email_match:
        sender = email_match.group(0)
    
    subject = ""
    
    return subject, sender


@router.post("/classify", response_model=ClassificationResponse)
async def classify_email_endpoint(email: EmailRequest):
    """
    Classifica email em Produtivo ou Improdutivo.
    
    - **sender**: Remetente do email (opcional)
    - **subject**: Assunto do email (opcional)
    - **message**: Corpo da mensagem
    """
    
    start_time = time.time()
    
    try:
        full_text = f"{email.subject or ''} {email.message}"
        
        logger.info(f"Processando email de {email.sender or 'desconhecido'}")
        
        processed_text = preprocess_text(full_text)
        
        classification_result = classify_email(processed_text)
        
        if not classification_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail="Erro ao classificar email"
            )    
                 
        suggested_response = generate_response(
            sender=email.sender,
            subject=email.subject or "",
            message=email.message,
            classification=classification_result["classification"]
        )
        
        processing_time = time.time() - start_time
        
        return ClassificationResponse(
            classification=classification_result["classification"],
            confidence=classification_result["confidence"],
            suggested_response=suggested_response,
            sender=email.sender or None,
            subject=email.subject or "",
            processing_time=round(processing_time, 3)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no endpoint de classificação: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar email"
        )

        
@router.post("/classify-file", response_model=ClassificationResponse)
async def classify_email_from_file(file: UploadFile = File(...)):
    """
    Classifica email a partir de arquivo (PDF ou TXT).
    
    - **file**: Arquivo PDF ou TXT com o email
    """
    
    start_time = time.time()
    
    try:
        if not any(file.filename.endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não permitido. Aceita: {settings.ALLOWED_EXTENSIONS}"
            )
        
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        text = extract_text_from_file(content, file.filename)
        
        if not text or text.strip() == "":
            logger.error(f"Arquivo vazio ou sem texto: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Não foi possível extrair texto do arquivo. O arquivo pode estar corrompido ou vazio."
            )
        
        logger.info(f"Processando arquivo: {file.filename}")
        
        subject, sender = extract_subject_and_sender(text)
        
        processed_text = preprocess_text(text)
        
        classification_result = classify_email(processed_text)
        
        if not classification_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail="Erro ao classificar email"
            )
        
        suggested_response = generate_response(
            sender=sender,
            subject=subject,
            message=text,
            classification=classification_result["classification"]
        )
        
        processing_time = time.time() - start_time
        
        return ClassificationResponse(
            classification=classification_result["classification"],
            confidence=classification_result["confidence"],
            suggested_response=suggested_response,
            sender=sender,
            subject=subject,
            processing_time=round(processing_time, 3)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar: {str(e)}"
        )     

        
@router.get("/health")
async def health_check():
    """Health check da API"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }