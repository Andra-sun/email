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


"""
EXEMPLOS DE EMAILS PRODUTIVOS (trabalho relevante, propostas, projetos, reuniões):
============================================================================================

EXEMPLO 1 - Reunião agendada:
    Assunto: Reunião de Planejamento Q1 2026
    Corpo:
    "Olá,
    Gostaria de agendar uma reunião com sua equipe para discutir o planejamento
    do primeiro trimestre. Proponho os seguintes temas:
    - Objetivos do trimestre
    - Alocação de recursos
    - Cronograma de entregas
    
    Você teria disponibilidade na semana que vem?
    Atenciosamente,
    João Silva"

EXEMPLO 2 - Proposta de projeto:
    Assunto: Proposta de Projeto - Sistema de Automação
    Corpo:
    "Prezados,
    Desenvolvi uma proposta de novo projeto que pode otimizar o processo de 
    faturamento. O projeto inclui:
    - Análise de requisitos
    - Desenvolvimento do sistema
    - Testes e implementação
    - Documentação completa
    
    Orçamento: R$ 45.000,00
    Prazo estimado: 3 meses
    
    Gostaria de apresentar os detalhes. Qual data funciona melhor?"

EXEMPLO 3 - Feedback sobre relatório:
    Assunto: RE: Relatório Trimestral - Análise
    Corpo:
    "Recebi o relatório trimestral. Excelente trabalho!
    Alguns pontos que gostaria de expandir:
    1. Detalhamento das métricas de performance
    2. Análise comparativa com trimestre anterior
    3. Recomendações estratégicas
    
    Quando teremos a próxima versão?"

EXEMPLO 4 - Assinatura de contrato:
    Assunto: Contrato para Assinatura - Fornecimento de Serviços
    Corpo:
    "Em anexo, o contrato para fornecimento de serviços de consultoria.
    Por favor, revise os termos e confirme se está tudo certo.
    O contrato tem validade de 12 meses com possibilidade de renovação.
    Fique à vontade para solicitar ajustes nos termos."

============================================================================================

EXEMPLOS DE EMAILS IMPRODUTIVOS (spam, promoções, clickbait, irrelevante):
============================================================================================

EXEMPLO 1 - Spam comercial:
    Assunto: GANHE 50% DE DESCONTO AGORA - Oferta Imperdível!
    Corpo:
    "CLIQUE AQUI para aproveitar a maior promoção do ano!
    Apenas HOJE você consegue 50% off em TUDO!
    Não perca! Essa oportunidade não volta.
    COMPRE AGORA antes que acabe o estoque!
    APROVEITE!"

EXEMPLO 2 - Sorteio/Loteria:
    Assunto: VOCÊ GANHOU! Parabéns!!
    Corpo:
    "Parabéns! Você foi selecionado para receber um prêmio exclusivo!
    Você ganhou: 1 iPhone 15 + R$ 10.000 em créditos!
    Clique aqui para reivindicar seu prêmio antes que expire.
    Sorteio válido por 24 horas!"

EXEMPLO 3 - Phishing/Verificação falsa:
    Assunto: URGENTE: Confirme seus dados de acesso
    Corpo:
    "Sua conta foi detectada com atividade suspeita.
    Por segurança, você precisa verificar seus dados clicando no link abaixo.
    Clique aqui para atualizar sua conta.
    Isso levará apenas 2 minutos!"

EXEMPLO 4 - Newsletter/Marketing genérico:
    Assunto: Confira as novidades da semana!
    Corpo:
    "Olá amigo!
    Não perca nossas novidades esta semana:
    - Novo produto X
    - Curso de Y
    - Oferta especial em Z
    Clique aqui para ver tudo!"

============================================================================================

NOTAS PARA MELHORAR A CLASSIFICAÇÃO:
- Emails produtivos: mencionam reuniões, projetos, prazos, análises, dados específicos
- Emails improdutivos: usam ALL CAPS, múltiplas exclamações, urgência artificial, clickbait
- Produtivo: assunto específico e relacionado ao trabalho
- Improdutivo: assunto genérico, urgência forçada, chamadas para ação agressivas
"""


