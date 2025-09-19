"""
Funciones de autenticación y manejo de JWT
"""
import jwt
import datetime
from .config import Config


def generar_token(egresado):
    """
    Genera un token JWT para un egresado autenticado
    
    Args:
        egresado: Instancia de la clase Egresado
    
    Returns:
        str: Token JWT codificado
    """
    payload = {
        "cedula": egresado.cedula,
        "red": egresado.red,
        "perfil": egresado.perfil,
        "nombre": egresado.nombre,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def verificar_token(token):
    """
    Verifica y decodifica un token JWT
    
    Args:
        token (str): Token JWT a verificar
    
    Returns:
        dict or None: Payload del token si es válido, None si es inválido o expirado
    """
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def extraer_token_del_header(auth_header):
    """
    Extrae el token del header Authorization
    
    Args:
        auth_header (str): Header Authorization en formato "Bearer <token>"
    
    Returns:
        str or None: Token si es válido, None si el formato es incorrecto
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    return auth_header.split(" ")[1]


def autenticar_egresado(cedula, ficha, egresados_lista):
    """
    Autentica un egresado con cedula y ficha
    
    Args:
        cedula (str): Cédula del egresado
        ficha (str): Ficha del egresado
        egresados_lista (list): Lista de egresados registrados
    
    Returns:
        Egresado or None: Egresado si las credenciales son válidas, None si no
    """
    return next((e for e in egresados_lista if e.cedula == cedula and e.ficha == ficha), None)