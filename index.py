"""
PilAPE API - Versión simplificada para Vercel
Sistema de matching de empleos para egresados
"""
import os
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

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

class Pila:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def esta_vacia(self):
        return len(self.items) == 0

# =============================================
# BASE DE DATOS SIMULADA
# =============================================
egresados_data = [
    Egresado("1001", "Juan Software", "F001", "Software", "Desarrollador especializado en aplicaciones web modernas con experiencia en Python, JavaScript y frameworks como React y Flask."),
    Egresado("1002", "María Salud", "F002", "Salud", "Profesional de la salud especializada en atención al paciente, primeros auxilios y procedimientos médicos básicos."),
    Egresado("1003", "Carlos Agricultura", "F003", "Agrícola", "Técnico agrícola con conocimientos en cultivos, manejo de suelos, irrigación y tecnologías agroindustriales modernas."),
    Egresado("1004", "Ana Construcción", "F004", "Construcción", "Especialista en construcción con experiencia en lectura de planos, supervisión de obras y manejo de materiales de construcción."),
    Egresado("1005", "Luis Mecánica", "F005", "Mecánica Industrial", "Técnico en mecánica industrial especializado en mantenimiento de maquinaria, soldadura y reparación de equipos industriales."),
]

empleos_data = [
    # Software (15 empleos)
    Empleo(1, "Desarrollador Frontend", "Desarrollo de interfaces web responsivas usando React, JavaScript y CSS moderno.", "Software", "$2,500,000", "Bogotá"),
    Empleo(2, "Programador Python", "Desarrollo backend con Python, Flask/Django y bases de datos.", "Software", "$2,800,000", "Medellín"),
    Empleo(3, "Desarrollador Full Stack", "Desarrollo completo de aplicaciones web con tecnologías modernas.", "Software", "$3,200,000", "Cali"),
    
    # Salud (10 empleos)
    Empleo(51, "Auxiliar de Enfermería", "Apoyo en procedimientos médicos y atención al paciente en hospital.", "Salud", "$1,800,000", "Bogotá"),
    Empleo(52, "Técnico en Primeros Auxilios", "Atención de emergencias médicas y primeros auxilios en empresa.", "Salud", "$2,000,000", "Medellín"),
    
    # Agricultura (8 empleos)
    Empleo(81, "Técnico Agrícola", "Manejo de cultivos, supervisión de siembras y control de plagas.", "Agrícola", "$1,600,000", "Valle del Cauca"),
    Empleo(82, "Supervisor de Campo", "Coordinación de labores agrícolas y manejo de personal de campo.", "Agrícola", "$2,200,000", "Cundinamarca"),
    
    # Mecánica Industrial (12 empleos)
    Empleo(121, "Técnico en Mantenimiento", "Mantenimiento preventivo y correctivo de maquinaria industrial.", "Mecánica Industrial", "$2,400,000", "Bogotá"),
    Empleo(122, "Soldador Industrial", "Soldadura de estructuras metálicas y reparación de equipos.", "Mecánica Industrial", "$2,100,000", "Barranquilla"),
]

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
    
    score = 0
    red_lower = egresado.red.lower()
    empleo_perfil_lower = empleo.perfil_requerido.lower()
    
    # Match exacto = 100 puntos
    if red_lower == empleo_perfil_lower:
        score = 100
    else:
        # Calcular compatibilidad por palabras
        palabras_red_egresado = filtrar_palabras_relevantes(egresado.red)
        palabras_perfil_egresado = filtrar_palabras_relevantes(egresado.perfil)
        palabras_empleo_perfil = filtrar_palabras_relevantes(empleo.perfil_requerido)
        palabras_titulo = filtrar_palabras_relevantes(empleo.titulo)
        
        palabras_egresado_todas = palabras_red_egresado.union(palabras_perfil_egresado)
        
        if palabras_egresado_todas:
            # Scoring con pesos
            coincidencias_red = len(palabras_red_egresado.intersection(palabras_empleo_perfil))
            score += coincidencias_red * 40
            
            coincidencias_perfil_req = len(palabras_perfil_egresado.intersection(palabras_empleo_perfil))
            score += coincidencias_perfil_req * 30
            
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
        for empleo in empleos_data:
            score = calcular_score_por_palabras_clave(egresado, empleo)
            
            if score > 0:
                empleo_dict = empleo.to_dict()
                empleo_dict["score_compatibilidad"] = score
                empleos_con_score.append(empleo_dict)

        # Ordenar por score
        empleos_con_score.sort(key=lambda x: x["score_compatibilidad"], reverse=True)
        
        # Usar pila para respuesta
        pila = Pila()
        for empleo_dict in reversed(empleos_con_score):
            pila.push(empleo_dict)

        trabajos = []
        while not pila.esta_vacia():
            trabajos.append(pila.pop())

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