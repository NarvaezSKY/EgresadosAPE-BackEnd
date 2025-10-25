"""
Script de prueba para el backend con ordenamiento por árbol
Verifica que la funcionalidad básica del árbol jerárquico funcione correctamente
"""

# Simular las clases sin importar Flask para pruebas básicas
class MockEgresado:
    def __init__(self, cedula, nombre, ficha, red, perfil, rol_principal, especializacion, tecnologias):
        self.cedula = cedula
        self.nombre = nombre
        self.ficha = ficha
        self.red = red
        self.perfil = perfil
        self.rol_principal = rol_principal
        self.especializacion = especializacion
        self.tecnologias = tecnologias

class MockEmpleo:
    def __init__(self, id, titulo, rol_requerido, especializacion_requerida, tecnologias_requeridas, prioridad_rol):
        self.id = id
        self.titulo = titulo
        self.rol_requerido = rol_requerido
        self.especializacion_requerida = especializacion_requerida
        self.tecnologias_requeridas = tecnologias_requeridas
        self.prioridad_rol = prioridad_rol
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "rol_requerido": self.rol_requerido,
            "especializacion_requerida": self.especializacion_requerida,
            "tecnologias_requeridas": self.tecnologias_requeridas,
            "prioridad_rol": self.prioridad_rol
        }

class NodoArbol:
    def __init__(self, valor, peso=1, padre=None):
        self.valor = valor
        self.peso = peso
        self.padre = padre
        self.hijos = []
    
    def agregar_hijo(self, hijo):
        hijo.padre = self
        self.hijos.append(hijo)
    
    def calcular_peso_total(self):
        peso_total = self.peso
        nodo_actual = self.padre
        while nodo_actual:
            peso_total += nodo_actual.peso
            nodo_actual = nodo_actual.padre
        return peso_total

class ArbolJerarquico:
    def __init__(self):
        self.raiz = NodoArbol("Software Development", peso=10)
        self._construir_arbol()
    
    def _construir_arbol(self):
        # Development Team
        dev_team = NodoArbol("Development Team", peso=10)
        self.raiz.agregar_hijo(dev_team)
        
        # Fullstack
        fullstack = NodoArbol("Fullstack", peso=9)
        dev_team.agregar_hijo(fullstack)
        
        # Frontend
        frontend = NodoArbol("Frontend", peso=8)
        fullstack.agregar_hijo(frontend)
        
        # Tecnologías Frontend
        for tech in ["HTML", "CSS", "JavaScript", "React", "Angular"]:
            tech_node = NodoArbol(tech, peso=7)
            frontend.agregar_hijo(tech_node)
        
        # Backend
        backend = NodoArbol("Backend", peso=8)
        fullstack.agregar_hijo(backend)
        
        # Tecnologías Backend
        for tech in ["Node.js", "Java", "Python", "Spring", "Django"]:
            tech_node = NodoArbol(tech, peso=7)
            backend.agregar_hijo(tech_node)
        
        # QA Tester
        qa_tester = NodoArbol("QA Tester", peso=8)
        self.raiz.agregar_hijo(qa_tester)
        
        # UX/UI Designer
        ux_ui = NodoArbol("UX/UI Designer", peso=8)
        self.raiz.agregar_hijo(ux_ui)
    
    def buscar_nodo(self, valor, nodo_inicio=None):
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
        score_total = 0
        
        # Matching por rol principal
        if egresado.rol_principal.lower() == empleo.rol_requerido.lower():
            nodo_rol = self.buscar_nodo(egresado.rol_principal)
            if nodo_rol:
                score_total += nodo_rol.peso * 50
                print(f"✓ Coincidencia de rol: {egresado.rol_principal} = +{nodo_rol.peso * 50}")
        
        # Matching por especialización
        if (egresado.especializacion and empleo.especializacion_requerida and 
            egresado.especializacion.lower() == empleo.especializacion_requerida.lower()):
            nodo_esp = self.buscar_nodo(egresado.especializacion)
            if nodo_esp:
                score_total += nodo_esp.peso * 30
                print(f"✓ Coincidencia de especialización: {egresado.especializacion} = +{nodo_esp.peso * 30}")
        
        # Matching por tecnologías
        tecnologias_egresado = [tech.lower() for tech in egresado.tecnologias] if egresado.tecnologias else []
        tecnologias_empleo = [tech.lower() for tech in empleo.tecnologias_requeridas] if empleo.tecnologias_requeridas else []
        
        coincidencias_tecnologicas = 0
        for tech_egresado in tecnologias_egresado:
            for tech_empleo in tecnologias_empleo:
                if tech_egresado == tech_empleo:
                    nodo_tech = self.buscar_nodo(tech_egresado)
                    if nodo_tech:
                        score_total += nodo_tech.peso * 15
                        coincidencias_tecnologicas += 1
                        print(f"✓ Coincidencia tecnológica: {tech_egresado} = +{nodo_tech.peso * 15}")
        
        # Bonificaciones por múltiples coincidencias
        if coincidencias_tecnologicas >= 3:
            score_total += 100
            print(f"✓ Bonificación por múltiples tecnologías: +100")
        elif coincidencias_tecnologicas >= 2:
            score_total += 50
            print(f"✓ Bonificación por buen dominio tecnológico: +50")
        
        # Ajuste por prioridad del rol
        if empleo.prioridad_rol == 1:
            score_total = int(score_total * 1.2)
            print(f"✓ Ajuste por alta prioridad: +20%")
        elif empleo.prioridad_rol == 2:
            score_total = int(score_total * 1.1)
            print(f"✓ Ajuste por prioridad media: +10%")
        
        score_final = min(score_total, 1000)
        return score_final

