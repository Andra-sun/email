import re
import spacy
from nltk.corpus import stopwords


nlp = spacy.load("pt_core_news_sm")
stop_words = set(stopwords.words("portuguese"))

def preprocess_text(text: str) -> str:
    """Recebe texto puro (idependente da origem) e retorna texto normalizado para IA.1"""
    
    
    text = text.lower()
    
    text = re.sub(r"[a-zà-ú\s]", " ", text)
    
    doc = nlp(text)
    
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_punct and len(token.text) > 2]
    
    return " ".join(tokens)