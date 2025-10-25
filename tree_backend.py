"""
PilAPE API - Versión con ordenamiento por árbol jerárquico
Sistema de matching de empleos para egresados usando estructura de árbol
"""
import os
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import logging

# =============================================
# CONFIGURACIÓN
# =============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'desarrollo_secret_key_cambiar_en_produccion')

# =============================================
# MODELOS DE DATOS
# =============================================
class Egresado:
    def __init__(self, cedula, nombre, ficha, red, perfil, rol_principal, especializacion, tecnologias):
        self.cedula = cedula
        self.nombre = nombre
        self.ficha = ficha
        self.red = red
        self.perfil = perfil
        # Nuevos atributos jerárquicos para matching por árbol
        self.rol_principal = rol_principal  # Ej: "Development Team", "QA Tester", etc.
        self.especializacion = especializacion  # Ej: "Frontend", "Backend", "Fullstack"
        self.tecnologias = tecnologias  # Lista de tecnologías que maneja

class Empleo:
    def __init__(self, id, titulo, descripcion, perfil_requerido, salario, ubicacion, 
                 rol_requerido, especializacion_requerida, tecnologias_requeridas, prioridad_rol):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.perfil_requerido = perfil_requerido
        self.salario = salario
        self.ubicacion = ubicacion
        # Nuevos atributos jerárquicos para matching por árbol
        self.rol_requerido = rol_requerido  # Rol principal que busca la empresa
        self.especializacion_requerida = especializacion_requerida  # Especialización específica
        self.tecnologias_requeridas = tecnologias_requeridas  # Lista de tecnologías necesarias
        self.prioridad_rol = prioridad_rol  # Prioridad del rol (1=alta, 2=media, 3=baja)
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "perfil_requerido": self.perfil_requerido,
            "salario": self.salario,
            "ubicacion": self.ubicacion,
            "rol_requerido": self.rol_requerido,
            "especializacion_requerida": self.especializacion_requerida,
            "tecnologias_requeridas": self.tecnologias_requeridas,
            "prioridad_rol": self.prioridad_rol
        }

class NodoArbol:
    """
    Nodo del árbol jerárquico para ordenamiento de empleos.
    
    Cada nodo representa un nivel de la jerarquía:
    - Nivel 1: Rol principal (Development Team, QA Tester, UX/UI Designer)
    - Nivel 2: Especialización (Frontend, Backend, Fullstack, etc.)
    - Nivel 3: Tecnologías específicas
    
    El árbol define la afinidad entre el perfil del egresado y los empleos disponibles.
    """
    def __init__(self, valor, peso=1, padre=None):
        self.valor = valor  # El valor del nodo (rol, especialización, tecnología)
        self.peso = peso    # Peso de importancia en el matching (1-10)
        self.padre = padre  # Referencia al nodo padre
        self.hijos = []     # Lista de nodos hijos
        self.empleos_asociados = []  # Empleos que coinciden con este nodo
    
    def agregar_hijo(self, hijo):
        """Agrega un nodo hijo a este nodo"""
        hijo.padre = self
        self.hijos.append(hijo)
    
    def obtener_ruta_completa(self):
        """Obtiene la ruta completa desde la raíz hasta este nodo"""
        ruta = []
        nodo_actual = self
        while nodo_actual:
            ruta.append(nodo_actual.valor)
            nodo_actual = nodo_actual.padre
        return list(reversed(ruta))
    
    def calcular_peso_total(self):
        """Calcula el peso total acumulado desde la raíz"""
        peso_total = self.peso
        nodo_actual = self.padre
        while nodo_actual:
            peso_total += nodo_actual.peso
            nodo_actual = nodo_actual.padre
        return peso_total

