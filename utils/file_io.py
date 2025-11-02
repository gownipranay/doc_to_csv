from pathlib import Path
from PIL import Image
import pdfplumber
try:
    import fitz  # PyMuPDF  # type: ignore
except Exception:
    fitz = None  # type: ignore

def is_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf"

def load_pdf_pages(path: Path):
    # returns list of Pillow images (rasterized), and/or text per page
    pages = []
    # prefer extracting text with pdfplumber
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            # Save page raster if needed:
            pil_img = p.to_image(resolution=300).original  # pillow image
            pages.append({"text": text or "", "image": pil_img})
    return pages
