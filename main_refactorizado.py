"""
Punto de entrada de la aplicación PilAPE
"""
import os
import sys

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

# Crear la aplicación usando el factory pattern con configuración de producción
app = create_app('production' if os.getenv('VERCEL') else None)

# Para Vercel: asegurarse de que la app esté disponible
application = app

# Handler para Vercel
def handler(request, context):
    """Handler para Vercel serverless"""
    return app(request.environ, context)

if __name__ == "__main__":
    # Obtener configuración del entorno
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)