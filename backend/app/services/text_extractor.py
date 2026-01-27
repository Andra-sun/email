from pypdf import PdfReader

def extract_text_from_file(file, filename: str) -> str:
    if filename.endswith(".txt"):
        return file.decode("utf-8")

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    return ""
