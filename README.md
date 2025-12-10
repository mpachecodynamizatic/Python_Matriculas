# Aplicación OCR para Matrículas y Cuenta kilómetros

Aplicación web desarrollada con Flask que permite capturar imágenes desde la cámara del dispositivo y extraer texto mediante **Google Gemini 2.5 Flash**.

## 🚀 Demo en Vivo

**Accede a la aplicación**: [https://python-matriculas-ocr.onrender.com](https://python-matriculas-ocr.onrender.com)

**Credenciales de prueba**:
- Usuario: `admin` / Contraseña: `admin123`
- Usuario: `user` / Contraseña: `user123`

⚠️ **Nota**: La primera carga puede tardar ~30 segundos (el servicio gratuito se duerme después de 15 min sin uso).

## Características

- ✅ **Google Gemini 2.5 Flash**: IA de alta precisión para OCR
- ✅ **Sistema de gestión de vehículos** con tabla y exportación Excel
- ✅ **Autenticación de usuarios** con sistema de login
- ✅ **Captura secuencial** de matrícula y kilometraje
- ✅ **Drag & Drop**: Arrastra imágenes o usa la cámara
- ✅ **Entrada manual** de kilometraje como alternativa
- ✅ **Editar/Eliminar** vehículos registrados
- ✅ Captura de imágenes en tiempo real desde la cámara
- ✅ Reconocimiento de matrículas europeas
- ✅ Lectura de cuentakilómetros digitales
- ✅ **Descarga de datos en Excel** (.xlsx)
- ✅ Interfaz web responsive
- ✅ **Soporte HTTPS para acceso móvil**

## Motor OCR

### 🤖 Google Gemini 2.5 Flash
- **Alta precisión**: 95%+
- **Requiere API Key** (gratuita con límites)
- **Online** - Requiere conexión
- **Velocidad**: Rápido (~1-2s)
- Obtén tu API Key en: https://makersuite.google.com/app/apikey

## Requisitos Previos

### 1. Python
- Python 3.8 o superior

### 2. Motor OCR (Elige uno o varios)

#### Opción A: Tesseract OCR (Recomendado para empezar)
- Descarga e instala desde: https://github.com/UB-Mannheim/tesseract/wiki
- Ver guía completa: [INSTALACION_TESSERACT.md](INSTALACION_TESSERACT.md)
- **100% gratuito y sin límites**

#### Opción B: OCR.space API (Nuevo - Sin instalación)
- **Ya incluido por defecto** con API key gratuita
- **25,000 peticiones/mes gratis**
- Opcional: Obtén tu propia API key en: https://ocr.space/ocrapi
- Configura en `.env`: `OCRSPACE_API_KEY=tu_key` (opcional)

#### Opción C: Google Gemini (Mayor precisión)
- Obtén tu API key en: https://aistudio.google.com/app/apikey
- Configura en `.env`: `GEMINI_API_KEY=tu_key`
- **Cuota gratuita limitada**

## Instalación

### Paso 1: Instalar dependencias

Ejecuta `install.bat`:
```cmd
.\install.bat
```

O manualmente:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 2: Configurar variables de entorno

1. Copia `.env.example` a `.env`:
```bash
copy .env.example .env
```

2. Edita `.env` y configura:
```env
# API Key de Gemini (OPCIONAL - si excedes cuota, usa OCR.space o Tesseract)
GEMINI_API_KEY=tu_api_key_aqui

# API Key de OCR.space (OPCIONAL - ya tiene una por defecto)
# OCRSPACE_API_KEY=tu_api_key_aqui

# Usuarios del sistema (formato: usuario:password,usuario2:password2)
LOGIN_USERS=admin:admin123,user:user123
```

### Paso 3: Activar HTTPS (para móviles)

**Los navegadores móviles requieren HTTPS para acceder a la cámara.**

Ejecuta una sola vez:
```bash
.\activar_https.bat
```

Esto generará certificados SSL auto-firmados (`cert.pem` y `key.pem`).

### Paso 4: Configurar firewall (opcional - para acceso en red local)

Para acceder desde otros dispositivos en la misma WiFi:

```bash
.\configurar_firewall.bat
```

## Uso

### 1. Iniciar la aplicación

```bash
.\run.bat
```

O manualmente:
```bash
.venv\Scripts\activate
python app.py
```

### 2. Acceder a la aplicación

**Desde el mismo PC:**
- HTTPS: `https://localhost:5000`
- HTTP: `http://localhost:5000`

**Desde móvil/tablet (misma WiFi):**
- HTTPS: `https://TU_IP:5000` (ejemplo: `https://192.168.1.100:5000`)

*Nota: El navegador mostrará advertencia de certificado auto-firmado. Es normal, acepta para continuar.*

### 3. Login

Credenciales por defecto (configurable en `.env`):
- **Admin**: `admin` / `admin123`
- **Usuario**: `user` / `user123`

### 4. Seleccionar Motor OCR

En la pantalla de **Gestión de Vehículos**, encontrarás el selector de motor:

**⚙️ Motor de Reconocimiento**
- 🆓 **Tesseract OCR**: Gratuito - Sin límites - Offline (por defecto)
- 🤖 **Google Gemini 2.5**: Mayor precisión - Requiere API Key

Haz clic en la opción deseada. El cambio es inmediato.

> **💡 Tip**: Si alcanzas el límite de Gemini, cambia a Tesseract automáticamente.

### 5. Gestionar vehículos

#### a) Pantalla de Gestión
Tras el login, accederás a la **pantalla de gestión de vehículos** donde verás:
- **Selector de Motor OCR**: Elige entre Tesseract o Gemini
- **Tabla de vehículos**: Matrícula y kilometraje de cada vehículo registrado
- **Botón "Iniciar Captura"**: Abre la cámara para capturar un nuevo vehículo
- **Botón "Descargar Excel"**: Descarga todos los datos en formato `.xlsx`

#### b) Captura de Vehículo (Flujo de 2 pasos)
Al hacer clic en "Iniciar Captura":

**Paso 1: Capturar Matrícula**
1. Enfoca la matrícula del vehículo con la cámara
2. Haz clic en "Capturar Matrícula"
3. Gemini Vision procesa la imagen
4. El texto detectado aparece en pantalla

**Paso 2: Capturar Kilometraje**
1. El botón cambia automáticamente a "Capturar Kilometraje"
2. Enfoca el cuentakilómetros del vehículo
3. Haz clic en "Capturar Kilometraje"
4. Gemini Vision procesa la imagen
5. El vehículo se guarda automáticamente y vuelves a la tabla

#### c) Cerrar sin Guardar
- En cualquier momento durante la captura, haz clic en "✖ Cerrar"
- Regresarás a la pantalla de gestión sin guardar los datos

#### d) Descargar Excel
- Haz clic en "Descargar Excel" en la pantalla de gestión
- Se generará un archivo `.xlsx` con:
  - Matrícula
  - Kilometraje
  - Fecha de registro
- El archivo se descarga automáticamente

## Estructura del Proyecto

```
Python_Matriculas/
├── app.py                          # Aplicación Flask principal
├── ocr_processor.py                # Motor OCR con Gemini Vision
├── .env                            # Configuración (API keys, usuarios)
├── .env.example                    # Plantilla de configuración
├── requirements.txt                # Dependencias Python
├── install.bat                     # Script instalación Windows
├── run.bat                         # Script ejecución Windows
├── activar_https.bat               # Generar certificados SSL
├── configurar_firewall.bat         # Configurar firewall Windows
├── cert.pem / key.pem              # Certificados SSL
├── templates/
│   ├── login.html                  # Página de login
│   ├── vehiculos.html              # Gestión de vehículos
│   └── captura.html                # Captura dual (matrícula + km)
├── static/
│   ├── css/style.css               # Estilos
│   └── js/
│       ├── camera.js               # Lógica de cámara (legacy)
│       └── captura.js              # Captura secuencial
└── DOCUMENTACION/
    ├── GESTION_VEHICULOS.md        # Guía del sistema de gestión
    ├── CONFIGURACION_GEMINI.md     # Guía de Gemini API
    ├── SISTEMA_LOGIN.md            # Documentación login
    ├── SOLUCION_CAMARA_MOVIL.md    # Solución HTTPS móvil
    └── ACCESO_RED_LOCAL.md         # Acceso desde WiFi
```
│   └── js/camera.js                # Lógica de cámara
└── DOCUMENTACION/
    ├── CONFIGURACION_GEMINI.md     # Guía de Gemini API
    ├── SISTEMA_LOGIN.md            # Documentación login
    ├── SOLUCION_CAMARA_MOVIL.md    # Solución HTTPS móvil
    └── ACCESO_RED_LOCAL.md         # Acceso desde WiFi
```

## Tecnologías Utilizadas

- **Backend**: Flask 3.0.0
- **OCR/IA**: Google Gemini 2.5 Flash Vision
- **Procesamiento**: OpenCV, Pillow, NumPy
- **Exportación**: openpyxl 3.1.2 (Excel)
- **Frontend**: HTML5, CSS3, JavaScript (MediaDevices API)
- **Seguridad**: Flask Sessions, HTTPS, python-dotenv
- **Servidor Producción**: Gunicorn 21.2.0

## 🌐 Despliegue en Render (Producción)

### Opción 1: Deploy Automático (Recomendado)

1. **Fork/Clone el repositorio** en tu cuenta de GitHub
2. Ve a [render.com](https://render.com) y crea una cuenta gratuita
3. Click en "New +" → "Web Service"
4. Conecta tu repositorio de GitHub
5. Render detectará automáticamente `render.yaml` y configurará todo
6. Click en "Apply" y luego "Create Web Service"
7. Espera 5-10 minutos mientras se despliega
8. ¡Listo! Tu app estará en: `https://tu-app.onrender.com`

### Opción 2: Configuración Manual

1. En Render, selecciona "New Web Service"
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name**: `python-matriculas-ocr` (o tu nombre preferido)
   - **Environment**: `Python 3`
   - **Region**: `Frankfurt` (más cercano a Europa)
   - **Branch**: `master`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

4. Añade **Variables de Entorno**:
   ```
   GEMINI_API_KEY=tu_api_key_aqui (REQUERIDO)
   LOGIN_USERS=admin:admin123,user:user123
   SECRET_KEY=(déjalo vacío, Render lo generará)
   PYTHON_VERSION=3.11.0
   ```

5. Click en "Create Web Service"
6. Espera el despliegue (5-10 minutos)

### ⚠️ Limitaciones del Plan Gratuito de Render

- ⏰ El servicio se "duerme" después de 15 minutos sin actividad
- 🐌 Primera carga después de dormir: ~30 segundos
- 💾 750 horas/mes de tiempo activo
- 🔑 Requiere API Key de Gemini configurada

### 📝 Archivos de Configuración para Render

El proyecto ya incluye:
- ✅ `Procfile`: Define el comando de inicio con Gunicorn
- ✅ `render.yaml`: Configuración automática de Render
- ✅ `requirements.txt`: Dependencias con Gunicorn incluido
- ✅ `.gitignore`: Excluye archivos sensibles

## Documentación Adicional

- 📖 **[INSTALACION_TESSERACT.md](INSTALACION_TESSERACT.md)**: Instalar Tesseract OCR en Windows
- 📖 **[GESTION_VEHICULOS.md](GESTION_VEHICULOS.md)**: Sistema de gestión y exportación Excel
- 📖 **[CONFIGURACION_GEMINI.md](CONFIGURACION_GEMINI.md)**: Configurar API de Gemini
- 📖 **[SISTEMA_LOGIN.md](SISTEMA_LOGIN.md)**: Sistema de autenticación
- 📖 **[SOLUCION_CAMARA_MOVIL.md](SOLUCION_CAMARA_MOVIL.md)**: Configurar HTTPS para móviles
- 📖 **[ACCESO_RED_LOCAL.md](ACCESO_RED_LOCAL.md)**: Acceder desde red WiFi
- 📖 **[GUIA_RAPIDA_HTTPS.md](GUIA_RAPIDA_HTTPS.md)**: Guía rápida HTTPS

## Solución de Problemas

### Error: "No se encontró GEMINI_API_KEY"
- Verifica que `.env` existe y contiene `GEMINI_API_KEY=tu_key`
- Reinicia la aplicación después de crear `.env`

### La cámara no funciona en móvil
- Asegúrate de usar **HTTPS** (no HTTP)
- Ejecuta `activar_https.bat` para generar certificados
- Acepta la advertencia de certificado en el navegador

### "No hay vehículos para descargar"
- Debes capturar al menos un vehículo antes de poder descargar el Excel
- Los datos se guardan en la sesión y se pierden al cerrar sesión

### No puedo acceder desde otro dispositivo
- Verifica que ambos dispositivos están en la misma WiFi
- Ejecuta `configurar_firewall.bat` para abrir puerto 5000
- Usa la IP correcta (ejecuta `ipconfig` para verla)

### Error de login
- Verifica que `.env` contiene `LOGIN_USERS`
- Formato: `usuario:password,usuario2:password2`
- Reinicia la aplicación después de cambiar usuarios

## Rendimiento

- **Procesamiento**: ~1-2 segundos por imagen
- **Precisión**: 95%+ con buena iluminación
- **Modelos**: Gemini 2.5 Flash (cloud-based, sin descarga local)
- **Consumo**: Bajo (procesamiento en la nube)

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Desarrollado con ❤️ usando Flask y Google Gemini Vision AI
