from pathlib import Path
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from src.config import RUTA_TESSERACT, RUTA_POPPLER

def extraer_texto_pdf(ruta_pdf: Path) -> str:
    texto_completo = ""
    try:
        lector = PdfReader(ruta_pdf)
        for pagina in lector.pages:
            texto_completo += pagina.extract_text() or ""
        texto_completo = texto_completo.replace("\n", " ").strip()
    except Exception as e:
        print(f"[ADVERTENCIA] Error PyPDF2: {e}")

    if len(texto_completo) < 100:
        pytesseract.pytesseract.tesseract_cmd = RUTA_TESSERACT
        imagenes = convert_from_path(ruta_pdf, poppler_path=RUTA_POPPLER)
        texto_ocr = "".join(pytesseract.image_to_string(img) for img in imagenes)
        texto_completo = texto_ocr.replace("\n", " ").strip()

    return texto_completo
