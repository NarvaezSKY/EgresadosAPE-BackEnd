"""
Modelos de datos para la aplicación - Versión árbol jerárquico
Solo empleos de desarrollo de software organizados según estructura de árbol
"""

# Importar las clases del backend principal
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class Egresado:
    """Modelo para representar un egresado con atributos jerárquicos"""
    
    def __init__(self, cedula, ficha, nombre, red, perfil, rol_principal, especializacion, tecnologias):
        self.cedula = cedula
        self.ficha = ficha
        self.nombre = nombre
        self.red = red
        self.perfil = perfil
        # Nuevos atributos para el árbol jerárquico
        self.rol_principal = rol_principal  # Development Team, QA Tester, UX/UI Designer
        self.especializacion = especializacion  # Frontend, Backend, Fullstack, etc.
        self.tecnologias = tecnologias  # Lista de tecnologías que maneja
        
    def to_dict(self):
        return {
            'cedula': self.cedula,
            'ficha': self.ficha,
            'nombre': self.nombre,
            'red': self.red,
            'perfil': self.perfil,
            'rol_principal': self.rol_principal,
            'especializacion': self.especializacion,
            'tecnologias': self.tecnologias
        }

class Empleo:
    """Modelo para representar una oportunidad de empleo de software"""
    
    def __init__(self, id, titulo, descripcion, perfil_requerido, salario, ubicacion, 
                 rol_requerido, especializacion_requerida, tecnologias_requeridas, prioridad_rol):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.perfil_requerido = perfil_requerido
        self.salario = salario
        self.ubicacion = ubicacion
        # Atributos específicos para el árbol jerárquico
        self.rol_requerido = rol_requerido
        self.especializacion_requerida = especializacion_requerida
        self.tecnologias_requeridas = tecnologias_requeridas
        self.prioridad_rol = prioridad_rol  # 1=alta, 2=media, 3=baja

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

