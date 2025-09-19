"""
Configuración de la aplicación Flask
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Configuración JWT
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '2'))