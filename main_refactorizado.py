"""
Punto de entrada de la aplicación PilAPE
"""
import os
from app import create_app

# Crear la aplicación usando el factory pattern
app = create_app()

if __name__ == "__main__":
    # Obtener configuración del entorno
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)