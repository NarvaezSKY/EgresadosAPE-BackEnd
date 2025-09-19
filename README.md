# PilAPE Backend - API de Matching de Empleos 🚀

API REST desarrollada en Flask que implementa un sistema inteligente de matching entre egresados y empleos basado en compatibilidad de perfiles y palabras clave.

## 📋 Características

- ✅ **Autenticación JWT** con tokens de 2 horas de duración
- ✅ **Sistema de Scoring Inteligente** (0-100 puntos) basado en palabras clave técnicas
- ✅ **Filtrado de Ruido** - Excluye conectores y palabras irrelevantes
- ✅ **Estructura de Datos Pila** para organización de resultados
- ✅ **144+ Empleos Simulados** distribuidos en 12 categorías profesionales
- ✅ **Arquitectura Modular** con separación clara de responsabilidades

## 🛠️ Tecnologías

- **Backend**: Flask 3.1.2
- **Autenticación**: PyJWT 2.10.1
- **Variables de Entorno**: python-dotenv 1.1.1
- **Python**: 3.13+

## 📦 Estructura del Proyecto

```
pilapeback/
├── app/
│   ├── __init__.py          # Factory pattern de la aplicación Flask
│   ├── config.py            # Configuraciones y variables de entorno
│   ├── models.py            # Modelos de datos y base de datos simulada
│   ├── auth.py              # Manejo de autenticación JWT
│   └── routes.py            # Endpoints y lógica de negocio
├── main_refactorizado.py    # Punto de entrada principal
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (no incluido en Git)
├── swagger.yaml             # Documentación API (opcional)
└── README.md               # Este archivo
```

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/NarvaezSKY/EgresadosAPE-BackEnd.git
cd EgresadosAPE-BackEnd
```

### 2. Crear Entorno Virtual

**En Windows (PowerShell):**
```powershell
python -m venv pilapeback
cd pilapeback
Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv pilapeback
cd pilapeback
Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv pilapeback
cd pilapeback
source bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración Flask
FLASK_APP=main_refactorizado.py
FLASK_ENV=development
FLASK_DEBUG=True

# Clave secreta para JWT (cámbiala en producción)
SECRET_KEY=tu-clave-secreta-super-segura-aqui

# Puerto del servidor
PORT=5000

# Base de datos (futuro)
DATABASE_URL=sqlite:///pilapeback.db
```

### 5. Ejecutar la Aplicación

```bash
python main_refactorizado.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

## 🔐 Usuarios de Prueba

La aplicación incluye usuarios de prueba para cada categoría profesional:

| Categoría | Cédula | Ficha | Red |
|-----------|--------|-------|-----|
| Software | 1001 | F001 | Software |
| Salud | 1002 | F002 | Salud |
| Agricultura | 1003 | F003 | Agrícola |
| Construcción | 1004 | F004 | Construcción |
| Mecánica | 1005 | F005 | Mecánica Industrial |
| Electrónica | 1006 | F006 | Electrónica |
| Comercio | 1007 | F007 | Comercio |
| Hotelería | 1008 | F008 | Hotelería |
| Gestión | 1009 | F009 | Gestión |
| Ambiental | 1010 | F010 | Ambiental |
| Artes | 1011 | F011 | Artes |
| Deportes | 1012 | F012 | Deportes |

## 📚 Uso de la API

### 1. Autenticación

**POST** `/login`

```json
{
  "cedula": "1001",
  "ficha": "F001"
}
```

**Respuesta:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "red": "Software",
  "perfil": "Desarrollador especializado en aplicaciones web...",
  "nombre": "Juan Software",
  "msg": "Login exitoso"
}
```

### 2. Obtener Empleos

**GET** `/trabajos`

**Headers:**
```
Authorization: Bearer <tu-token-jwt>
```

**Respuesta:**
```json
{
  "trabajos": [
    {
      "id": 1,
      "titulo": "Desarrollador Frontend",
      "descripcion": "Desarrollo de interfaces web...",
      "perfil_requerido": "Software",
      "salario": "$2,500,000",
      "ubicacion": "Bogotá",
      "score_compatibilidad": 100
    }
  ],
  "total": 15,
  "red": "Software",
  "perfil": "Desarrollador especializado...",
  "algoritmo": "score_por_palabras_clave_mejorado"
}
```

### 3. Endpoints Adicionales

- **GET** `/` - Página de bienvenida
- **GET** `/health` - Estado de la API

## 🧮 Sistema de Scoring

El algoritmo de compatibilidad funciona con un sistema de puntuación:

### Puntuación Máxima (100 puntos)
- **Match exacto**: Red del egresado = Perfil requerido del empleo

### Puntuación Variable (0-99 puntos)
- **Red vs Perfil requerido**: 40 puntos por palabra coincidente
- **Perfil descriptivo vs Perfil requerido**: 30 puntos por palabra
- **Perfil descriptivo vs Título**: 20 puntos por palabra
- **Perfil descriptivo vs Descripción**: 10 puntos por palabra

### Filtrado Inteligente
- ❌ **Excluye**: Conectores, artículos, preposiciones
- ✅ **Prioriza**: Términos técnicos y profesionales específicos

## 🏗️ Arquitectura

### Patrón Factory
```python
# app/__init__.py
def create_app():
    app = Flask(__name__)
    # Configuración
    init_routes(app)
    return app
```

### Estructura de Datos Pila
```python
# Los empleos se organizan usando una estructura Pila (LIFO)
# Se usa reversed() para mantener orden correcto por score
for empleo_dict in reversed(empleos_con_score):
    pila.push(empleo_dict)
```

## 🧪 Testing

Para probar la API puedes usar:

### cURL
```bash
# Login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"cedula":"1001","ficha":"F001"}'

# Obtener trabajos
curl -X GET http://127.0.0.1:5000/trabajos \
  -H "Authorization: Bearer <tu-token>"
```

### Postman
1. Importa el archivo `swagger.yaml` (si disponible)
2. Configura el token en las cabeceras de autorización

## 🚧 Desarrollo

### Agregar Nuevos Empleos
Edita el archivo `app/models.py` en la lista `empleos_data`:

```python
empleos_data.append(Empleo(
    id=nuevo_id,
    titulo="Nuevo Empleo",
    descripcion="Descripción detallada...",
    perfil_requerido="Categoría",
    salario="$X,XXX,XXX",
    ubicacion="Ciudad"
))
```

### Agregar Nuevos Egresados
Edita el archivo `app/models.py` en la lista `egresados_data`:

```python
egresados_data.append(Egresado(
    cedula="nueva_cedula",
    nombre="Nombre Completo",
    ficha="NUEVA_FICHA",
    red="Nueva Red",
    perfil="Descripción del perfil profesional..."
))
```

## 🔄 Estados del Servidor

- ✅ **Healthy**: `GET /health` - API funcionando correctamente
- 🔐 **Protected**: Endpoints requieren autenticación JWT válida
- ⏰ **Token Expiry**: Los tokens expiran en 2 horas

## 📝 Logs y Debugging

Para habilitar logs detallados:

```python
# En development
app.config['DEBUG'] = True
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **NarvaezSKY** - *Desarrollo inicial* - [GitHub](https://github.com/NarvaezSKY)

## 🙏 Agradecimientos

- Inspirado en sistemas de matching de empleos
- Basado en Flask framework
- Implementación de estructuras de datos educativas

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/NarvaezSKY/EgresadosAPE-BackEnd/issues) en GitHub.