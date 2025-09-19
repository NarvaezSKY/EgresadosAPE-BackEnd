"""
Modelos de datos para la aplicación
"""

class Egresado:
    """Modelo para representar un egresado"""
    
    def __init__(self, cedula, ficha, nombre, red, perfil):
        self.cedula = cedula
        self.ficha = ficha
        self.nombre = nombre
        self.red = red  # Red de conocimiento (ej: "Software", "Salud", etc.)
        self.perfil = perfil  # Descripción de capacidades del egresado
        
    def to_dict(self):
        """Convierte el egresado a diccionario"""
        return {
            "cedula": self.cedula,
            "ficha": self.ficha,
            "nombre": self.nombre,
            "red": self.red,
            "perfil": self.perfil
        }


class Empleo:
    """Modelo para representar una oportunidad de empleo"""
    
    def __init__(self, titulo, descripcion, salario, perfil_requerido):
        self.titulo = titulo
        self.descripcion = descripcion
        self.salario = salario
        self.perfil_requerido = perfil_requerido

    def to_dict(self):
        """Convierte el empleo a diccionario"""
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "salario": self.salario,
            "perfil_requerido": self.perfil_requerido
        }


class Pila:
    """Implementación de estructura de datos tipo pila (LIFO)"""
    
    def __init__(self):
        self.items = []

    def push(self, item):
        """Agrega un elemento al tope de la pila"""
        self.items.append(item)

    def pop(self):
        """Remueve y retorna el elemento del tope de la pila"""
        return self.items.pop() if not self.esta_vacia() else None

    def esta_vacia(self):
        """Verifica si la pila está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Retorna el tamaño de la pila"""
        return len(self.items)


# ===============================
# Datos simulados (en una app real estarían en una base de datos)
# ===============================
egresados_data = [
    Egresado("123", "456", "Ana Pérez", "Software", 
             "Desarrolla sistemas informáticos usando tecnologías web, bases de datos y programación orientada a objetos"),
    Egresado("124", "457", "Luis Gómez", "Contabilidad", 
             "Administra procesos financieros, contables y tributarios con análisis de costos y presupuestos empresariales"),
    Egresado("125", "458", "María Torres", "Actividad Física", 
             "Diseña programas de entrenamiento físico, rehabilitación deportiva y promoción de la salud corporal"),
    Egresado("126", "459", "Carlos Ruiz", "Agricultura", 
             "Maneja técnicas de cultivo agrícola, producción pecuaria y gestión sostenible de recursos del campo"),
    Egresado("127", "460", "Elena Vargas", "Ambiental", 
             "Implementa proyectos de conservación ambiental, sostenibilidad y manejo de recursos naturales"),
    Egresado("128", "461", "Diego Castro", "Artes y Oficios", 
             "Crea obras artísticas y artesanales usando técnicas tradicionales en madera, metal y diseño"),
    Egresado("129", "462", "Sofía Mendoza", "Comercio", 
             "Gestiona estrategias de ventas, marketing comercial y atención al cliente en diversos mercados"),
    Egresado("130", "463", "Ricardo López", "Construcción", 
             "Ejecuta proyectos de construcción civil, supervisión de obras y diseño arquitectónico"),
    Egresado("131", "464", "Camila Rojas", "Electrónica", 
             "Programa sistemas de automatización, control industrial y mantenimiento de equipos electrónicos"),
    Egresado("132", "465", "Andrés Herrera", "Gestión", 
             "Coordina procesos administrativos, liderazgo de equipos y planificación estratégica organizacional"),
    Egresado("133", "466", "Valentina Cruz", "Hotelería", 
             "Administra servicios hoteleros, turismo, gastronomía y organización de eventos especializados"),
    Egresado("134", "467", "Fernando Silva", "Mecánica Industrial", 
             "Opera maquinaria industrial, mantenimiento mecánico y control de procesos de producción"),
    Egresado("135", "468", "Isabella García", "Salud", 
             "Brinda atención médica, cuidados de enfermería, diagnóstico clínico y rehabilitación de pacientes"),
]

