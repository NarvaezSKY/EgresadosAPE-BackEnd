"""
Rutas y endpoints de la API
"""
from flask import request, jsonify
from .auth import generar_token, verificar_token, extraer_token_del_header, autenticar_egresado
from .models import egresados_data, empleos_data, Pila


def init_routes(app):
    """
    Inicializa todas las rutas de la aplicación
    
    Args:
        app: Instancia de la aplicación Flask
    """
    #==============================
    # Rutas de autenticación        
    #==============================
    @app.route("/login", methods=["POST"])
    def login():
        """
        Endpoint para autenticación de egresados
        
        Expects:
            JSON body con cedula y ficha
        
        Returns:
            JSON: Token JWT y datos del egresado si es exitoso
        """
        try:
            data = request.json
            if not data:
                return jsonify({"msg": "Datos requeridos"}), 400
            
            cedula = data.get("cedula")
            ficha = data.get("ficha")
            
            if not cedula or not ficha:
                return jsonify({"msg": "Cédula y ficha son requeridos"}), 400

            # Validar egresado
            egresado = autenticar_egresado(cedula, ficha, egresados_data)
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
            return jsonify({"msg": "Error interno del servidor"}), 500
        
    #==============================
    # Rutas de empleos            
    #==============================
    # Función para calcular score de compatibilidad    

    def calcular_score_por_palabras_clave(egresado, empleo):
        """
        Calcula el score de compatibilidad basado en palabras clave relevantes
        
        Args:
            egresado (Egresado): Objeto egresado con red y perfil descriptivo
            empleo (Empleo): Objeto empleo a evaluar
        
        Returns:
            int: Score de compatibilidad (0-100)
        """
        # Palabras irrelevantes a excluir (conectores, artículos, preposiciones)
        palabras_excluidas = {
            'de', 'del', 'la', 'el', 'los', 'las', 'en', 'con', 'por', 'para', 'y', 'o', 'un', 'una', 
            'este', 'esta', 'ese', 'esa', 'su', 'sus', 'se', 'que', 'es', 'son', 'como', 'más', 'muy',
            'al', 'le', 'lo', 'te', 'me', 'nos', 'les', 'pero', 'sino', 'aunque', 'porque', 'cuando',
            'donde', 'quien', 'cual', 'cuales', 'todo', 'toda', 'todos', 'todas', 'otro', 'otra', 'otros',
            'otras', 'mismo', 'misma', 'mismos', 'mismas', 'tanto', 'tanta', 'tantos', 'tantas'
        }
        
        # Palabras técnicas y profesionales relevantes por categorías
        palabras_tecnicas = {
            # INFORMÁTICA, DISEÑO Y DESARROLLO DE SOFTWARE
            'software', 'desarrollo', 'programacion', 'informatica', 'diseño', 'sistemas', 'aplicaciones',
            'web', 'movil', 'frontend', 'backend', 'fullstack', 'digital',
            
            # ACTIVIDAD FÍSICA, RECREACIÓN Y DEPORTE
            'deportes', 'fisica', 'entrenamiento', 'gimnasio', 'fitness',
            'terapia', 'rehabilitacion', 'nutricion', 'educacion',
            
            # AGRÍCOLA
            'agricola', 'agricultura', 'cultivos', 'agronomia','campo',
            'cosecha', 'ganaderia', 'veterinaria', 'agroindustria',
            
            # AMBIENTAL
            'ambiental', 'medio', 'ambiente', 'ecologia', 'sostenibilidad', 'conservacion', 'recursos',
            'naturales', 'biodiversidad', 'contaminacion', 'reciclaje', 'energia', 'renovable',
            
            # ARTES Y OFICIOS
            'artes', 'oficios', 'artesanias', 'manualidades', 'creatividad', 'pintura',
            'textil', 'madera', 'metal', 'joyeria', 'decoracion',
            
            # COMERCIO Y VENTAS
            'comercio', 'ventas', 'marketing', 'publicidad', 'mercadeo', 'distribucion',
            'atencion', 'cliente', 'negociacion', 'productos', 'servicios', 'logistica',
            
            # CONSTRUCCIÓN
            'construccion', 'edificacion', 'arquitectura', 'civil', 'estructural', 'obra',
            'proyecto', 'planos', 'materiales', 'supervision', 'acabados', 'instalaciones',
            
            # ELECTRÓNICA Y AUTOMATIZACIÓN
            'electronica', 'automatizacion', 'control', 'industrial', 'robotica', 'sensores',
            'circuitos', 'microcontroladores', 'instrumentacion', 'mantenimiento',
            
            # GESTIÓN
            'gestion', 'administracion', 'management', 'direccion', 'coordinacion', 'planificacion',
            'organizacion', 'liderazgo', 'proyectos', 'procesos', 'calidad', 'estrategia',
            
            # HOTELERÍA Y TURISMO
            'hoteleria', 'turismo', 'hospitalidad', 'servicios', 'eventos', 'gastronomia',
            'recepcion', 'reservas', 'entretenimiento',
            
            # MECÁNICA INDUSTRIAL
            'mecanica', 'industrial', 'maquinaria', 'equipos', 'mantenimiento', 'reparacion',
            'soldadura', 'torneria', 'fresadora', 'hidraulica', 'neumatica', 'produccion',
            
            # SALUD
            'salud', 'medicina', 'enfermeria', 'terapia', 'rehabilitacion', 'farmacia',
            'laboratorio', 'clinico', 'diagnostico', 'tratamiento', 'cuidado', 'paciente',

        }
        
        # Función para filtrar palabras relevantes
        def filtrar_palabras_relevantes(texto):
            """Filtra palabras relevantes excluyendo conectores y priorizando términos técnicos"""
            palabras = set(texto.lower().split())
            # Remover palabras excluidas
            palabras_filtradas = palabras - palabras_excluidas
            # Priorizar palabras técnicas
            palabras_tecnicas_encontradas = palabras_filtradas.intersection(palabras_tecnicas)
            # Si hay palabras técnicas, usarlas; sino, usar todas las filtradas
            return palabras_tecnicas_encontradas if palabras_tecnicas_encontradas else palabras_filtradas
        
        score = 0
        
        # Convertir a minúsculas para comparación
        red_lower = egresado.red.lower()
        perfil_egresado_lower = egresado.perfil.lower()
        empleo_perfil_lower = empleo.perfil_requerido.lower()
        
        # Match exacto de la red = 100 puntos (máxima prioridad)
        if red_lower == empleo_perfil_lower:
            score = 100
        else:
            # Obtener palabras relevantes del egresado
            palabras_red_egresado = filtrar_palabras_relevantes(egresado.red)
            palabras_perfil_egresado = filtrar_palabras_relevantes(egresado.perfil)
            
            # Obtener palabras relevantes del empleo
            palabras_empleo_perfil = filtrar_palabras_relevantes(empleo.perfil_requerido)
            palabras_titulo = filtrar_palabras_relevantes(empleo.titulo)
            palabras_descripcion = filtrar_palabras_relevantes(empleo.descripcion)
            
            # Combinar palabras del egresado para matching
            palabras_egresado_todas = palabras_red_egresado.union(palabras_perfil_egresado)
            
            # Solo calcular score si el egresado tiene palabras relevantes
            if palabras_egresado_todas:
                # 1. Match de red con perfil requerido del empleo (peso muy alto)
                coincidencias_red = len(palabras_red_egresado.intersection(palabras_empleo_perfil))
                score += coincidencias_red * 40
                
                # 2. Match del perfil descriptivo con perfil requerido (peso alto)
                coincidencias_perfil_req = len(palabras_perfil_egresado.intersection(palabras_empleo_perfil))
                score += coincidencias_perfil_req * 30
                
                # 3. Match del perfil descriptivo con título del empleo (peso medio)
                coincidencias_titulo = len(palabras_perfil_egresado.intersection(palabras_titulo))
                score += coincidencias_titulo * 20
                
                # 4. Match del perfil descriptivo con descripción (peso bajo)
                coincidencias_descripcion = len(palabras_perfil_egresado.intersection(palabras_descripcion))
                score += coincidencias_descripcion * 10
        
        # Limitar score máximo a 100
        return min(score, 100)

    @app.route("/trabajos", methods=["GET"])
    def get_trabajos():
        """
        Endpoint para obtener trabajos filtrados por perfil del usuario autenticado
        
        Headers:
            Authorization: Bearer <token>
        
        Returns:
            JSON: Lista de trabajos disponibles para el perfil del usuario ordenados por compatibilidad
        """
        try:
            auth_header = request.headers.get("Authorization")
            token = extraer_token_del_header(auth_header)
            
            if not token:
                return jsonify({"msg": "Token requerido"}), 401

            data = verificar_token(token)
            if not data:
                return jsonify({"msg": "Token inválido o expirado"}), 401

            # Obtener información del egresado desde el token
            cedula = data["cedula"]
            red = data["red"]
            perfil_descriptivo = data["perfil"]
            
            # Buscar el egresado completo (para tener acceso a todo el objeto)
            egresado = next((e for e in egresados_data if e.cedula == cedula), None)
            if not egresado:
                return jsonify({"msg": "Egresado no encontrado"}), 404

            # Calcular scores para todos los empleos
            empleos_con_score = []
            for empleo in empleos_data:
                score = calcular_score_por_palabras_clave(egresado, empleo)
                
                # Solo incluir empleos con score > 0 (alguna compatibilidad)
                if score > 0:
                    empleo_dict = empleo.to_dict()
                    empleo_dict["score_compatibilidad"] = score
                    empleos_con_score.append(empleo_dict)

            # Ordenar por score de mayor a menor
            empleos_con_score.sort(key=lambda x: x["score_compatibilidad"], reverse=True)
            
            # Usar pila para la respuesta (manteniendo la lógica original pero con orden correcto)
            pila = Pila()
            # Meter los empleos en orden inverso para que salgan en el orden correcto
            for empleo_dict in reversed(empleos_con_score):
                pila.push(empleo_dict)

            # Convertir pila a lista para la respuesta
            trabajos = []
            while not pila.esta_vacia():
                trabajos.append(pila.pop())

            return jsonify({
                "trabajos": trabajos,
                "total": len(trabajos),
                "red": red,
                "perfil": perfil_descriptivo,
                "algoritmo": "score_por_palabras_clave_mejorado"
            })
            
        except Exception as e:
            return jsonify({"msg": "Error interno del servidor"}), 500

    @app.route("/", methods=["GET"])
    def home():
        """
        Endpoint de bienvenida
        """
        return jsonify({
            "msg": "Bienvenido a PilAPE API",
            "version": "1.0",
            "endpoints": [
                "POST /login - Autenticación",
                "GET /trabajos - Obtener trabajos (requiere token)"
            ]
        })

    @app.route("/health", methods=["GET"])
    def health_check():
        """
        Endpoint para verificar el estado de la API
        """
        return jsonify({
            "status": "healthy",
            "timestamp": "2025-09-18"
        })