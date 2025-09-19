"""
API entry point para Vercel
"""
import os
import sys

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configurar variables de entorno para Vercel
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('DEBUG', 'False')

try:
    from app import create_app
    
    # Crear la aplicación
    app = create_app('production')
    
    # Variable requerida por Vercel
    application = app
    
except Exception as e:
    # Si hay error, crear una aplicación básica que muestre el error
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error_handler():
        return jsonify({
            "error": "Application failed to initialize",
            "message": str(e),
            "type": type(e).__name__
        }), 500
    
    @app.route('/health')
    def health():
        return jsonify({"status": "error", "message": "App initialization failed"})
    
    application = app

# Para compatibilidad con diferentes servidores WSGI
def handler(environ, start_response):
    """WSGI handler para Vercel"""
    return application(environ, start_response)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)