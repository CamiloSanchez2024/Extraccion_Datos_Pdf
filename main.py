import re
from pathlib import Path
from typing import Dict, Optional
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path

# === CONFIGURACIÓN GLOBAL ===
RUTA_TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
RUTA_POPPLER = r"C:\ProgramData\chocolatey\lib\poppler\tools\poppler-25.10.0\bin"

def extraer_texto_pdf(ruta_pdf: Path) -> str:
    texto_completo = ""
    try:
        lector = PdfReader(ruta_pdf)
        for pagina in lector.pages:
            texto_completo += pagina.extract_text() or ""
        texto_completo = texto_completo.replace("\n", " ").strip()
    except Exception as e:
        print(f"[ADVERTENCIA] No se pudo leer texto con PyPDF2: {e}")

    if len(texto_completo) < 100:
        try:
            print(f"[INFO] Poco texto detectado en {ruta_pdf.name}. Aplicando OCR...")
            pytesseract.pytesseract.tesseract_cmd = RUTA_TESSERACT
            imagenes = convert_from_path(ruta_pdf, poppler_path=RUTA_POPPLER)
            texto_ocr = "".join(pytesseract.image_to_string(img) for img in imagenes)
            texto_completo = texto_ocr.replace("\n", " ").strip()
        except Exception as e:
            print(f"[ERROR] No se pudo realizar OCR en {ruta_pdf.name}: {e}")

    return texto_completo

def extraer_datos_desde_texto(texto: str) -> Dict[str, str]:
    patron_folio = re.search(
        r"(?:proceso\s+(?:administrativo\s+coactivo\s+)?No\.?|AUTO\s*)\s*([A-Z]?\d{1,5}[-]?\d{2,4})",
        texto,
        re.IGNORECASE
    )

    patron_nombre = re.search(
        r"(?:contra|al\s+señor|del\s+señor)\s+([A-ZÁÉÍÓÚÑ\s]{5,80})[,\.]",
        texto,
        re.IGNORECASE
    )

    patron_cedula = re.search(
        r"(?:C\.?C\.?|cedula(?:\s+de\s+ciudadan[ií]a)?|N[o°]\.?)\s*(?:No\.?|N°|#)?\s*[:\-]?\s*(\d{5,15}(?:\.\d{3})*)",
        texto,
        re.IGNORECASE
    )

    return {
        "folio": patron_folio.group(1).strip() if patron_folio else "No encontrado",
        "nombre": patron_nombre.group(1).strip().title() if patron_nombre else "No encontrado",
        "cedula": patron_cedula.group(1).replace(".", "").strip() if patron_cedula else "No encontrado",
    }

def extraer_datos_pdf(ruta_pdf: Path) -> Optional[Dict[str, str]]:
    try:
        if not ruta_pdf.exists() or ruta_pdf.suffix.lower() != ".pdf":
            raise FileNotFoundError(f"El archivo {ruta_pdf} no existe o no es un PDF válido.")

        texto = extraer_texto_pdf(ruta_pdf)
        if not texto:
            raise ValueError("No se pudo extraer texto del PDF.")

        datos = extraer_datos_desde_texto(texto)
        datos["texto_completo"] = texto

        return datos
    except Exception as e:
        print(f"[ERROR] Falló la extracción de {ruta_pdf.name}: {e}")
        return None

def main():
    # Carpeta donde están todos los PDFs de OneDrive
    carpeta_pdf = Path(r"C:\Users\Camilo S\OneDrive - UCompensar\8 Semestre\Sistemas de informacion empresarial")

    if not carpeta_pdf.exists():
        print(f"[ERROR] La carpeta {carpeta_pdf} no existe.")
        return

    # Buscar todos los archivos .pdf en la carpeta
    archivos_pdf = list(carpeta_pdf.glob("*.pdf"))

    if not archivos_pdf:
        print(f"[INFO] No se encontraron PDFs en {carpeta_pdf}.")
        return

    # Procesar cada PDF
    for archivo in archivos_pdf:
        print(f"\n[INFO] Procesando archivo: {archivo.name}")
        resultado = extraer_datos_pdf(archivo)

        if resultado:
            print("=== DATOS EXTRAÍDOS ===")
            for clave, valor in resultado.items():
                if clave != "texto_completo":
                    print(f"{clave.capitalize()}: {valor}")
        else:
            print("❌ No se pudo extraer información de este PDF.")

if __name__ == "__main__":
    main()
