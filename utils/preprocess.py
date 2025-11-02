import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(img: Image.Image):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def preprocess_image(pil_img: Image.Image):
    img = pil_to_cv2(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # denoise
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    # thresh
    _, th = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # deskew
    coords = np.column_stack(np.where(th > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = th.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rotated = cv2.warpAffine(th, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return cv2_to_pil(rotated)