empleos_data = [
    # ===== INFORMÁTICA, DISEÑO Y DESARROLLO DE SOFTWARE =====
    Empleo("Desarrollador Python Backend", "Desarrollo de APIs REST y microservicios con Python", 3200000, "Software"),
    Empleo("Frontend Developer React", "Desarrollo de interfaces web modernas con React y TypeScript", 2800000, "Software"),
    Empleo("Diseñador UX/UI", "Diseño de experiencias digitales y interfaces de usuario", 2600000, "Software"),
    Empleo("Desarrollador Full Stack", "Desarrollo completo web frontend y backend", 3500000, "Software"),
    Empleo("Analista de Sistemas", "Análisis y diseño de sistemas informáticos empresariales", 2900000, "Software"),
    Empleo("Tester QA Automatización", "Pruebas automatizadas y control de calidad de software", 2400000, "Software"),
    Empleo("DevOps Engineer", "Administración de infraestructura cloud y CI/CD", 3800000, "Software"),
    Empleo("Desarrollador Mobile", "Aplicaciones móviles Android e iOS nativas", 3100000, "Software"),
    Empleo("Arquitecto de Software", "Diseño de arquitecturas escalables y robustas", 4200000, "Software"),
    Empleo("Especialista en Ciberseguridad", "Seguridad informática y protección de datos", 3600000, "Software"),
    Empleo("Data Scientist", "Análisis de datos y machine learning", 3900000, "Software"),
    Empleo("Administrador de Base de Datos", "Gestión y optimización de bases de datos SQL", 2700000, "Software"),
    
    # ===== ACTIVIDAD FÍSICA, RECREACIÓN Y DEPORTE =====
    Empleo("Entrenador Personal", "Entrenamiento físico personalizado y rutinas de ejercicio", 1800000, "Actividad Física"),
    Empleo("Fisioterapeuta Deportivo", "Rehabilitación y terapia física para deportistas", 2200000, "Actividad Física"),
    Empleo("Instructor de Gimnasio", "Clases grupales de fitness y acondicionamiento físico", 1600000, "Actividad Física"),
    Empleo("Coordinador Deportivo", "Organización de eventos y programas deportivos", 2000000, "Actividad Física"),
    Empleo("Nutricionista Deportivo", "Planes nutricionales para atletas y deportistas", 2100000, "Actividad Física"),
    Empleo("Profesor de Educación Física", "Enseñanza de actividades físicas y deportes", 1900000, "Actividad Física"),
    Empleo("Entrenador de Natación", "Enseñanza y entrenamiento en disciplinas acuáticas", 1700000, "Actividad Física"),
    Empleo("Terapeuta Ocupacional", "Rehabilitación funcional y terapia ocupacional", 2300000, "Actividad Física"),
    Empleo("Preparador Físico", "Acondicionamiento físico para equipos deportivos", 2400000, "Actividad Física"),
    Empleo("Instructor de Yoga", "Clases de yoga y técnicas de relajación", 1500000, "Actividad Física"),
    Empleo("Masajista Deportivo", "Masajes terapéuticos para recuperación deportiva", 1800000, "Actividad Física"),
    Empleo("Recreacionista", "Actividades recreativas y de tiempo libre", 1600000, "Actividad Física"),
    
    # ===== AGRÍCOLA =====
    Empleo("Ingeniero Agrónomo", "Supervisión de cultivos y técnicas de producción agrícola", 2800000, "Agricultura"),
    Empleo("Técnico en Cultivos", "Manejo técnico de cultivos y control de plagas", 2000000, "Agricultura"),
    Empleo("Veterinario Pecuario", "Atención veterinaria para ganado y animales de granja", 2600000, "Agricultura"),
    Empleo("Operador de Maquinaria Agrícola", "Manejo de tractores y equipos de campo", 1800000, "Agricultura"),
    Empleo("Supervisor de Cosecha", "Coordinación de actividades de recolección", 2200000, "Agricultura"),
    Empleo("Técnico en Riego", "Diseño e instalación de sistemas de irrigación", 2100000, "Agricultura"),
    Empleo("Especialista en Semillas", "Selección y mejoramiento genético de semillas", 2500000, "Agricultura"),
    Empleo("Administrador de Finca", "Gestión integral de propiedades rurales", 2700000, "Agricultura"),
    Empleo("Técnico en Fertilizantes", "Aplicación y control de nutrientes del suelo", 1900000, "Agricultura"),
    Empleo("Inspector de Calidad Agrícola", "Control de calidad en productos agropecuarios", 2300000, "Agricultura"),
    Empleo("Zootecnista", "Manejo y producción de animales de granja", 2400000, "Agricultura"),
    Empleo("Operador de Invernadero", "Cultivo controlado en ambientes protegidos", 1700000, "Agricultura"),
    
    # ===== AMBIENTAL =====
    Empleo("Ingeniero Ambiental", "Proyectos de conservación y gestión ambiental", 3000000, "Ambiental"),
    Empleo("Especialista en Sostenibilidad", "Implementación de prácticas sostenibles empresariales", 2800000, "Ambiental"),
    Empleo("Técnico en Tratamiento de Aguas", "Operación de plantas de tratamiento", 2200000, "Ambiental"),
    Empleo("Auditor Ambiental", "Evaluación de impacto ambiental en proyectos", 2600000, "Ambiental"),
    Empleo("Gestor de Residuos", "Manejo integral de residuos sólidos y reciclaje", 2100000, "Ambiental"),
    Empleo("Biólogo Conservacionista", "Conservación de ecosistemas y biodiversidad", 2500000, "Ambiental"),
    Empleo("Técnico en Energías Renovables", "Instalación y mantenimiento de sistemas solares", 2400000, "Ambiental"),
    Empleo("Consultor Ambiental", "Asesoría en normatividad y permisos ambientales", 2900000, "Ambiental"),
    Empleo("Operador de Reciclaje", "Clasificación y procesamiento de materiales reciclables", 1600000, "Ambiental"),
    Empleo("Educador Ambiental", "Programas de educación y conciencia ambiental", 1900000, "Ambiental"),
    Empleo("Monitor de Calidad del Aire", "Medición y análisis de contaminación atmosférica", 2300000, "Ambiental"),
    Empleo("Técnico Forestal", "Manejo y conservación de bosques", 2000000, "Ambiental"),
    
    # ===== ARTES Y OFICIOS =====
    Empleo("Artesano en Madera", "Creación de muebles y objetos decorativos en madera", 1800000, "Artes y Oficios"),
    Empleo("Diseñador Gráfico", "Diseño de material publicitario y corporativo", 2200000, "Artes y Oficios"),
    Empleo("Joyero Artesanal", "Diseño y elaboración de joyas artesanales", 2000000, "Artes y Oficios"),
    Empleo("Pintor Artístico", "Obras de arte y murales decorativos", 1600000, "Artes y Oficios"),
    Empleo("Ceramista", "Creación de piezas cerámicas artísticas y utilitarias", 1500000, "Artes y Oficios"),
    Empleo("Restaurador de Arte", "Restauración y conservación de obras artísticas", 2400000, "Artes y Oficios"),
    Empleo("Tapicero", "Tapizado y restauración de muebles", 1700000, "Artes y Oficios"),
    Empleo("Escultor", "Creación de esculturas en diversos materiales", 1900000, "Artes y Oficios"),
    Empleo("Decorador de Interiores", "Diseño y decoración de espacios interiores", 2300000, "Artes y Oficios"),
    Empleo("Trabajador del Metal", "Forja y trabajo artesanal en metales", 2100000, "Artes y Oficios"),
    Empleo("Diseñador Textil", "Creación de patrones y diseños para textiles", 2000000, "Artes y Oficios"),
    Empleo("Vitralista", "Diseño y elaboración de vitrales artísticos", 2200000, "Artes y Oficios"),
    
    # ===== COMERCIO Y VENTAS =====
    Empleo("Ejecutivo de Ventas", "Ventas B2B y desarrollo de cartera de clientes", 2500000, "Comercio"),
    Empleo("Representante Comercial", "Representación de productos en territorio asignado", 2200000, "Comercio"),
    Empleo("Gerente de Tienda", "Administración integral de punto de venta", 2800000, "Comercio"),
    Empleo("Asesor Comercial", "Asesoría y venta de productos especializados", 2000000, "Comercio"),
    Empleo("Coordinador de Marketing", "Estrategias de mercadeo y promoción", 2600000, "Comercio"),
    Empleo("Vendedor de Mostrador", "Atención directa al cliente en punto de venta", 1600000, "Comercio"),
    Empleo("Especialista en E-commerce", "Gestión de ventas online y plataformas digitales", 2400000, "Comercio"),
    Empleo("Merchandiser", "Exhibición y promoción de productos en puntos de venta", 1800000, "Comercio"),
    Empleo("Supervisor de Ventas", "Coordinación de equipos comerciales", 2700000, "Comercio"),
    Empleo("Analista de Mercados", "Investigación y análisis de tendencias comerciales", 2300000, "Comercio"),
    Empleo("Cajero Comercial", "Operaciones de caja y atención al cliente", 1500000, "Comercio"),
    Empleo("Promotor de Ventas", "Promoción directa de productos y servicios", 1700000, "Comercio"),
    
    # ===== CONSTRUCCIÓN =====
    Empleo("Ingeniero Civil", "Diseño y supervisión de obras civiles", 3500000, "Construcción"),
    Empleo("Maestro de Obra", "Coordinación de trabajos de construcción", 2500000, "Construcción"),
    Empleo("Arquitecto", "Diseño arquitectónico y planos de construcción", 3200000, "Construcción"),
    Empleo("Albañil Especializado", "Trabajos de mampostería y acabados", 2000000, "Construcción"),
    Empleo("Soldador Certificado", "Soldadura estructural y de acabados", 2200000, "Construcción"),
    Empleo("Electricista Constructor", "Instalaciones eléctricas residenciales y comerciales", 2300000, "Construcción"),
    Empleo("Plomero Industrial", "Instalaciones hidráulicas y sanitarias", 2100000, "Construcción"),
    Empleo("Operador de Maquinaria Pesada", "Manejo de excavadoras y equipos de construcción", 2400000, "Construcción"),
    Empleo("Supervisor de Seguridad", "Implementación de normas de seguridad en obra", 2600000, "Construcción"),
    Empleo("Topógrafo", "Levantamientos topográficos y geodésicos", 2700000, "Construcción"),
    Empleo("Pintor de Obra", "Acabados en pintura y revestimientos", 1800000, "Construcción"),
    Empleo("Carpintero", "Trabajos en madera y estructuras", 2000000, "Construcción"),
    
    # ===== ELECTRÓNICA Y AUTOMATIZACIÓN =====
    Empleo("Ingeniero Electrónico", "Diseño de circuitos y sistemas electrónicos", 3200000, "Electrónica"),
    Empleo("Técnico en Automatización", "Programación y mantenimiento de sistemas automatizados", 2600000, "Electrónica"),
    Empleo("Especialista en PLC", "Programación de controladores lógicos programables", 2800000, "Electrónica"),
    Empleo("Técnico en Instrumentación", "Calibración y mantenimiento de instrumentos", 2400000, "Electrónica"),
    Empleo("Programador de Microcontroladores", "Desarrollo de firmware para sistemas embebidos", 2900000, "Electrónica"),
    Empleo("Técnico en Robótica", "Mantenimiento y operación de sistemas robóticos", 2700000, "Electrónica"),
    Empleo("Especialista en Sensores", "Instalación y configuración de sistemas de sensores", 2500000, "Electrónica"),
    Empleo("Técnico en Control Industrial", "Mantenimiento de sistemas de control de procesos", 2600000, "Electrónica"),
    Empleo("Reparador de Equipos Electrónicos", "Diagnóstico y reparación de dispositivos electrónicos", 2000000, "Electrónica"),
    Empleo("Instalador de Sistemas", "Instalación de sistemas electrónicos y de control", 2200000, "Electrónica"),
    Empleo("Técnico en Telecomunicaciones", "Mantenimiento de redes y equipos de comunicación", 2400000, "Electrónica"),
    Empleo("Especialista en Domótica", "Sistemas inteligentes para edificios", 2800000, "Electrónica"),
    
    # ===== GESTIÓN =====
    Empleo("Gerente General", "Dirección estratégica y operativa de la empresa", 4500000, "Gestión"),
    Empleo("Coordinador de Proyectos", "Planificación y ejecución de proyectos empresariales", 2800000, "Gestión"),
    Empleo("Analista de Procesos", "Optimización y mejora de procesos organizacionales", 2600000, "Gestión"),
    Empleo("Supervisor de Calidad", "Implementación de sistemas de gestión de calidad", 2400000, "Gestión"),
    Empleo("Asistente de Gerencia", "Apoyo administrativo a la alta dirección", 2000000, "Gestión"),
    Empleo("Líder de Equipo", "Coordinación y liderazgo de grupos de trabajo", 2500000, "Gestión"),
    Empleo("Planificador Estratégico", "Desarrollo de planes estratégicos organizacionales", 3200000, "Gestión"),
    Empleo("Coordinador Administrativo", "Gestión de procesos administrativos internos", 2200000, "Gestión"),
    Empleo("Analista Organizacional", "Estudios de eficiencia y estructura organizacional", 2700000, "Gestión"),
    Empleo("Gestor de Recursos Humanos", "Administración del talento humano", 2900000, "Gestión"),
    Empleo("Supervisor Operativo", "Supervisión de operaciones diarias", 2300000, "Gestión"),
    Empleo("Especialista en Mejora Continua", "Implementación de metodologías de mejora", 2800000, "Gestión"),
    
    # ===== HOTELERÍA Y TURISMO =====
    Empleo("Gerente de Hotel", "Administración integral de establecimiento hotelero", 3500000, "Hotelería"),
    Empleo("Recepcionista Bilingüe", "Atención al huésped y servicios de recepción", 1800000, "Hotelería"),
    Empleo("Chef Ejecutivo", "Dirección de cocina y creación de menús", 3000000, "Hotelería"),
    Empleo("Guía Turístico", "Conducción de tours y actividades turísticas", 2000000, "Hotelería"),
    Empleo("Coordinador de Eventos", "Organización de eventos corporativos y sociales", 2400000, "Hotelería"),
    Empleo("Camarero de Restaurante", "Servicio de alimentos y bebidas", 1600000, "Hotelería"),
    Empleo("Ama de Llaves", "Supervisión de servicios de limpieza y mantenimiento", 1900000, "Hotelería"),
    Empleo("Bartender Especializado", "Preparación de cócteles y servicio de bar", 1800000, "Hotelería"),
    Empleo("Animador Turístico", "Entretenimiento y actividades para huéspedes", 1700000, "Hotelería"),
    Empleo("Coordinador de Reservas", "Gestión de reservas y disponibilidad", 2100000, "Hotelería"),
    Empleo("Sommelier", "Especialista en vinos y maridajes", 2500000, "Hotelería"),
    Empleo("Conserje", "Servicios especializados de atención al huésped", 2000000, "Hotelería"),
    
    # ===== MECÁNICA INDUSTRIAL =====
    Empleo("Ingeniero Mecánico", "Diseño y supervisión de sistemas mecánicos", 3400000, "Mecánica Industrial"),
    Empleo("Técnico en Mantenimiento", "Mantenimiento preventivo y correctivo de maquinaria", 2300000, "Mecánica Industrial"),
    Empleo("Operador de Torno CNC", "Mecanizado de precisión en torno computarizado", 2500000, "Mecánica Industrial"),
    Empleo("Soldador Industrial", "Soldadura especializada para industria pesada", 2400000, "Mecánica Industrial"),
    Empleo("Mecánico de Equipos Pesados", "Mantenimiento de maquinaria industrial", 2600000, "Mecánica Industrial"),
    Empleo("Técnico en Hidráulica", "Sistemas hidráulicos industriales", 2200000, "Mecánica Industrial"),
    Empleo("Operador de Fresadora", "Mecanizado en fresadoras industriales", 2300000, "Mecánica Industrial"),
    Empleo("Supervisor de Producción", "Coordinación de líneas de producción", 2800000, "Mecánica Industrial"),
    Empleo("Técnico en Neumática", "Sistemas neumáticos y de aire comprimido", 2100000, "Mecánica Industrial"),
    Empleo("Inspector de Calidad Mecánica", "Control de calidad en procesos mecánicos", 2400000, "Mecánica Industrial"),
    Empleo("Mecánico Automotriz Industrial", "Mantenimiento de flota vehicular industrial", 2200000, "Mecánica Industrial"),
    Empleo("Técnico en Refrigeración", "Sistemas de refrigeración y climatización industrial", 2500000, "Mecánica Industrial"),
    
    # ===== SALUD =====
    Empleo("Enfermero Profesional", "Atención directa al paciente y cuidados de enfermería", 2400000, "Salud"),
    Empleo("Auxiliar de Enfermería", "Apoyo en cuidados básicos y asistencia médica", 1800000, "Salud"),
    Empleo("Técnico de Laboratorio", "Análisis clínicos y pruebas diagnósticas", 2200000, "Salud"),
    Empleo("Fisioterapeuta", "Rehabilitación física y terapias especializadas", 2600000, "Salud"),
    Empleo("Farmaceuta", "Dispensación de medicamentos y atención farmacéutica", 2800000, "Salud"),
    Empleo("Técnico en Radiología", "Operación de equipos de diagnóstico por imágenes", 2500000, "Salud"),
    Empleo("Paramédico", "Atención prehospitalaria y emergencias médicas", 2300000, "Salud"),
    Empleo("Terapeuta Respiratorio", "Tratamientos respiratorios especializados", 2400000, "Salud"),
    Empleo("Auxiliar de Farmacia", "Apoyo en dispensación y atención al público", 1700000, "Salud"),
    Empleo("Técnico en Emergencias", "Atención en servicios de urgencias", 2200000, "Salud"),
    Empleo("Instrumentador Quirúrgico", "Asistencia en procedimientos quirúrgicos", 2700000, "Salud"),
    Empleo("Técnico en Órtesis", "Fabricación y adaptación de dispositivos ortopédicos", 2300000, "Salud"),
]