import pytesseract
from PIL import Image
import easyocr

# If Tesseract binary not in PATH, set:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

reader = easyocr.Reader(['en'], gpu=False)  # set gpu True when available

def ocr_tesseract(pil_img: Image.Image):
    return pytesseract.image_to_string(pil_img, lang='eng')

def ocr_easyocr(pil_img: Image.Image):
    results = reader.readtext(np.array(pil_img))
    # results = [(bbox, text, prob), ...]
    text = "\n".join([r[1] for r in results])
    return text

def extract_text_from_image(pil_img: Image.Image):
    # try pdf native text first (if provided)
    try:
        txt = ocr_tesseract(pil_img)
        if len(txt.strip()) > 10:
            return txt
    except Exception:
        pass
    # fallback to easyocr
    return ocr_easyocr(pil_img)
