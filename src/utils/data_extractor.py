import re
from typing import Dict

def extraer_datos_desde_texto(texto: str) -> Dict[str, str]:
    patron_folio = re.search(r"(?:proceso\s+(?:administrativo\s+coactivo\s+)?No\.?|AUTO\s*)\s*([A-Z]?\d{1,5}[-]?\d{2,4})", texto, re.IGNORECASE)
    patron_nombre = re.search(r"(?:contra|al\s+señor|del\s+señor)\s+([A-ZÁÉÍÓÚÑ\s]{5,80})[,\.]", texto, re.IGNORECASE)
    patron_cedula = re.search(r"(?:C\.?C\.?|cedula(?:\s+de\s+ciudadan[ií]a)?|N[o°]\.?)\s*(?:No\.?|N°|#)?\s*[:\-]?\s*(\d{5,15}(?:\.\d{3})*)", texto, re.IGNORECASE)

    return {
        "folio": patron_folio.group(1).strip() if patron_folio else "No encontrado",
        "nombre": patron_nombre.group(1).strip().title() if patron_nombre else "No encontrado",
        "cedula": patron_cedula.group(1).replace(".", "").strip() if patron_cedula else "No encontrado",
    }
