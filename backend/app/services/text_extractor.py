from pypdf import PdfReader
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


def extract_text_from_file(file, filename: str) -> str:
    """
    Extrai texto de arquivo (PDF ou TXT).
    """
    
    try:
        if filename.endswith(".txt"):
            try:
                return file.decode("utf-8")
            except UnicodeDecodeError:
                return file.decode("latin-1")
        
        if filename.endswith(".pdf"):
            return _extract_text_from_pdf(file)
        
        return ""
    
    except Exception as e:
        logger.error(f"Erro ao extrair texto: {e}")
        raise Exception(f"Não foi possível extrair texto do arquivo: {str(e)}")


def _extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extrai texto de PDF com múltiplas tentativas.
    """
    pdf_file = BytesIO(file_content)
    
    try:
        reader = PdfReader(pdf_file)
        
        if len(reader.pages) == 0:
            raise Exception("PDF vazio ou corrompido")
        
        logger.info(f"PDF contém {len(reader.pages)} página(s)")
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    logger.info(f"Página {page_num + 1}: {len(page_text)} caracteres extraídos")
                else:
                    logger.warning(f"Página {page_num + 1}: Nenhum texto extraído")
            except Exception as e:
                logger.warning(f"Erro ao extrair página {page_num + 1}: {e}")
                continue
        
        if not text or text.strip() == "":
            raise Exception("Nenhum texto foi extraído do PDF")
        
        logger.info(f"Total de caracteres extraídos: {len(text)}")
        return text.strip()
    
    except Exception as e:
        logger.error(f"Erro ao processar PDF: {e}")
        raise Exception(f"Erro ao ler PDF: {str(e)}")