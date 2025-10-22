from supabase import create_client, Client
from typing import Dict, Optional
from src.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

def obtener_cliente_supabase() -> Client:
    """Crea y retorna un cliente de Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def guardar_en_supabase(datos: Dict[str, str], tabla: str = "Datos") -> Optional[Dict]:
    """
    Guarda los datos extraídos en Supabase
    
    Args:
        datos: Diccionario con los datos extraídos (folio, nombre, cedula)
        tabla: Nombre de la tabla en Supabase (default: "Datos")
    
    Returns:
        Datos insertados si fue exitoso, None en caso de error
    """
    try:
        supabase = obtener_cliente_supabase()
        
        # Preparar datos para inserción - nombres exactos de tu tabla
        datos_insertar = {
            "Folio": datos.get("folio"),
            "Nombre": datos.get("nombre"),
            "Cedula": datos.get("cedula")
        }
        
        # Insertar en Supabase
        response = supabase.table(tabla).insert(datos_insertar).execute()
        
        return response.data
        
    except Exception as e:
        print(f"Error al guardar en Supabase: {e}")
        print(f"Intentando insertar: {datos_insertar}")
        return None

def verificar_documento_existe(folio: str, tabla: str = "Datos") -> bool:
    """
    Verifica si un documento con el mismo folio ya existe en la base de datos
    
    Args:
        folio: Número de folio a verificar
        tabla: Nombre de la tabla en Supabase
    
    Returns:
        True si existe, False si no existe
    """
    try:
        supabase = obtener_cliente_supabase()
        response = supabase.table(tabla).select("Folio").eq("Folio", folio).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error al verificar documento: {e}")
        return False