def _extract_json_from_text(text: str) -> Dict:
    """Extrai JSON de um texto que pode conter outros caracteres"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
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
        logger.info(f"[CLASSIFY_EMAIL] Tamanho do texto: {len(text)} caracteres")
        logger.info(f"[CLASSIFY_EMAIL] Primeiros 200 chars do texto: {text[:200]}")
        logger.info(f"[CLASSIFY_EMAIL] Token HF configurado: {'Sim' if settings.HF_TOKEN else 'NÃO - ERRO!'}")
        
        prompt = f"""Classifique este email como "Produtivo" (trabalho relevante, propostas, projetos, reuniões, documentos importantes) ou "Improdutivo" (spam, promoções, clickbait, conteúdo irrelevante).

Responda APENAS com este JSON (sem texto adicional):
{{"classification": "Produtivo ou Improdutivo", "confidence": 0.0-1.0}}

Email:
{text}"""
        
        logger.info(f"[CLASSIFY_EMAIL] Prompt completo a ser enviado:\n{prompt}")
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:together",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um classificador de emails. Analise o texto e responda APENAS com um JSON válido, sem texto adicional."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )
        response_text = response.choices[0].message.content.strip()
        
        logger.info(f"[CLASSIFY_EMAIL] Resposta da API (raw): '{response_text}'")
        logger.info(f"[CLASSIFY_EMAIL] Tamanho da resposta: {len(response_text)} caracteres")
        
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


def _extract_sender_name(sender: str, message: str) -> str:
    """
    Extrai e valida o nome do remetente (pessoa ou empresa) com regras específicas.
    
    Regras de identificação:
    1. O nome do remetente vem do email, antes do @
    2. Deve ter apenas letras (a-z, A-Z), acentos, números (para empresas), espaços e hífens
    3. Não deve ser uma palavra comum que indica cargo/função (admin, suporte, etc)
    4. Deve ter pelo menos 2 caracteres
    5. Validação cruzada: verifica se aparece no corpo do email
    
    Detecta automaticamente se é:
    - NOME DE PESSOA: padrão "nome sobrenome" (ex: "João Silva")
    - NOME DE EMPRESA: pode conter números ou palavras maiúsculas (ex: "Tech123", "ABCConsultoria")
    
    Validação cruzada:
    - Busca o nome no corpo da mensagem para confirmar origem
    - Padrões: "João,", "meu nome é João", "sou a empresa X", etc
    """
    if not sender or "@" not in sender:
        return None
    
    email_prefix = sender.split("@")[0]
    
    cleaned_name = re.sub(r'[._+]', ' ', email_prefix).strip()
    cleaned_name = cleaned_name.replace('-', ' ')
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    
    function_words = [
        'admin', 'suporte', 'vendas', 'contato', 'info', 'noreply',
        'support', 'sales', 'contact', 'no-reply', 'hello', 'hi',
        'service', 'servico', 'atendimento', 'help', 'helpdesk',
        'newsletter', 'notificacao', 'notificação', 'alert', 'alerta'
    ]
    
    if cleaned_name.lower() in function_words:
        return None
    
    if not re.match(r'^[a-záàâãéèêíïóôõöúçñ0-9\s\-&]+$', cleaned_name, re.IGNORECASE):
        return None
    
    if len(cleaned_name) < 2:
        return None
    
    name_appears_in_message = False
    if message:
        message_lower = message.lower()
        cleaned_lower = cleaned_name.lower()
        first_word = cleaned_name.split()[0].lower()
        
        sender_patterns = [
            f"^{re.escape(first_word)}[^a-z]",  # No início (Ex: "João,")
            f" {re.escape(first_word)}[,.]",     # No meio com pontuação
            f"meu nome é {re.escape(cleaned_lower)}",  # Explícito - pessoa
            f"nome da empresa é {re.escape(cleaned_lower)}",  # Explícito - empresa
            f"somos {re.escape(cleaned_lower)}",  # Explícito - empresa
            f"sou o {re.escape(first_word)}",  # Explícito - pessoa
            f"eu sou o {re.escape(first_word)}",  # Explícito - pessoa
            f"estou na {re.escape(cleaned_lower)}",  # Trabalha em empresa
            f"da {re.escape(cleaned_lower)}",  # Vem de empresa
            f"pela {re.escape(cleaned_lower)}",  # Pela empresa
        ]
        
        for pattern in sender_patterns:
            try:
                if re.search(pattern, message_lower):
                    name_appears_in_message = True
                    break
            except re.error:
                # Se houver erro no padrão, ignora
                continue
    
    return cleaned_name.title() if cleaned_name else None


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
        sender_name = _extract_sender_name(sender, message)
        
        greeting_instruction = ""
        if sender_name:
            greeting_instruction = f"""Comece a resposta chamando {sender_name} pelo nome ou empresa.
            Regras para identificar que '{sender_name}' é o nome/empresa correto do remetente:
            1. O nome foi extraído do email ({sender}) e validado
            2. Pode ser NOME DE PESSOA (apenas letras: "João Silva") ou EMPRESA (pode ter números: "Tech123")
            3. Não contém símbolos especiais problemáticos (como pontos, underscores, +)
            4. Não é um cargo genérico (não é 'admin', 'suporte', 'vendas' ou 'contato')
            5. Se encontrado no corpo do email, aumenta confiança de ser realmente o nome/empresa
            6. Padrões de validação: "Meu nome é {sender_name}", "Somos {sender_name}", "Da {sender_name}", etc
            Use este nome na saudação inicial: "Olá {sender_name}," ou "Prezados {sender_name},"
            """
        
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
                    
                    Regras:
                    - Não pode deixar frases incompletas.
                    - Não pode gerar respostas genéricas ou vagas.
                    - Deve sedmpre enviar o texto.
                    - Deve sempre pontuar corretamente as frases.
                    - deve haver ao menos 6 linhas na resposta.
                    - Não pode haver mais de 10 linhas de respostas, ela deve ser completa no limite recomendado.
                    
                    Exemplo de resposta produtiva:
                    Olá,

                    Recebemos sua mensagem e analisamos as informações relacionadas ao prazo, escopo e pontos levantados.
                    Alguns detalhes mencionados exigem uma validação interna antes de um posicionamento definitivo.
                    Neste momento, estamos revisando os impactos e alinhamentos necessários sobre o tema apresentado.
                    Em breve, retornaremos com uma resposta mais completa e direcionada ao seu pedido.
                    Caso seja necessário complementar alguma informação, entraremos em contato.
                    Agradecemos a compreensão e seguimos à disposição.

                    Atenciosamente
                    
                    Exemplo de resposta improdutiva:
                    A mensagem foi recebida e as informações apresentadas foram consideradas.
                    No momento, o conteúdo não demanda qualquer ação ou encaminhamento adicional.
                    Dessa forma, não haverá continuidade sobre o tema tratado.
                    Caso surja algum ponto novo ou relevante, poderá ser enviado em um novo contato.
                    Agradecemos a comunicação e a atenção dispensada.

                    Atenciosamente
                    
                    """
                }
            ],
            temperature=0.4
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"[GENERATE_RESPONSE] Resposta gerada (tamanho: {len(response_text)} chars)")
        logger.info(f"[GENERATE_RESPONSE] Primeiros 150 chars: {response_text[:150]}")
        
        if not response_text:
            logger.warning("[GENERATE_RESPONSE] Resposta vazia recebida! Usando fallback.")
            return _fallback_response(classification)
        
        return response_text
    
    except Exception as e:
        logger.error(f"[GENERATE_RESPONSE] Erro ao gerar resposta: {e}")
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