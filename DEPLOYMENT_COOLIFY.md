# Deployment en Coolify

## Archivos creados

- **Dockerfile** - Containeriza la aplicación Flask con Python 3.11
- **.dockerignore** - Excluye archivos innecesarios del build
- **docker-compose.yml** - Para testing local (opcional)

## Pasos para desplegar en Coolify

### 1. Preparar el repositorio Git

Asegúrate de que los nuevos archivos estén en tu repositorio:

```bash
git add Dockerfile .dockerignore docker-compose.yml DEPLOYMENT_COOLIFY.md
git commit -m "Agregar configuración Docker para Coolify"
git push origin master
```

### 2. Crear proyecto en Coolify

1. Accede a tu panel de Coolify
2. Click en **+ New Resource**
3. Selecciona **Deploy a new resource**
4. Elige **Public Repository** o **Private Repository** (GitHub)
5. Pega la URL de tu repositorio: `https://github.com/tu-usuario/Python_Matriculas`
6. Selecciona la rama: `master`

### 3. Configurar Variables de Entorno

En Coolify, ve a la sección de **Environment Variables** y agrega:

```
GEMINI_API_KEY=tu_api_key_aqui
LOGIN_USERS=admin:admin123,user:user123
SECRET_KEY=tu_secret_key_segura_aqui
PORT=8000
```

**Importante:**
- Cambia `GEMINI_API_KEY` con tu key real de Google Gemini
- Cambia `LOGIN_USERS` con credenciales seguras
- Genera un `SECRET_KEY` seguro (mínimo 32 caracteres aleatorios)

### 4. Configuración de la aplicación

Coolify detectará automáticamente el Dockerfile. Ajustes recomendados:

- **Build Pack:** Dockerfile (detectado automáticamente)
- **Port:** 8000 (ya configurado en el Dockerfile)
- **Health Check Path:** `/` (opcional)
- **Auto Deploy:** Activar para deploy automático en cada push

### 5. Deploy

Click en **Deploy** y espera a que se construya la imagen y se inicie el contenedor.

## Testing Local con Docker

Para probar localmente antes de desplegar:

```bash
# Construir la imagen
docker build -t python-matriculas .

# Correr el contenedor
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=tu_api_key \
  -e LOGIN_USERS=admin:admin123 \
  -e SECRET_KEY=test_secret \
  python-matriculas
```

O usa docker-compose:

```bash
# Crear .env con tus variables
cp .env.example .env
# Editar .env con tus valores

# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## Acceso a la aplicación

Una vez desplegado, Coolify te proporcionará una URL pública (o puedes configurar un dominio custom):

```
https://python-matriculas.tu-coolify.app
```

## Troubleshooting

### El contenedor no inicia
- Verifica los logs en Coolify
- Asegúrate de que `GEMINI_API_KEY` esté configurada correctamente

### Error 502 Bad Gateway
- El contenedor puede estar iniciando (espera 30-60 segundos)
- Verifica que el puerto 8000 esté expuesto correctamente

### Problemas con OpenCV
- El Dockerfile incluye todas las dependencias necesarias
- Si hay errores, verifica los logs del build

### Variables de entorno no se cargan
- En Coolify, verifica que las variables estén en la sección correcta
- No uses comillas en los valores de las variables

## Ventajas de Coolify vs Render

✅ **Coolify:**
- Control total sobre el servidor
- No hibernación automática
- Sin límites de tiempo de ejecución
- Más económico a largo plazo
- Puedes usar tu propia infraestructura

❌ **Render (free tier):**
- Hibernación después de 15 min
- Cold starts lentos
- Límites de recursos más estrictos

## Mantenimiento

### Actualizar la aplicación
Si tienes auto-deploy activado, simplemente:
```bash
git push origin master
```

Si no, ve a Coolify y click en **Redeploy**.

### Ver logs en tiempo real
En Coolify, ve a tu aplicación → **Logs** → **Follow**

### Escalar recursos
En Coolify, puedes ajustar CPU/RAM en la configuración del contenedor.

## Contacto

Para problemas con el deployment, revisa:
- Logs de Coolify
- Documentación oficial: https://coolify.io/docs
