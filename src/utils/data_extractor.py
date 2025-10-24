import re
from typing import Dict

def extraer_datos_desde_texto(texto: str) -> Dict[str, str]:
    patron_entidad_remitente = re.search(r"Entidad remitente:\s*(.*)", texto, re.IGNORECASE)
    patron_folio = re.search(r"Folio:\s*([A-Z0-9-]+)", texto, re.IGNORECASE)
    patron_nombre = re.search(r"Nombre\s+completo\s*[:\-]?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)(?=\s+Asunto|\n|$)", texto, re.IGNORECASE)
    patron_cedula = re.search(r"C[ée]dula\s*[:\-]?\s*(\d{5,15})", texto, re.IGNORECASE)


    return {
        "Entidad_Remitente": patron_entidad_remitente.group(1).strip().title() if patron_entidad_remitente else "No encontrado",
        "folio": patron_folio.group(1).strip() if patron_folio else "No encontrado",
        "nombre": patron_nombre.group(1).strip().title() if patron_nombre else "No encontrado",
        "cedula": patron_cedula.group(1).replace(".", "").strip() if patron_cedula else "No encontrado",
    }
