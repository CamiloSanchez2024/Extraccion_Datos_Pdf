# 📌 Proyecto: Automatización de lectura y extracción de datos judiciales

Este proyecto implementa un sistema automatizado que optimiza la gestión de solicitudes judiciales y fiscales recibidas por correo electrónico.  
El flujo de trabajo integra **Power Automate, Python (OCR y regex), bases de datos SQL/Supabase y Power BI** para reducir tiempos, minimizar errores y garantizar trazabilidad.

---

## 🎯 Funcionalidad principal

- **Recepción de correos electrónicos** con documentos adjuntos (PDF).
- **Descarga automática** de los archivos mediante Power Automate.
- **Procesamiento OCR** con Python (librería `pytesseract`) para extraer datos clave:
  - Número de folio  
  - Número de documento  
  - Nombre completo
  - Entidad remitente 
- **Almacenamiento en base de datos SQL/Supabase** para consulta centralizada.
- **Cruce automático con la base de clientes** para verificar productos financieros asociados.

---

## ⚙️ Ejecución del código principal

El archivo `src/main.py` contiene la lógica central del sistema:
- Procesa los documentos PDF.
- Aplica OCR y expresiones regulares.
- Inserta los datos en la base de datos.
- Llama los módulos de integración y generación de respuestas.

```bash
python -m src.main

# Creación del entorno virtual
python -m venv venv

# Activación del entorno virtual
venv/Scripts/Activate   # En Windows
source venv/bin/activate # En Linux/Mac

# Instalacion de librerias
pip install -r requirements.txt

