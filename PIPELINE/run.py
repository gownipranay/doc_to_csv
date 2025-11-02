from pathlib import Path
import pandas as pd
from utils.file_io import is_pdf, load_pdf_pages
from utils.preprocess import preprocess_image
from ocr.engine import extract_text_from_image
from nlp.clean import normalize_text
from nlp.ner import extract_entities
from langchain_extractor import extract_fields_with_llm  # from previous snippet

def process_file(path: Path):
    records = []
    if is_pdf(path):
        pages = load_pdf_pages(path)
        for p in pages:
            img = p["image"]
            cleaned = preprocess_image(img)
            text_from_img = extract_text_from_image(cleaned)
            text = (p.get("text", "") + "\n" + text_from_img).strip()
            text = normalize_text(text)
            # try quick NER
            entities = extract_entities(text)
            # try LLM structured extract for fields
            try:
                fields = extract_fields_with_llm(text)
            except Exception:
                fields = {}
            records.append({"path": str(path), "text": text, "entities": entities, **fields})
    else:
        from PIL import Image
        img = Image.open(path)
        cleaned = preprocess_image(img)
        text = normalize_text(extract_text_from_image(cleaned))
        entities = extract_entities(text)
        try:
            fields = extract_fields_with_llm(text)
        except Exception:
            fields = {}
        records.append({"path": str(path), "text": text, "entities": entities, **fields})
    return records

def batch_to_csv(paths, out_csv="output.csv"):
    rows = []
    for p in paths:
        rows.extend(process_file(Path(p)))
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    return out_csv
