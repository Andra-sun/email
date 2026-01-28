import logging
from typing import Dict
from openai import OpenAI
from app.core.config import settings
import json
import re

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=settings.HF_TOKEN,
)


def _extract_json_from_text(text: str) -> Dict:
    """Extrai JSON de um texto que pode conter outros caracteres"""
    # Tenta primeiro o parse direto
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Tenta encontrar um JSON entre chaves
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Não foi possível extrair JSON válido do texto")


def classify_email(text: str) -> Dict[str, any]:
    """
    Classifica email E extrai confiança usando IA.
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:together",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um classificador de emails. Analise o texto e responda APENAS com um JSON válido, sem texto adicional."
                },
                {
                    "role": "user",
                    "content": f"""Classifique este email como "Produtivo" (trabalho relevante, propostas, projetos, reuniões, documentos importantes) ou "Improdutivo" (spam, promoções, clickbait, conteúdo irrelevante).

Responda APENAS com este JSON (sem texto adicional):
{{"classification": "Produtivo ou Improdutivo", "confidence": 0.0-1.0}}

Email:
{text}"""
                }
            ],
            max_tokens=150,
            temperature=0.1
        )
        response_text = response.choices[0].message.content.strip()
        
        logger.info(f"Resposta da API (raw): '{response_text}'")
        logger.info(f"Tamanho da resposta: {len(response_text)} caracteres")
        
        result = _extract_json_from_text(response_text)
        
        return {
            "classification": result.get("classification", "Produtivo"),
            "confidence": float(result.get("confidence", 0.5)),
            "success": True
        }
    
    except ValueError as e:
        logger.error(f"Erro ao extrair JSON: {e}. Resposta: '{response_text if 'response_text' in locals() else 'N/A'}'")
        return _fallback_classification(text)
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao fazer parse JSON: {e}. Resposta recebida: '{response_text if 'response_text' in locals() else 'N/A'}'")
        return _fallback_classification(text)
    except Exception as e:
        logger.error(f"Erro ao classificar: {e}")
        return _fallback_classification(text)


def _fallback_classification(text: str) -> Dict[str, any]:
    """Fallback com análise mais robusta de keywords"""
    text_lower = text.lower()
    
    improdutive_keywords = [
        "clique", "ganhe", "prêmio", "desconto", "promoção", "grátis",
        "oferta", "compre agora", "limitado", "urgente", "aproveite",
        "junte-se", "revenda", "oportunidade de ganho", "trabalhe conosco",
        "acessar", "confirmar dados", "atualizar conta", "verificar segurança",
        "click here", "buy now", "limited time", "exclusive offer",
        "você ganhou", "parabéns", "sorteio", "loteria"
    ]
    
    productive_keywords = [
        "reunião", "projeto", "proposta", "análise", "relatório", "documento",
        "apresentação", "planejamento", "estratégia", "objetivo", "meta",
        "feedback", "revisão", "aprovação", "assinatura", "contrato",
        "deadline", "entrega", "resultado", "performance", "dados",
        "meeting", "schedule", "agenda", "discussion", "collaboration",
        "budget", "invoice", "quarterly", "planning", "update"
    ]
    
    improdutive_count = sum(1 for kw in improdutive_keywords if kw in text_lower)
    productive_count = sum(1 for kw in productive_keywords if kw in text_lower)
    
    logger.info(f"Fallback - Improdutivo: {improdutive_count}, Produtivo: {productive_count}")
    
    if improdutive_count > productive_count:
        return {
            "classification": "Improdutivo",
            "confidence": 0.6,
            "success": True,
            "fallback": True
        }
    
    if productive_count > improdutive_count:
        return {
            "classification": "Produtivo",
            "confidence": 0.6,
            "success": True,
            "fallback": True
        }
    
    return {
        "classification": "Produtivo",
        "confidence": 0.5,
        "success": True,
        "fallback": True
    }


def generate_response(
    sender: str,
    subject: str,
    message: str,
    classification: str
) -> str:
    """
    Gera resposta contextualizada baseada no texto real.
    """
    
    try:
        # Extrair nome do sender se houver
        sender_name = None
        if sender:
            # Tenta extrair o nome antes do @ se for email
            if "@" in sender:
                sender_name = sender.split("@")[0].capitalize()
            else:
                sender_name = sender.capitalize()
        
        # Instruções sobre saudação
        greeting_instruction = ""
        if sender_name:
            greeting_instruction = f"Comece a resposta chamando {sender_name} pelo nome."
        else:
            greeting_instruction = "Comece a resposta com uma saudação genérica (não tente chamar a pessoa pelo nome)."
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:together",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente profissional que gera respostas de email. Gere respostas completas, contextualizadas e bem estruturadas."
                },
                {
                    "role": "user",
                    "content": f"""Gere uma resposta profissional de email com 6-8 linhas.
                    {greeting_instruction}
                    A resposta deve ser {"positiva, construtiva e interessada" if classification == "Produtivo" else "educada, profissional mas que recusa a proposta"}.
                    Referencie o conteúdo específico do email, não uma resposta genérica.
                    Se houver assunto relevante, você pode citá-lo: "{subject}"

                    Texto do email recebido:
                    {message}

                    Gere a resposta completa do email, sem prefácio ou explicações. A resposta deve incluir:
                    - Saudação e agradecimento pelo contato
                    - Referência ao conteúdo específico
                    - Seu posicionamento (positivo se Produtivo, recusa educada se Improdutivo)
                    - Menção que retornarão com feedback completo em breve
                    - Fechamento profissional
                    A resposta não deve incluir assinatura, nome, empresa ou contato fictico no final.
                    """
                }
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"Resposta gerada (tamanho: {len(response_text)} chars)")
        logger.info(f"Primeiros 150 chars: {response_text[:150]}")
        
        return response_text if response_text else _fallback_response(classification)
    
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return _fallback_response(classification)


def _fallback_response(classification: str) -> str:
    """Fallback de resposta"""
    if classification == "Produtivo":
        return """Agradecemos o envio deste material.
        Analisamos o conteúdo e consideramos relevante para nossa análise.
        Vamos revisar com atenção todos os pontos apresentados.
        Retornaremos com um feedback completo em breve.
        Obrigado pela contribuição."""
    else:
        return """Agradecemos o contato.
        Analisamos o material com cuidado.
        No momento, não conseguimos prosseguir com esta solicitação.
        Recomendamos buscar outros canais mais adequados.
        Desejamos sucesso em seus projetos."""