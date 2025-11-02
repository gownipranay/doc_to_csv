# doc_to_csv
# OCR Agent -> CSV

This project extracts text and structured fields from images and PDFs and converts them to CSV for ML engineers.

## Features
- Image + PDF ingestion
- Preprocessing (deskew, denoise)
- OCR (Tesseract + EasyOCR fallback)
- NER via HuggingFace
- LLM-based structured extraction using LangChain
- CSV output and optional embedding store (Chroma)

## Quickstart
1. Clone repo
2. Create virtualenv: `python -m venv .venv && source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. (Windows) Install tesseract binary and add to PATH
5. Run: `python src/pipeline/run.py` or use `notebooks/demo.ipynb`

## Notes
- Configure HuggingFace API tokens (if using HuggingFaceHub)
- For production, use GPU for heavy LLMs and OCR acceleration
