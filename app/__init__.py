"""
Inicialización de la aplicación Flask
"""
from flask import Flask
from .config import Config
from .routes import init_routes


def create_app(config_class=Config):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_class: Clase de configuración a usar (por defecto Config)
    
    Returns:
        Flask: Instancia configurada de la aplicación Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar las rutas
    init_routes(app)
    
    return app