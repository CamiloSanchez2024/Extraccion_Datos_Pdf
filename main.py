from pathlib import Path
from config import CARPETA_PDFS
from utils.pdf_reader import extraer_texto_pdf
from utils.data_extractor import extraer_datos_desde_texto

def main():
    carpeta_pdf = Path(CARPETA_PDFS)
    archivos_pdf = list(carpeta_pdf.glob("*.pdf"))

    for archivo in archivos_pdf:
        print(f"\nProcesando: {archivo.name}")
        texto = extraer_texto_pdf(archivo)
        datos = extraer_datos_desde_texto(texto)
        for k, v in datos.items():
            print(f"{k.capitalize()}: {v}")

if __name__ == "__main__":
    main()