def test_arbol_jerarquico():
    """Función de prueba para verificar el funcionamiento del árbol"""
    print("=== PRUEBA DEL ÁRBOL JERÁRQUICO ===\n")
    
    # Crear instancia del árbol
    arbol = ArbolJerarquico()
    
    # Crear egresado de prueba
    egresado_test = MockEgresado(
        cedula="123",
        nombre="Ana Pérez",
        ficha="456",
        red="Software",
        perfil="Desarrolladora fullstack",
        rol_principal="Development Team",
        especializacion="Fullstack",
        tecnologias=["React", "Node.js", "PostgreSQL", "JavaScript"]
    )
    
    # Crear empleos de prueba
    empleos_test = [
        MockEmpleo(
            id=1,
            titulo="Desarrollador Full Stack Senior",
            rol_requerido="Development Team",
            especializacion_requerida="Fullstack",
            tecnologias_requeridas=["React", "Node.js", "PostgreSQL"],
            prioridad_rol=1
        ),
        MockEmpleo(
            id=2,
            titulo="Desarrollador Frontend React",
            rol_requerido="Development Team",
            especializacion_requerida="Frontend",
            tecnologias_requeridas=["React", "JavaScript"],
            prioridad_rol=2
        ),
        MockEmpleo(
            id=3,
            titulo="QA Tester Automatización",
            rol_requerido="QA Tester",
            especializacion_requerida="Automatización",
            tecnologias_requeridas=["Selenium", "Cypress"],
            prioridad_rol=1
        )
    ]
    
    print(f"Egresado: {egresado_test.nombre}")
    print(f"Rol: {egresado_test.rol_principal}")
    print(f"Especialización: {egresado_test.especializacion}")
    print(f"Tecnologías: {egresado_test.tecnologias}")
    print("\n" + "="*50 + "\n")
    
    # Calcular afinidades
    resultados = []
    for empleo in empleos_test:
        print(f"EVALUANDO: {empleo.titulo}")
        print(f"Rol requerido: {empleo.rol_requerido}")
        print(f"Especialización: {empleo.especializacion_requerida}")
        print(f"Tecnologías: {empleo.tecnologias_requeridas}")
        print(f"Prioridad: {empleo.prioridad_rol}")
        print()
        
        score = arbol.calcular_afinidad_egresado_empleo(egresado_test, empleo)
        
        empleo_dict = empleo.to_dict()
        empleo_dict["score_afinidad"] = score
        resultados.append(empleo_dict)
        
        print(f"SCORE FINAL: {score}")
        print("\n" + "-"*50 + "\n")
    
    # Ordenar resultados por score
    resultados_ordenados = sorted(resultados, key=lambda x: x["score_afinidad"], reverse=True)
    
    print("=== RESULTADOS ORDENADOS ===")
    for i, resultado in enumerate(resultados_ordenados, 1):
        print(f"{i}. {resultado['titulo']} - Score: {resultado['score_afinidad']}")
    
    print(f"\n✅ Prueba completada. El empleo más afín es: {resultados_ordenados[0]['titulo']}")
    return resultados_ordenados

if __name__ == "__main__":
    test_arbol_jerarquico()