class ArbolJerarquico:
    """
    Árbol jerárquico para organizar y ordenar empleos según afinidad.
    
    Estructura del árbol basada en la imagen:
    
    Raíz: Software Development
    ├── Development Team (peso: 10)
    │   ├── Fullstack (peso: 9)
    │   │   ├── Frontend (peso: 8)
    │   │   │   └── [HTML, CSS, JS, React, Angular]
    │   │   ├── Backend (peso: 8)
    │   │   │   └── [Node.js, Java, Python, Spring, Django]
    │   │   └── Base de Datos (peso: 8)
    │   │       └── [PostgreSQL, MySQL, MongoDB, Firebase]
    │   
    ├── QA Tester (peso: 8)
    │   ├── Tipos de pruebas (peso: 7)
    │   │   └── [Unitarias, Funcionales, Regresión, Exploratorias]
    │   ├── Automatización (peso: 7)
    │   │   └── [Selenium, Cypress, Postman, Appium]
    │   └── Gestión de pruebas (peso: 7)
    │       └── [Jira, TestRail, Zephyr]
    │
    └── UX/UI Designer (peso: 8)
        ├── Prototipado (peso: 7)
        │   └── [Figma, Adobe XD, Wireframes]
        ├── Diseño visual (peso: 7)
        │   └── [Guías UI, Tipografía, Color]
        └── Investigación UX (peso: 7)
            └── [Entrevistas, Pruebas de usabilidad]
    """
    
    def __init__(self):
        self.raiz = NodoArbol("Software Development", peso=10)
        self._construir_arbol()
    
    def _construir_arbol(self):
        """Construye la estructura completa del árbol jerárquico"""
        
        # ===== RAMA: DEVELOPMENT TEAM =====
        dev_team = NodoArbol("Development Team", peso=10)
        self.raiz.agregar_hijo(dev_team)
        
        # Desarrollador Fullstack
        fullstack = NodoArbol("Fullstack", peso=9)
        dev_team.agregar_hijo(fullstack)
        
        # Frontend
        frontend = NodoArbol("Frontend", peso=8)
        fullstack.agregar_hijo(frontend)
        
        # Tecnologías Frontend
        techs_frontend = ["HTML", "CSS", "JavaScript", "React", "Angular"]
        for tech in techs_frontend:
            tech_node = NodoArbol(tech, peso=7)
            frontend.agregar_hijo(tech_node)
        
        # Backend
        backend = NodoArbol("Backend", peso=8)
        fullstack.agregar_hijo(backend)
        
        # Tecnologías Backend
        techs_backend = ["Node.js", "Java", "Python", "Spring", "Django"]
        for tech in techs_backend:
            tech_node = NodoArbol(tech, peso=7)
            backend.agregar_hijo(tech_node)
        
        # Base de Datos
        bd = NodoArbol("Base de Datos", peso=8)
        fullstack.agregar_hijo(bd)
        
        # Tecnologías Base de Datos
        techs_bd = ["PostgreSQL", "MySQL", "MongoDB", "Firebase"]
        for tech in techs_bd:
            tech_node = NodoArbol(tech, peso=7)
            bd.agregar_hijo(tech_node)
        
        # ===== RAMA: QA TESTER =====
        qa_tester = NodoArbol("QA Tester", peso=8)
        self.raiz.agregar_hijo(qa_tester)
        
        # Tipos de pruebas
        tipos_pruebas = NodoArbol("Tipos de pruebas", peso=7)
        qa_tester.agregar_hijo(tipos_pruebas)
        
        pruebas = ["Unitarias", "Funcionales", "Regresión", "Exploratorias"]
        for prueba in pruebas:
            prueba_node = NodoArbol(prueba, peso=6)
            tipos_pruebas.agregar_hijo(prueba_node)
        
        # Automatización
        automatizacion = NodoArbol("Automatización", peso=7)
        qa_tester.agregar_hijo(automatizacion)
        
        herramientas_auto = ["Selenium", "Cypress", "Postman", "Appium"]
        for herramienta in herramientas_auto:
            herr_node = NodoArbol(herramienta, peso=6)
            automatizacion.agregar_hijo(herr_node)
        
        # Gestión de pruebas
        gestion_pruebas = NodoArbol("Gestión de pruebas", peso=7)
        qa_tester.agregar_hijo(gestion_pruebas)
        
        herramientas_gestion = ["Jira", "TestRail", "Zephyr"]
        for herramienta in herramientas_gestion:
            herr_node = NodoArbol(herramienta, peso=6)
            gestion_pruebas.agregar_hijo(herr_node)
        
        # ===== RAMA: UX/UI DESIGNER =====
        ux_ui = NodoArbol("UX/UI Designer", peso=8)
        self.raiz.agregar_hijo(ux_ui)
        
        # Prototipado
        prototipado = NodoArbol("Prototipado", peso=7)
        ux_ui.agregar_hijo(prototipado)
        
        herramientas_proto = ["Figma", "Adobe XD", "Wireframes"]
        for herramienta in herramientas_proto:
            herr_node = NodoArbol(herramienta, peso=6)
            prototipado.agregar_hijo(herr_node)
        
        # Diseño visual
        diseno_visual = NodoArbol("Diseño visual", peso=7)
        ux_ui.agregar_hijo(diseno_visual)
        
        elementos_diseno = ["Guías UI", "Tipografía", "Color"]
        for elemento in elementos_diseno:
            elem_node = NodoArbol(elemento, peso=6)
            diseno_visual.agregar_hijo(elem_node)
        
        # Investigación UX
        investigacion_ux = NodoArbol("Investigación UX", peso=7)
        ux_ui.agregar_hijo(investigacion_ux)
        
        metodos_investigacion = ["Entrevistas", "Pruebas de usabilidad"]
        for metodo in metodos_investigacion:
            metodo_node = NodoArbol(metodo, peso=6)
            investigacion_ux.agregar_hijo(metodo_node)
    
    def buscar_nodo(self, valor, nodo_inicio=None):
        """Busca un nodo por su valor en el árbol"""
        if nodo_inicio is None:
            nodo_inicio = self.raiz
        
        if nodo_inicio.valor.lower() == valor.lower():
            return nodo_inicio
        
        for hijo in nodo_inicio.hijos:
            resultado = self.buscar_nodo(valor, hijo)
            if resultado:
                return resultado
        
        return None
    
    def calcular_afinidad_egresado_empleo(self, egresado, empleo):
        """
        Calcula la afinidad entre un egresado y un empleo usando el árbol jerárquico.
        
        El algoritmo de matching funciona así:
        1. Busca coincidencias exactas en el rol principal (peso máximo)
        2. Busca coincidencias en especializaciones (peso medio)
        3. Busca coincidencias en tecnologías (peso acumulativo)
        4. Aplica bonificaciones por múltiples coincidencias
        5. Considera la prioridad del rol en la empresa
        
        Returns:
            int: Score de afinidad (0-1000)
        """
        score_total = 0
        
        # ===== MATCHING POR ROL PRINCIPAL =====
        # Si el rol del egresado coincide exactamente con el rol requerido del empleo
        if egresado.rol_principal.lower() == empleo.rol_requerido.lower():
            nodo_rol = self.buscar_nodo(egresado.rol_principal)
            if nodo_rol:
                # Bonificación alta por coincidencia exacta de rol
                score_total += nodo_rol.peso * 50
                logging.info(f"Coincidencia de rol: {egresado.rol_principal} = +{nodo_rol.peso * 50}")
        
        # ===== MATCHING POR ESPECIALIZACIÓN =====
        # Si la especialización del egresado coincide con la requerida
        if (egresado.especializacion and empleo.especializacion_requerida and 
            egresado.especializacion.lower() == empleo.especializacion_requerida.lower()):
            nodo_esp = self.buscar_nodo(egresado.especializacion)
            if nodo_esp:
                # Bonificación media por especialización
                score_total += nodo_esp.peso * 30
                logging.info(f"Coincidencia de especialización: {egresado.especializacion} = +{nodo_esp.peso * 30}")
        
        # ===== MATCHING POR TECNOLOGÍAS =====
        # Calcula coincidencias entre tecnologías del egresado y las requeridas
        tecnologias_egresado = [tech.lower() for tech in egresado.tecnologias] if egresado.tecnologias else []
        tecnologias_empleo = [tech.lower() for tech in empleo.tecnologias_requeridas] if empleo.tecnologias_requeridas else []
        
        coincidencias_tecnologicas = 0
        for tech_egresado in tecnologias_egresado:
            for tech_empleo in tecnologias_empleo:
                if tech_egresado == tech_empleo:
                    nodo_tech = self.buscar_nodo(tech_egresado)
                    if nodo_tech:
                        # Bonificación por cada tecnología coincidente
                        score_total += nodo_tech.peso * 15
                        coincidencias_tecnologicas += 1
                        logging.info(f"Coincidencia tecnológica: {tech_egresado} = +{nodo_tech.peso * 15}")
        
        # ===== BONIFICACIONES POR MÚLTIPLES COINCIDENCIAS =====
        # Bonificación extra si hay múltiples tecnologías en común
        if coincidencias_tecnologicas >= 3:
            score_total += 100  # Bonificación por dominio amplio
            logging.info(f"Bonificación por múltiples tecnologías: +100")
        elif coincidencias_tecnologicas >= 2:
            score_total += 50   # Bonificación por buen dominio
            logging.info(f"Bonificación por buen dominio tecnológico: +50")
        
        # ===== AJUSTE POR PRIORIDAD DEL ROL =====
        # Los roles con alta prioridad en la empresa reciben ajuste positivo
        if empleo.prioridad_rol == 1:  # Alta prioridad
            score_total = int(score_total * 1.2)  # +20%
            logging.info(f"Ajuste por alta prioridad: +20%")
        elif empleo.prioridad_rol == 2:  # Media prioridad
            score_total = int(score_total * 1.1)  # +10%
            logging.info(f"Ajuste por prioridad media: +10%")
        # Prioridad 3 (baja) no recibe ajuste
        
        # ===== LIMITACIÓN DE SCORE MÁXIMO =====
        score_final = min(score_total, 1000)  # Máximo 1000 puntos
        
        logging.info(f"Score final para {empleo.titulo}: {score_final}")
        return score_final

