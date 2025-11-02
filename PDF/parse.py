import pdfplumber
from PIL import Image
from pathlib import Path

def extract_from_pdf(path: Path):
    docs = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            # try table extraction
            tables = page.extract_tables()
            docs.append({"text": text, "tables": tables})
    return docs
