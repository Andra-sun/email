# app/services/text_extractor.py

from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)


def extract_text_from_file(file, filename: str) -> str:
    """
    Extrai texto de arquivo (PDF ou TXT).
    
    Args:
        file: Arquivo em bytes
        filename: Nome do arquivo (para identificar tipo)
        
    Returns:
        Texto extraído do arquivo
    """
    
    try:
        if filename.endswith(".txt"):
            return file.decode("utf-8")
        
        if filename.endswith(".pdf"):
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        
        return ""
    
    except Exception as e:
        logger.error(f"Erro ao extrair texto: {e}")
        return ""