# =============================================
# INSTANCIA GLOBAL DEL ÁRBOL
# =============================================
arbol_jerarquico = ArbolJerarquico()

# =============================================
# BASE DE DATOS - SOLO EMPLEOS DE SOFTWARE
# =============================================
# Importar los datos actualizados de software development
from tree_models import egresados_data, empleos_data

# =============================================
# FUNCIONES DE AUTENTICACIÓN
# =============================================
def generar_token(egresado):
    """Genera token JWT para el egresado"""
    payload = {
        'cedula': egresado.cedula,
        'red': egresado.red,
        'perfil': egresado.perfil,
        'rol_principal': egresado.rol_principal,
        'especializacion': egresado.especializacion,
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
# ALGORITMO DE ORDENAMIENTO POR ÁRBOL
# =============================================
def ordenar_empleos_por_arbol(egresado, empleos):
    """
    Ordena los empleos usando el algoritmo de árbol jerárquico.
    
    Este método reemplaza completamente el sistema de colas FIFO.
    En su lugar, utiliza la estructura de árbol para:
    
    1. Calcular scores de afinidad basados en la jerarquía de roles/tecnologías
    2. Ordenar empleos de mayor a menor afinidad
    3. Devolver empleos ordenados por relevancia para el egresado
    
    Args:
        egresado: Objeto Egresado con perfil del usuario
        empleos: Lista de objetos Empleo disponibles
    
    Returns:
        list: Empleos ordenados por afinidad descendente
    """
    empleos_con_score = []
    
    logging.info(f"Iniciando ordenamiento por árbol para egresado: {egresado.nombre}")
    logging.info(f"Rol: {egresado.rol_principal}, Especialización: {egresado.especializacion}")
    logging.info(f"Tecnologías: {egresado.tecnologias}")
    
    # Calcular score de afinidad para cada empleo usando el árbol jerárquico
    for empleo in empleos:
        score = arbol_jerarquico.calcular_afinidad_egresado_empleo(egresado, empleo)
        
        if score > 0:  # Solo incluir empleos con alguna afinidad
            empleo_dict = empleo.to_dict()
            empleo_dict["score_afinidad"] = score
            empleo_dict["algoritmo_usado"] = "arbol_jerarquico"
            empleos_con_score.append(empleo_dict)
            
            logging.info(f"Empleo: {empleo.titulo} - Score: {score}")
    
    # Ordenar por score de afinidad (mayor a menor)
    # Este es el reemplazo directo del sistema de colas FIFO
    empleos_ordenados = sorted(empleos_con_score, 
                              key=lambda x: x["score_afinidad"], 
                              reverse=True)
    
    logging.info(f"Ordenamiento completado. {len(empleos_ordenados)} empleos relevantes encontrados.")
    
    return empleos_ordenados

# =============================================
# ENDPOINTS
# =============================================
@app.route("/", methods=["GET"])
def home():
    """Endpoint de bienvenida"""
    return jsonify({
        "msg": "PilAPE API - Ordenamiento por Árbol Jerárquico",
        "version": "3.0 - Tree-Based Matching",
        "algoritmo": "Árbol jerárquico de roles y tecnologías",
        "especialidad": "Empleos de desarrollo de software",
        "endpoints": [
            "POST /login - Autenticación",
            "GET /trabajos - Obtener trabajos ordenados por árbol (requiere token)",
            "GET /arbol-info - Información sobre la estructura del árbol",
            "GET /health - Estado de la API"
        ]
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0",
        "algoritmo": "arbol_jerarquico"
    })

@app.route("/arbol-info", methods=["GET"])
def arbol_info():
    """Información sobre la estructura del árbol jerárquico"""
    
    def nodo_to_dict(nodo, incluir_hijos=True):
        """Convierte un nodo del árbol a diccionario para JSON"""
        nodo_dict = {
            "valor": nodo.valor,
            "peso": nodo.peso,
            "peso_total": nodo.calcular_peso_total(),
            "ruta_completa": nodo.obtener_ruta_completa()
        }
        
        if incluir_hijos and nodo.hijos:
            nodo_dict["hijos"] = [nodo_to_dict(hijo, incluir_hijos=False) for hijo in nodo.hijos]
        
        return nodo_dict
    
    return jsonify({
        "estructura_arbol": nodo_to_dict(arbol_jerarquico.raiz),
        "total_nodos": len(list(_obtener_todos_los_nodos(arbol_jerarquico.raiz))),
        "roles_principales": [hijo.valor for hijo in arbol_jerarquico.raiz.hijos],
        "descripcion": "Árbol jerárquico para matching de empleos de software"
    })

def _obtener_todos_los_nodos(nodo):
    """Función auxiliar para obtener todos los nodos del árbol"""
    yield nodo
    for hijo in nodo.hijos:
        yield from _obtener_todos_los_nodos(hijo)

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
            "rol_principal": egresado.rol_principal,
            "especializacion": egresado.especializacion,
            "tecnologias": egresado.tecnologias,
            "nombre": egresado.nombre,
            "msg": "Login exitoso",
            "algoritmo": "arbol_jerarquico"
        })
        
    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500