# ===============================
# EGRESADOS CON PERFILES DE SOFTWARE
# ===============================
# Egresados organizados según la estructura del árbol jerárquico
egresados_data = [
    # ===== DEVELOPMENT TEAM - FULLSTACK =====
    Egresado(
        cedula="123", 
        ficha="456", 
        nombre="Ana Pérez", 
        red="Software", 
        perfil="Desarrolla sistemas web completos con experiencia en frontend y backend",
        rol_principal="Development Team",
        especializacion="Fullstack",
        tecnologias=["HTML", "CSS", "JavaScript", "React", "Node.js", "PostgreSQL"]
    ),
    
    Egresado(
        cedula="124", 
        ficha="457", 
        nombre="Luis Gómez", 
        red="Software", 
        perfil="Especialista en desarrollo full stack con Java y Angular",
        rol_principal="Development Team",
        especializacion="Fullstack",
        tecnologias=["Java", "Spring", "Angular", "MySQL", "JavaScript", "CSS"]
    ),
    
    # ===== DEVELOPMENT TEAM - FRONTEND =====
    Egresado(
        cedula="125", 
        ficha="458", 
        nombre="María Torres", 
        red="Software", 
        perfil="Desarrolladora frontend especializada en React y experiencia de usuario",
        rol_principal="Development Team",
        especializacion="Frontend",
        tecnologias=["React", "JavaScript", "HTML", "CSS", "Angular"]
    ),
    
    Egresado(
        cedula="126", 
        ficha="459", 
        nombre="Carlos Ruiz", 
        red="Software", 
        perfil="Desarrollador frontend con experiencia en Angular y Vue.js",
        rol_principal="Development Team",
        especializacion="Frontend",
        tecnologias=["Angular", "JavaScript", "HTML", "CSS", "React"]
    ),
    
    # ===== DEVELOPMENT TEAM - BACKEND =====
    Egresado(
        cedula="127", 
        ficha="460", 
        nombre="Elena Vargas", 
        red="Software", 
        perfil="Desarrolladora backend especializada en Python y microservicios",
        rol_principal="Development Team",
        especializacion="Backend",
        tecnologias=["Python", "Django", "PostgreSQL", "Node.js", "MongoDB"]
    ),
    
    Egresado(
        cedula="128", 
        ficha="461", 
        nombre="Diego Castro", 
        red="Software", 
        perfil="Desarrollador backend con experiencia en Java Spring y bases de datos",
        rol_principal="Development Team",
        especializacion="Backend",
        tecnologias=["Java", "Spring", "MySQL", "PostgreSQL", "Python"]
    ),
    
    # ===== QA TESTER =====
    Egresado(
        cedula="129", 
        ficha="462", 
        nombre="Sofía Mendoza", 
        red="Software", 
        perfil="Tester de calidad con experiencia en automatización y pruebas funcionales",
        rol_principal="QA Tester",
        especializacion="Automatización",
        tecnologias=["Selenium", "Cypress", "Jira", "Postman", "TestRail"]
    ),
    
    Egresado(
        cedula="130", 
        ficha="463", 
        nombre="Ricardo López", 
        red="Software", 
        perfil="Especialista en pruebas de software y gestión de calidad",
        rol_principal="QA Tester",
        especializacion="Tipos de pruebas",
        tecnologias=["Unitarias", "Funcionales", "Regresión", "Jira", "Selenium"]
    ),
    
    # ===== UX/UI DESIGNER =====
    Egresado(
        cedula="131", 
        ficha="464", 
        nombre="Camila Rojas", 
        red="Software", 
        perfil="Diseñadora UX/UI especializada en prototipado y experiencia de usuario",
        rol_principal="UX/UI Designer",
        especializacion="Prototipado",
        tecnologias=["Figma", "Adobe XD", "Wireframes", "Entrevistas", "Pruebas de usabilidad"]
    ),
    
    Egresado(
        cedula="132", 
        ficha="465", 
        nombre="Andrés Herrera", 
        red="Software", 
        perfil="Diseñador visual especializado en interfaces y sistemas de diseño",
        rol_principal="UX/UI Designer",
        especializacion="Diseño visual",
        tecnologias=["Figma", "Adobe XD", "Guías UI", "Tipografía", "Color"]
    ),
    
    # ===== DEVELOPMENT TEAM - BASE DE DATOS =====
    Egresado(
        cedula="133", 
        ficha="466", 
        nombre="Valentina Cruz", 
        red="Software", 
        perfil="Especialista en bases de datos y arquitectura de datos",
        rol_principal="Development Team",
        especializacion="Base de Datos",
        tecnologias=["PostgreSQL", "MySQL", "MongoDB", "Firebase", "Python"]
    ),
    
    Egresado(
        cedula="134", 
        ficha="467", 
        nombre="Fernando Silva", 
        red="Software", 
        perfil="Desarrollador fullstack con énfasis en gestión de datos",
        rol_principal="Development Team",
        especializacion="Fullstack",
        tecnologias=["MongoDB", "Node.js", "React", "Firebase", "JavaScript"]
    ),
]

