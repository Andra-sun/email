import re
import os
import spacy
import nltk
from nltk.corpus import stopwords
from app.core.config import settings

NLTK_DATA_DIR = "/opt/render/project/src/nltk_data"
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

nltk.data.path.append(NLTK_DATA_DIR)
nltk.download("stopwords", download_dir=NLTK_DATA_DIR)

try:
    nlp = spacy.load(settings.SPACY_MODEL)
except OSError:
    raise RuntimeError(
        f"Modelo Spacy não encontrado. "
        f"Execute: python -m spacy download {settings.SPACY_MODEL}"
    )

stop_words = set(stopwords.words("portuguese"))


def preprocess_text(text: str) -> str:
    """ Recebe texto puro e retorna texto normalizado para IA.
    
        Operações:
        - Converter para minúsculas
        - Remover URLs e caracteres especiais
        - Tokenizar com Spacy
        - Remover stopwords
        - Remover pontuação
        - Aplicar lemmatização
        
        Args:
            text: Texto bruto
            
        Returns:
            Texto processado e pronto para classificação.
    """
    
    
    text = text.lower()
    
    text = re.sub(r'http\S+|www\S+', '', text)
    
    text = re.sub(r"[^a-zà-ú\s]", " ", text)
    
    doc = nlp(text)
    
    tokens = [
        token.lemma_ for token in doc
        if token.text not in stop_words 
        and not token.is_punct 
        and len(token.text) > 2
    ]
    
        
    return " ".join(tokens)