@app.route("/trabajos", methods=["GET"])
def get_trabajos():
    """
    Obtener trabajos ordenados por árbol jerárquico.
    
    Este endpoint reemplaza completamente el sistema de colas FIFO.
    Ahora usa el árbol jerárquico para calcular afinidades y ordenar empleos.
    """
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

        # ===== ALGORITMO DE ORDENAMIENTO POR ÁRBOL =====
        # Reemplaza completamente el sistema anterior de colas FIFO
        trabajos_ordenados = ordenar_empleos_por_arbol(egresado, empleos_data)

        return jsonify({
            "trabajos": trabajos_ordenados,
            "total": len(trabajos_ordenados),
            "egresado": {
                "red": data["red"],
                "perfil": data["perfil"],
                "rol_principal": data.get("rol_principal", ""),
                "especializacion": data.get("especializacion", "")
            },
            "algoritmo": "arbol_jerarquico_v3",
            "descripcion": "Empleos ordenados por afinidad usando estructura de árbol jerárquico",
            "criterios_ordenamiento": [
                "Coincidencia de rol principal (peso alto)",
                "Coincidencia de especialización (peso medio)", 
                "Coincidencias tecnológicas (peso acumulativo)",
                "Bonificaciones por múltiples coincidencias",
                "Ajuste por prioridad del rol en empresa"
            ]
        })
        
    except Exception as e:
        logging.exception("Error en get_trabajos")
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500