# ===============================
# EMPLEOS EXCLUSIVAMENTE DE SOFTWARE
# ===============================
# Empleos organizados según la estructura del árbol jerárquico mostrado en la imagen
empleos_data = [
    # ===== EMPLEOS PARA DEVELOPMENT TEAM - FULLSTACK =====
    Empleo(
        id=1,
        titulo="Desarrollador Full Stack Senior",
        descripcion="Desarrollo completo de aplicaciones web usando React, Node.js y PostgreSQL",
        perfil_requerido="Desarrollador con experiencia en frontend y backend",
        salario=4500000,
        ubicacion="Bogotá",
        rol_requerido="Development Team",
        especializacion_requerida="Fullstack",
        tecnologias_requeridas=["React", "Node.js", "PostgreSQL", "JavaScript"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=2,
        titulo="Desarrollador Full Stack Java",
        descripcion="Desarrollo de aplicaciones empresariales con Java Spring y Angular",
        perfil_requerido="Desarrollador Java con conocimientos en frontend",
        salario=4200000,
        ubicacion="Medellín", 
        rol_requerido="Development Team",
        especializacion_requerida="Fullstack",
        tecnologias_requeridas=["Java", "Spring", "Angular", "MySQL"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=3,
        titulo="Desarrollador Full Stack Python",
        descripcion="Desarrollo de plataformas web con Django y React",
        perfil_requerido="Desarrollador Python con experiencia frontend",
        salario=3900000,
        ubicacion="Cali",
        rol_requerido="Development Team",
        especializacion_requerida="Fullstack",
        tecnologias_requeridas=["Python", "Django", "React", "PostgreSQL"],
        prioridad_rol=2  # Media prioridad
    ),
    
    # ===== EMPLEOS PARA DEVELOPMENT TEAM - FRONTEND =====
    Empleo(
        id=4,
        titulo="Desarrollador Frontend React Senior",
        descripcion="Desarrollo de interfaces de usuario modernas con React y TypeScript",
        perfil_requerido="Especialista en desarrollo frontend",
        salario=3800000,
        ubicacion="Bogotá",
        rol_requerido="Development Team",
        especializacion_requerida="Frontend",
        tecnologias_requeridas=["React", "JavaScript", "HTML", "CSS"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=5,
        titulo="Desarrollador Frontend Angular",
        descripcion="Creación de aplicaciones web SPA con Angular y Material Design",
        perfil_requerido="Desarrollador con experiencia en Angular",
        salario=3500000,
        ubicacion="Medellín",
        rol_requerido="Development Team",
        especializacion_requerida="Frontend",
        tecnologias_requeridas=["Angular", "JavaScript", "HTML", "CSS"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=6,
        titulo="Desarrollador Frontend Vue.js",
        descripcion="Desarrollo de interfaces interactivas con Vue.js",
        perfil_requerido="Desarrollador frontend con conocimientos en Vue",
        salario=3300000,
        ubicacion="Cartagena",
        rol_requerido="Development Team",
        especializacion_requerida="Frontend",
        tecnologias_requeridas=["JavaScript", "HTML", "CSS", "React"],  # React como alternativa
        prioridad_rol=3  # Baja prioridad
    ),
    
    # ===== EMPLEOS PARA DEVELOPMENT TEAM - BACKEND =====
    Empleo(
        id=7,
        titulo="Desarrollador Backend Python Senior",
        descripcion="Desarrollo de APIs y microservicios con Python y Django",
        perfil_requerido="Especialista en desarrollo backend",
        salario=4000000,
        ubicacion="Bogotá",
        rol_requerido="Development Team",
        especializacion_requerida="Backend",
        tecnologias_requeridas=["Python", "Django", "PostgreSQL"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=8,
        titulo="Desarrollador Backend Java Spring",
        descripcion="Desarrollo de servicios empresariales con Java Spring Boot",
        perfil_requerido="Desarrollador Java con experiencia en Spring",
        salario=4100000,
        ubicacion="Medellín",
        rol_requerido="Development Team",
        especializacion_requerida="Backend",
        tecnologias_requeridas=["Java", "Spring", "MySQL"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=9,
        titulo="Desarrollador Backend Node.js",
        descripcion="Desarrollo de APIs REST con Node.js y Express",
        perfil_requerido="Desarrollador JavaScript backend",
        salario=3700000,
        ubicacion="Cali",
        rol_requerido="Development Team",
        especializacion_requerida="Backend",
        tecnologias_requeridas=["Node.js", "JavaScript", "MongoDB"],
        prioridad_rol=2  # Media prioridad
    ),
    
    # ===== EMPLEOS PARA DEVELOPMENT TEAM - BASE DE DATOS =====
    Empleo(
        id=10,
        titulo="Especialista en Bases de Datos PostgreSQL",
        descripcion="Administración y optimización de bases de datos PostgreSQL",
        perfil_requerido="Especialista en gestión de bases de datos",
        salario=3600000,
        ubicacion="Bogotá",
        rol_requerido="Development Team",
        especializacion_requerida="Base de Datos",
        tecnologias_requeridas=["PostgreSQL", "Python"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=11,
        titulo="Desarrollador de Bases de Datos NoSQL",
        descripcion="Desarrollo con MongoDB y Firebase para aplicaciones modernas",
        perfil_requerido="Desarrollador con experiencia en NoSQL",
        salario=3400000,
        ubicacion="Medellín",
        rol_requerido="Development Team",
        especializacion_requerida="Base de Datos",
        tecnologias_requeridas=["MongoDB", "Firebase", "Node.js"],
        prioridad_rol=3  # Baja prioridad
    ),
    
    # ===== EMPLEOS PARA QA TESTER =====
    Empleo(
        id=12,
        titulo="QA Tester Automatización Senior",
        descripcion="Automatización de pruebas con Selenium y Cypress",
        perfil_requerido="Tester con experiencia en automatización",
        salario=3200000,
        ubicacion="Bogotá",
        rol_requerido="QA Tester",
        especializacion_requerida="Automatización",
        tecnologias_requeridas=["Selenium", "Cypress", "Jira"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=13,
        titulo="QA Tester Funcional",
        descripcion="Ejecución de pruebas funcionales y de regresión",
        perfil_requerido="Tester con experiencia en pruebas manuales",
        salario=2800000,
        ubicacion="Medellín",
        rol_requerido="QA Tester",
        especializacion_requerida="Tipos de pruebas",
        tecnologias_requeridas=["Funcionales", "Regresión", "Jira"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=14,
        titulo="QA Tester Mobile",
        descripcion="Pruebas de aplicaciones móviles con Appium",
        perfil_requerido="Tester especializado en aplicaciones móviles",
        salario=3000000,
        ubicacion="Cali",
        rol_requerido="QA Tester",
        especializacion_requerida="Automatización",
        tecnologias_requeridas=["Appium", "Selenium", "Postman"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=15,
        titulo="QA Tester de Performance",
        descripcion="Pruebas de rendimiento y carga de aplicaciones",
        perfil_requerido="Tester con experiencia en pruebas de performance",
        salario=3300000,
        ubicacion="Bogotá",
        rol_requerido="QA Tester",
        especializacion_requerida="Tipos de pruebas",
        tecnologias_requeridas=["Unitarias", "Funcionales", "Postman"],
        prioridad_rol=3  # Baja prioridad
    ),
    
    # ===== EMPLEOS PARA UX/UI DESIGNER =====
    Empleo(
        id=16,
        titulo="UX/UI Designer Senior",
        descripcion="Diseño de experiencias de usuario y prototipado con Figma",
        perfil_requerido="Diseñador con experiencia en UX/UI",
        salario=3500000,
        ubicacion="Bogotá",
        rol_requerido="UX/UI Designer",
        especializacion_requerida="Prototipado",
        tecnologias_requeridas=["Figma", "Adobe XD", "Wireframes"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=17,
        titulo="Diseñador de Interfaces UI",
        descripcion="Creación de interfaces visuales y sistemas de diseño",
        perfil_requerido="Diseñador especializado en interfaces",
        salario=3200000,
        ubicacion="Medellín",
        rol_requerido="UX/UI Designer",
        especializacion_requerida="Diseño visual",
        tecnologias_requeridas=["Figma", "Guías UI", "Tipografía", "Color"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=18,
        titulo="UX Researcher",
        descripcion="Investigación de usuarios y pruebas de usabilidad",
        perfil_requerido="Investigador de experiencia de usuario",
        salario=3000000,
        ubicacion="Cali",
        rol_requerido="UX/UI Designer",
        especializacion_requerida="Investigación UX",
        tecnologias_requeridas=["Entrevistas", "Pruebas de usabilidad", "Figma"],
        prioridad_rol=2  # Media prioridad
    ),
    
    Empleo(
        id=19,
        titulo="Product Designer",
        descripcion="Diseño de productos digitales de extremo a extremo",
        perfil_requerido="Diseñador de productos con visión integral",
        salario=3800000,
        ubicacion="Bogotá",
        rol_requerido="UX/UI Designer",
        especializacion_requerida="Prototipado",
        tecnologias_requeridas=["Figma", "Adobe XD", "Entrevistas", "Wireframes"],
        prioridad_rol=1  # Alta prioridad
    ),
    
    Empleo(
        id=20,
        titulo="Visual Designer",
        descripcion="Diseño visual y creación de identidades digitales",
        perfil_requerido="Diseñador visual con experiencia digital",
        salario=2900000,
        ubicacion="Cartagena",
        rol_requerido="UX/UI Designer",
        especializacion_requerida="Diseño visual", 
        tecnologias_requeridas=["Adobe XD", "Tipografía", "Color", "Guías UI"],
        prioridad_rol=3  # Baja prioridad
    ),
]