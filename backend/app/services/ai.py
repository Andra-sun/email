import requests
import logging
from typing import Dict

logger = logging.getLogger(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/DeBERTa-v3-large-mnli-fever-docnli-ling-2c"
HF_TOKEN = None

def classify_email(text: str) -> Dict[str, any]:
    """
    Classifica email em Produtivo ou Inprodutivo usando Hugging Face.
    
    Args:
        text: Texto pré-processado do email.
        
    Returns:
        Dict com:
        - classitication: 'Produtivo' ou 'Inprodutivo'
        - confidence: Confiança (0-1)
        - success: True/False
    """
    
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": ["Produtivo", "Inprodutivo"],
            "multi_class": False
        }
    }
    
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
        
    
    try:
        response = requests.post(
            HF_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        ) 
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "classification": result['labels'][0],
                "confidence": result['scores'][0],
                "success": True
            }
        else:
            logger.warning(f"API retornou status {response.status_code}")
            return _fallback_classification(text)
        
    except requests.exceptions.Timeout:
        logger.warning("Timeout na API HF, usando fallback")
        return _fallback_classification(text)
    
    except Exception as e:
        logger.error(f"Erro ao classificar: {e}")
        return _fallback_classification(text)    
    
def _fallback_classification(text: str) -> Dict[str, any]:
    """
    Classificação por regras simples quando API falha.
    
    Args:
        text: Texto para classificar
        
    Returns:
        Classificação baseada em palavras-chave
    """
    
    text_lower = text.lower()
    
    spam_keywords = [
        "clique", "ganhe", "prêmio", "desconto", 
        "promoção", "grátis", "oferta"
    ]
    
    if any(kw in text_lower for kw in spam_keywords):
        return {
            "classification": "Inprodutivo",
            "confidence": 0.7,
            "success": True,
            "fallback": True
        }
        
    productive_keywords = [
        "reunião", "projeto", "proposta", 
        "colaboração", "discussão", "análise"
    ]
    
    if any(kw in text_lower for kw in productive_keywords):
        return {
            "classification": "Produtivo",
            "confidence": 0.7,
            "success": True,
            "fallback": True
        }
        
def generate_response(
    classification: str,
    subject: str,
    context: str = "default"
) -> str:
    """
    Gera resposta automática baseada na classificação.
    
    Args:
        classification: "Produtivo" ou "Improdutivo"
        subject: Assunto do email
        context: Tipo de contexto (question, proposal, etc)
        
    Returns:
        Resposta sugerida
    """
    
    templates = {
            "Produtivo": {
            "question": f"Agradeço sua pergunta sobre '{subject}'. Vou analisar e retorno em breve.",
            "proposal": f"Muito interessado em sua proposição sobre '{subject}'. Vamos avaliar.",
            "urgent": f"Entendo a urgência. Vou priorizar '{subject}' e responder em breve.",
            "default": f"Obrigado pelo seu email sobre '{subject}'. Responderei em breve."
        },
            "Improdutivo": {
            "question": "Agradecemos seu contato, mas não conseguimos ajudar com esta solicitação.",
            "proposal": "Sua proposta não está de acordo com nossos objetivos atuais.",
            "urgent": "Infelizmente não conseguimos priorizar este assunto.",
            "default": "Agradecemos o contato. Recomendamos outros canais para esta demanda."
        }
    }
    
    
    response_dict = templates.get(classification, templates["Produtivo"])
    return response_dict.get(context, response_dict["default"])