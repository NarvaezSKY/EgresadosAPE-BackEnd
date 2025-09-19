"""
Inicialización de la aplicación Flask
"""
import os
from flask import Flask
from .config import config
from .routes import init_routes


def create_app(config_name=None):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración ('development', 'production', etc.)
    
    Returns:
        Flask: Instancia configurada de la aplicación Flask
    """
    if config_name is None:
        # Detectar entorno automáticamente
        if os.getenv('VERCEL') or os.getenv('FLASK_ENV') == 'production':
            config_name = 'production'
        else:
            config_name = 'development'
    
    app = Flask(__name__)
    
    # Aplicar configuración
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    # Inicializar configuración específica
    config_class.init_app(app)
    
    # Inicializar las rutas
    init_routes(app)
    
    return app