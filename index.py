"""
PilAPE API - Versión simplificada para Vercel
Sistema de matching de empleos para egresados
"""
import os
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import logging
from collections import deque

# =============================================
# CONFIGURACIÓN
# =============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'desarrollo_secret_key_cambiar_en_produccion')

# =============================================
# MODELOS DE DATOS
# =============================================
class Egresado:
    def __init__(self, cedula, nombre, ficha, red, perfil):
        self.cedula = cedula
        self.nombre = nombre
        self.ficha = ficha
        self.red = red
        self.perfil = perfil

class Empleo:
    def __init__(self, id, titulo, descripcion, perfil_requerido, salario, ubicacion):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.perfil_requerido = perfil_requerido
        self.salario = salario
        self.ubicacion = ubicacion
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "perfil_requerido": self.perfil_requerido,
            "salario": self.salario,
            "ubicacion": self.ubicacion
        }

class Cola:
    """Cola FIFO simple respaldada por collections.deque

    Métodos:
    - encolar(item): añade al final
    - desencolar(): saca del frente (None si vacía)
    - esta_vacia(): True si no hay elementos
    """
    def __init__(self):
        self.items = deque()

    def encolar(self, item):
        # Añade el item al final de la cola (operación O(1)).
        # Si encolamos en orden descendente por score, el frente
        # contendrá siempre el empleo con mayor score.
        self.items.append(item)

    def desencolar(self):
        # Quita y devuelve el elemento del frente (primer en entrar).
        # Devuelve None si la cola está vacía.
        if not self.esta_vacia():
            return self.items.popleft()
        return None

    def esta_vacia(self):
        return len(self.items) == 0

# =============================================
# BASE DE DATOS (usar `app.models` como fuente única)
# =============================================
# Importar los datos desde `app.models` para evitar duplicidad entre entrypoints
from app.models import egresados_data, empleos_data