# Debug endpoint para verificar datos cargados
@app.route('/debug-data', methods=['GET'])
def debug_data():
    try:
        egresados_sample = [
            {
                'cedula': e.cedula,
                'ficha': e.ficha,
                'nombre': e.nombre,
                'red': e.red,
                'rol_principal': e.rol_principal,
                'especializacion': e.especializacion,
                'tecnologias': e.tecnologias[:3] if e.tecnologias else []  # Solo las primeras 3
            }
            for e in egresados_data[:3]  # Solo los primeros 3 egresados
        ]
        empleos_sample = [
            {
                'titulo': emp.titulo,
                'rol_requerido': emp.rol_requerido,
                'especializacion_requerida': emp.especializacion_requerida,
                'tecnologias_requeridas': emp.tecnologias_requeridas[:3] if emp.tecnologias_requeridas else [],
                'prioridad_rol': emp.prioridad_rol
            }
            for emp in empleos_data[:5]  # Solo los primeros 5 empleos
        ]
        
        return jsonify({
            'algoritmo': 'arbol_jerarquico',
            'egresados_sample': egresados_sample,
            'empleos_sample': empleos_sample,
            'egresados_count': len(egresados_data),
            'empleos_count': len(empleos_data),
            'estructura_arbol': 'Ver /arbol-info para detalles completos'
        })
    except Exception as e:
        logging.exception('Error generando debug-data')
        return jsonify({'msg': 'Error interno generando debug-data', 'error': str(e)}), 500

# =============================================
# CONFIGURACIÓN PARA VERCEL
# =============================================
# Variable requerida por Vercel
application = app

if __name__ == "__main__":
    # Configurar logging para desarrollo
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)