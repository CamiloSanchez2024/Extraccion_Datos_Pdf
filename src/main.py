from pathlib import Path
from src.config import CARPETA_PDFS
from utils.pdf_reader import extraer_texto_pdf
from utils.data_extractor import extraer_datos_desde_texto
from  utils.supabase_client import guardar_en_supabase

def main():
    carpeta_pdf = Path(CARPETA_PDFS)
    archivos_pdf = list(carpeta_pdf.glob("*.pdf"))

    for archivo in archivos_pdf:
        print(f"\nProcesando: {archivo.name}")
        texto = extraer_texto_pdf(archivo)
        datos = extraer_datos_desde_texto(texto)
        # Mostrar datos extraídos
        for k, v in datos.items():
            print(f"{k.capitalize()}: {v}")
        # Guardar en Supabase
        resultado = guardar_en_supabase(datos)
        if resultado:
            print(f"✓ Datos guardados exitosamente en Supabase")
        else:
            print(f"✗ Error al guardar en Supabase")    

if __name__ == "__main__":
    main()
