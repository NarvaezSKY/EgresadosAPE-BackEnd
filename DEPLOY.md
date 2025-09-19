# Despliegue en Vercel 🚀

Esta guía te ayudará a desplegar la API PilAPE en Vercel.

## 📋 Requisitos Previos

- Cuenta en [Vercel](https://vercel.com/)
- Repositorio en GitHub
- CLI de Vercel (opcional)

## 🚀 Opción 1: Despliegue desde Dashboard de Vercel

### 1. Conectar Repositorio
1. Ve a [vercel.com](https://vercel.com/) e inicia sesión
2. Haz clic en "Import Project"
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `EgresadosAPE-BackEnd`

### 2. Configurar Variables de Entorno
En el dashboard de Vercel, ve a Settings → Environment Variables y añade:

```
SECRET_KEY=tu-clave-secreta-super-segura-para-produccion
FLASK_ENV=production
DEBUG=False
JWT_EXPIRATION_HOURS=2
```

### 3. Desplegar
- Haz clic en "Deploy"
- Vercel detectará automáticamente el `vercel.json` y `requirements.txt`

## 🚀 Opción 2: Despliegue con CLI de Vercel

### 1. Instalar CLI
```bash
npm i -g vercel
```

### 2. Login y Deploy
```bash
# En el directorio raíz del proyecto
vercel login
vercel --prod
```

### 3. Configurar Variables de Entorno
```bash
vercel env add SECRET_KEY
vercel env add FLASK_ENV
vercel env add DEBUG
```

## 🔧 Configuración Automática

El proyecto incluye:

- ✅ **vercel.json** - Configuración de despliegue
- ✅ **requirements.txt** - Dependencias de Python
- ✅ **.vercelignore** - Archivos a excluir
- ✅ **Configuración de entornos** - Development/Production

## 📍 URLs de la API

Después del despliegue, tu API estará disponible en:

```
https://tu-proyecto.vercel.app/
```

### Endpoints:
- `POST /login` - Autenticación
- `GET /trabajos` - Empleos (requiere token)
- `GET /health` - Estado de la API

## 🧪 Testing en Producción

### 1. Health Check
```bash
curl https://tu-proyecto.vercel.app/health
```

### 2. Login de Prueba
```bash
curl -X POST https://tu-proyecto.vercel.app/login \
  -H "Content-Type: application/json" \
  -d '{"cedula":"1001","ficha":"F001"}'
```

### 3. Obtener Empleos
```bash
curl -X GET https://tu-proyecto.vercel.app/trabajos \
  -H "Authorization: Bearer <token-obtenido>"
```

## ⚠️ Consideraciones Importantes

### Limitaciones de Vercel
- **Tiempo de ejecución**: Máximo 10 segundos por request
- **Memoria**: 1024MB máximo
- **Tamaño**: 50MB después de la compilación

### Variables de Entorno
- Nunca commits el archivo `.env` 
- Configura `SECRET_KEY` diferente para producción
- Usa variables de entorno seguras en Vercel

### Monitoreo
- Vercel proporciona logs automáticos
- Ve a Functions → View Function Logs
- Monitorea performance en Analytics

## 🔍 Troubleshooting

### Error: "Module not found"
```bash
# Verificar requirements.txt
cat requirements.txt
```

### Error: "Application failed to start"
```bash
# Verificar logs en Vercel Dashboard
# Functions → View Function Logs
```

### Error: "Environment variables"
```bash
# Verificar variables en Vercel
# Settings → Environment Variables
```

## 🔄 Actualizaciones

Cada push a la rama `main` desplegará automáticamente:

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
# ↑ Esto triggerea el despliegue automático
```

## 📊 Monitoreo

Vercel proporciona:
- 📈 **Analytics** - Uso y performance
- 📋 **Logs** - Errores y debugging  
- 🔍 **Functions** - Estado de las funciones serverless
- 🌐 **Domains** - Gestión de dominios personalizados

---

**¿Problemas?** Revisa los [logs de Vercel](https://vercel.com/docs/concepts/functions/serverless-functions#logs) o abre un issue en GitHub.