# =============================================
# FUNCIONES DE AUTENTICACIÓN
# =============================================
def generar_token(egresado):
    """Genera token JWT para el egresado"""
    payload = {
        'cedula': egresado.cedula,
        'red': egresado.red,
        'perfil': egresado.perfil,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verificar_token(token):
    """Verifica y decodifica el token JWT"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def extraer_token_del_header(auth_header):
    """Extrae el token del header Authorization"""
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    return None

# =============================================
# ALGORITMO DE MATCHING
# =============================================
def calcular_score_por_palabras_clave(egresado, empleo):
    """Calcula score de compatibilidad entre egresado y empleo"""
    # Palabras irrelevantes a excluir
    palabras_excluidas = {
        'de', 'del', 'la', 'el', 'los', 'las', 'en', 'con', 'por', 'para', 'y', 'o', 'un', 'una', 
        'este', 'esta', 'ese', 'esa', 'su', 'sus', 'se', 'que', 'es', 'son', 'como', 'más', 'muy'
    }
    
    # Palabras técnicas relevantes
    palabras_tecnicas = {
        'software', 'desarrollo', 'programacion', 'web', 'python', 'javascript', 'react', 'flask',
        'salud', 'medicina', 'enfermeria', 'primeros', 'auxilios', 'paciente', 'hospital',
        'agricola', 'agricultura', 'cultivos', 'campo', 'siembra', 'cosecha',
        'mecanica', 'industrial', 'mantenimiento', 'soldadura', 'maquinaria', 'equipos'
    }
    
    def filtrar_palabras_relevantes(texto):
        palabras = set(texto.lower().split())
        palabras_filtradas = palabras - palabras_excluidas
        palabras_tecnicas_encontradas = palabras_filtradas.intersection(palabras_tecnicas)
        return palabras_tecnicas_encontradas if palabras_tecnicas_encontradas else palabras_filtradas
    
    # score acumulado (0-100)
    score = 0
    red_lower = egresado.red.lower()
    empleo_perfil_lower = empleo.perfil_requerido.lower()
    
    # Match exacto = 100 puntos (cuando la 'red' del egresado coincide
    # exactamente con el 'perfil_requerido' del empleo)
    if red_lower == empleo_perfil_lower:
        score = 100
    else:
        # Calcular compatibilidad por palabras
        palabras_red_egresado = filtrar_palabras_relevantes(egresado.red)
        palabras_perfil_egresado = filtrar_palabras_relevantes(egresado.perfil)
        palabras_empleo_perfil = filtrar_palabras_relevantes(empleo.perfil_requerido)
        palabras_titulo = filtrar_palabras_relevantes(empleo.titulo)
        
        palabras_egresado_todas = palabras_red_egresado.union(palabras_perfil_egresado)
        
    # Solo calculamos pesos si el egresado tiene palabras relevantes
    if palabras_egresado_todas:
            # Scoring con pesos
            # Coincidencias entre la 'red' del egresado y el perfil requerido
            # reciben peso alto (40 puntos por coincidencia)
            coincidencias_red = len(palabras_red_egresado.intersection(palabras_empleo_perfil))
            score += coincidencias_red * 40
            
            # Coincidencias entre el perfil del egresado y el perfil requerido
            # tienen peso intermedio (30 puntos por coincidencia)
            coincidencias_perfil_req = len(palabras_perfil_egresado.intersection(palabras_empleo_perfil))
            score += coincidencias_perfil_req * 30
            
            # Coincidencias entre el perfil del egresado y el título del empleo
            # tienen peso menor (20 puntos por coincidencia)
            coincidencias_titulo = len(palabras_perfil_egresado.intersection(palabras_titulo))
            score += coincidencias_titulo * 20
    
    return min(score, 100)

# =============================================
# ENDPOINTS
# =============================================
@app.route("/", methods=["GET"])
def home():
    """Endpoint de bienvenida"""
    return jsonify({
        "msg": "Bienvenido a PilAPE API",
        "version": "2.0 - Vercel Optimized",
        "endpoints": [
            "POST /login - Autenticación",
            "GET /trabajos - Obtener trabajos (requiere token)",
            "GET /health - Estado de la API"
        ]
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0"
    })

@app.route("/login", methods=["POST"])
def login():
    """Autenticación de egresados"""
    try:
        data = request.json
        if not data:
            return jsonify({"msg": "Datos requeridos"}), 400
        
        cedula = data.get("cedula")
        ficha = data.get("ficha")
        
        if not cedula or not ficha:
            return jsonify({"msg": "Cédula y ficha son requeridos"}), 400

        # Buscar egresado
        egresado = next((e for e in egresados_data if e.cedula == cedula and e.ficha == ficha), None)
        if not egresado:
            return jsonify({"msg": "Credenciales inválidas"}), 401

        token = generar_token(egresado)

        return jsonify({
            "token": token,
            "red": egresado.red,
            "perfil": egresado.perfil,
            "nombre": egresado.nombre,
            "msg": "Login exitoso"
        })
        
    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500


# Debug endpoint para verificar datos cargados en este entrypoint (útil en Vercel)
@app.route('/debug-data', methods=['GET'])
def debug_data_index():
    try:
        egresados_sample = [
            {
                'cedula': e.cedula,
                'ficha': e.ficha,
                'nombre': e.nombre,
                'red': e.red,
            }
            for e in egresados_data[:5]
        ]
        empleos_sample = [
            {
                'titulo': emp.titulo,
                'perfil_requerido': emp.perfil_requerido,
            }
            for emp in empleos_data[:5]
        ]
        logging.warning(f"[index.py] Egresados sample: {egresados_sample}")
        logging.warning(f"[index.py] Empleos sample: {empleos_sample}")
        return jsonify({
            'egresados_sample': egresados_sample,
            'empleos_sample': empleos_sample,
            'egresados_count': len(egresados_data),
            'empleos_count': len(empleos_data)
        })
    except Exception as e:
        logging.exception('Error generando debug-data')
        return jsonify({'msg': 'Error interno generando debug-data', 'error': str(e)}), 500

@app.route("/trabajos", methods=["GET"])
def get_trabajos():
    """Obtener trabajos filtrados por perfil"""
    try:
        auth_header = request.headers.get("Authorization")
        token = extraer_token_del_header(auth_header)
        
        if not token:
            return jsonify({"msg": "Token requerido"}), 401

        data = verificar_token(token)
        if not data:
            return jsonify({"msg": "Token inválido o expirado"}), 401

        # Obtener egresado
        cedula = data["cedula"]
        egresado = next((e for e in egresados_data if e.cedula == cedula), None)
        if not egresado:
            return jsonify({"msg": "Egresado no encontrado"}), 404

        # Calcular scores
        empleos_con_score = []
        # Recorremos todos los empleos y calculamos su score para este egresado.
        # Solo añadimos a la lista los empleos con score > 0 (alguna compatibilidad).
        for empleo in empleos_data:
            score = calcular_score_por_palabras_clave(egresado, empleo)
            if score > 0:
                empleo_dict = empleo.to_dict()
                empleo_dict["score_compatibilidad"] = score
                empleos_con_score.append(empleo_dict)

        # Ordenar por score (mayor -> menor). El empleo con mayor score queda
        # en la posición 0 de la lista.
        empleos_con_score.sort(key=lambda x: x["score_compatibilidad"], reverse=True)

        # Usar Cola FIFO para respuesta: encolamos en orden descendente
        # (mayor->menor) para que, al desencolar FIFO, el primer elemento
        # devuelto sea el de mayor score.
        cola = Cola()
        for empleo_dict in empleos_con_score:
            cola.encolar(empleo_dict)

        trabajos = []
        # Desencolamos hasta vaciar la cola; popleft() devuelve primero el
        # elemento que entró (empleo con mayor score)
        while not cola.esta_vacia():
            trabajos.append(cola.desencolar())

        return jsonify({
            "trabajos": trabajos,
            "total": len(trabajos),
            "red": data["red"],
            "perfil": data["perfil"],
            "algoritmo": "score_por_palabras_clave_simplificado"
        })
        
    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500

# =============================================
# CONFIGURACIÓN PARA VERCEL
# =============================================
# Variable requerida por Vercel
application = app

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)