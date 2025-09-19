"""
Configuración de la aplicación Flask
"""
import os

# Cargar variables de entorno solo si no estamos en Vercel
try:
    if not os.getenv('VERCEL'):
        from dotenv import load_dotenv
        load_dotenv()
except ImportError:
    # dotenv no está disponible, usar solo variables de entorno del sistema
    pass

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_para_desarrollo_cambiar_en_produccion')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuración JWT
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '2'))
    
    # Configuración de CORS para producción
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Inicialización adicional de la aplicación"""
        pass

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'desarrollo_secret_key')

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log de errores en producción
        import logging
        from logging.handlers import SMTPHandler
        
        if not app.debug and not app.testing:
            # Configurar logging para producción
            if not os.path.exists('logs'):
                os.mkdir('logs')

# Configuración por defecto basada en el entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}