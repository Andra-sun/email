import re
import spacy
from nltk.corpus import stopwords

try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    raise RuntimeError(
        "Modelo Spacy não encontrado. "
        "Execute: python -m spacy download pt_core_news_sm"
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
    
    text = re.sub(r"[a-zà-ú\s]", " ", text)
    
    doc = nlp(text)
    
    tokens = [
        token.lemma_ for token in doc
        if token.text not in stop_words 
        and not token.is_punct 
        and len(token.text) > 2
    ]
    
        
    return " ".join(tokens)