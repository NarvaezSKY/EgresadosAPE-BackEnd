# PilAPE API - Versión Árbol Jerárquico

Sistema de matching de empleos para egresados usando estructura de **árbol jerárquico** en lugar de colas FIFO.

## 🌳 Cambios Principales

### ❌ Sistema Anterior (FIFO)
- Usaba colas FIFO para ordenar empleos
- Ordenamiento simple por score de palabras clave
- Base de datos con empleos de múltiples sectores

### ✅ Sistema Nuevo (Árbol Jerárquico)
- **Estructura de árbol** para matching inteligente
- **Solo empleos de software** organizados jerárquicamente
- Ordenamiento basado en **afinidad por niveles**

## 🏗️ Estructura del Árbol

```
Software Development (Raíz)
├── Development Team (peso: 10)
│   ├── Fullstack (peso: 9)
│   │   ├── Frontend (peso: 8)
│   │   │   └── [HTML, CSS, JavaScript, React, Angular]
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
```

## 🧮 Algoritmo de Matching

### 1. **Coincidencia de Rol Principal** (Peso Alto)
- Si `egresado.rol_principal` == `empleo.rol_requerido`
- **Bonificación:** `peso_del_nodo × 50`
- Ejemplo: Development Team = +500 puntos

### 2. **Coincidencia de Especialización** (Peso Medio)
- Si `egresado.especializacion` == `empleo.especializacion_requerida`
- **Bonificación:** `peso_del_nodo × 30`
- Ejemplo: Fullstack = +270 puntos

### 3. **Coincidencias Tecnológicas** (Peso Acumulativo)
- Por cada tecnología en común
- **Bonificación:** `peso_del_nodo × 15`
- Ejemplo: React = +105 puntos

### 4. **Bonificaciones por Múltiples Coincidencias**
- **3+ tecnologías:** +100 puntos extra
- **2+ tecnologías:** +50 puntos extra

### 5. **Ajuste por Prioridad del Rol**
- **Alta prioridad (1):** +20% del score total
- **Media prioridad (2):** +10% del score total
- **Baja prioridad (3):** Sin ajuste

### 6. **Score Máximo**
- Limitado a **1000 puntos** máximo

## 📁 Archivos Nuevos

### `tree_backend.py`
Servidor backend completo con:
- Clases `NodoArbol` y `ArbolJerarquico` 
- Algoritmo de matching por árbol
- Endpoints actualizados para el nuevo sistema
- Comentarios detallados del funcionamiento

### `tree_models.py`
Base de datos actualizada con:
- Solo empleos de desarrollo de software
- Egresados con atributos jerárquicos
- 20 empleos organizados por la estructura del árbol
- 12 egresados con perfiles especializados

### `test_tree.py`
Script de prueba que verifica:
- Funcionamiento del árbol jerárquico
- Cálculo correcto de scores
- Ordenamiento por afinidad

## 🚀 Cómo Usar

### 1. Ejecutar Prueba
```bash
python test_tree.py
```

### 2. Ejecutar Servidor (requiere Flask y PyJWT)
```bash
python tree_backend.py
```

### 3. Endpoints Disponibles

- `GET /` - Información del sistema
- `GET /health` - Estado del servidor  
- `GET /arbol-info` - Estructura completa del árbol
- `POST /login` - Autenticación de egresados
- `GET /trabajos` - Empleos ordenados por árbol (requiere token)
- `GET /debug-data` - Datos de prueba

### 4. Ejemplo de Respuesta `/trabajos`
```json
{
  "trabajos": [
    {
      "id": 1,
      "titulo": "Desarrollador Full Stack Senior",
      "score_afinidad": 1000,
      "algoritmo_usado": "arbol_jerarquico",
      "rol_requerido": "Development Team",
      "especializacion_requerida": "Fullstack",
      "tecnologias_requeridas": ["React", "Node.js", "PostgreSQL"]
    }
  ],
  "algoritmo": "arbol_jerarquico_v3",
  "criterios_ordenamiento": [
    "Coincidencia de rol principal (peso alto)",
    "Coincidencia de especialización (peso medio)",
    "Coincidencias tecnológicas (peso acumulativo)",
    "Bonificaciones por múltiples coincidencias",
    "Ajuste por prioridad del rol en empresa"
  ]
}
```

## 🔍 Ejemplo de Matching

**Egresado:**
- Rol: "Development Team"
- Especialización: "Fullstack"  
- Tecnologías: ["React", "Node.js", "PostgreSQL", "JavaScript"]

**Empleo:**
- Rol requerido: "Development Team"
- Especialización: "Fullstack"
- Tecnologías: ["React", "Node.js", "PostgreSQL"]
- Prioridad: 1 (Alta)

**Cálculo:**
1. Rol coincide: +500 puntos
2. Especialización coincide: +270 puntos  
3. React coincide: +105 puntos
4. Node.js coincide: +105 puntos
5. Bonificación por 2+ tecnologías: +50 puntos
6. Ajuste alta prioridad (+20%): 1000 × 1.2 = **1000 puntos** (máximo)

## 💡 Ventajas del Nuevo Sistema

1. **Matching más inteligente** basado en jerarquías profesionales
2. **Especialización en software** para mejor precisión
3. **Peso por importancia** de cada nivel del árbol
4. **Bonificaciones progresivas** por múltiples coincidencias
5. **Priorización empresarial** según necesidades del empleador
6. **Escalabilidad** fácil para agregar nuevos roles/tecnologías

## 🛠️ Tecnologías

- **Python 3.8+**
- **Flask** (para API REST)
- **PyJWT** (para autenticación)
- **Estructura de datos:** Árbol n-ario personalizado
- **Algoritmo:** Matching jerárquico con pesos

---

*Este sistema reemplaza completamente el ordenamiento FIFO anterior, proporcionando un matching más preciso y relevante para empleos de desarrollo de software.*