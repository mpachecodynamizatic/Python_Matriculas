# 🚀 Guía de Configuración - Google Gemini Vision

## ¿Qué cambió?

La aplicación ahora usa **Google Gemini Vision** en lugar de EasyOCR para el reconocimiento de texto con IA.

### Ventajas de Gemini:
- ✅ **Más rápido**: Procesamiento en la nube de Google
- ✅ **Más preciso**: Modelo de última generación
- ✅ **Más ligero**: No requiere descargar modelos pesados (200MB)
- ✅ **Menor consumo**: No usa CPU/RAM localmente
- ⚠️ **Requiere**: API key gratuita y conexión a internet

## 📋 Pasos de Configuración

### 1. Obtener API Key de Gemini

1. Ve a: https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la clave generada

### 2. Configurar la aplicación

1. Copia el archivo de ejemplo:
   ```bash
   copy .env.example .env
   ```

2. Edita el archivo `.env` con un editor de texto:
   ```
   GEMINI_API_KEY=AIzaSy...tu_clave_aqui
   ```

3. Guarda el archivo

### 3. Instalar dependencias

```bash
.\install.bat
```

Esto instalará:
- `google-generativeai` - SDK de Gemini
- `python-dotenv` - Para leer variables de entorno
- `Flask`, `opencv-python-headless`, `Pillow`, etc.

### 4. Ejecutar la aplicación

```bash
.\run.bat
```

## 🔄 Cambiar entre modos

Puedes alternar entre **Gemini (IA)** y **Tradicional (sin IA)**:

```bash
.\cambiar_modo.bat
```

O manualmente edita `config.json`:
```json
{
    "ocr": {
        "motor": "gemini"  // o "tradicional"
    }
}
```

## 💰 Límites y Costos

Gemini API tiene un **nivel gratuito generoso**:

- ✅ 60 solicitudes por minuto
- ✅ 1500 solicitudes por día
- ✅ Gratis para uso personal

Suficiente para procesar cientos de imágenes al día.

## ❓ Solución de Problemas

### Error: "GEMINI_API_KEY no encontrada"

1. Verifica que el archivo `.env` existe en la carpeta del proyecto
2. Verifica que contiene: `GEMINI_API_KEY=tu_clave`
3. No uses comillas alrededor de la clave
4. Reinicia la aplicación

### Error: "google-generativeai no instalado"

```bash
.\.venv\Scripts\activate
pip install google-generativeai python-dotenv
```

### Error: "Invalid API key"

1. Verifica que copiaste la clave completa
2. La clave debe empezar con `AIzaSy`
3. Genera una nueva clave si es necesario

### Sin conexión a internet

Usa el modo tradicional:
```bash
.\cambiar_modo.bat
# Selecciona opción 2: Tradicional
```

## 📊 Comparación de Modos

| Característica | Gemini (IA) | Tradicional |
|---|---|---|
| Precisión | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Velocidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Requiere internet | ✅ Sí | ❌ No |
| Instalación | Ligera | Muy ligera |
| Costo | Gratuito* | Gratuito |
| Uso de CPU/RAM | Mínimo | Bajo |

*Dentro de los límites gratuitos

## 🔐 Seguridad

- ✅ El archivo `.env` está en `.gitignore` (no se sube a Git)
- ✅ La API key solo se usa localmente
- ✅ Las imágenes se envían a Google Cloud de forma segura (HTTPS)
- ⚠️ No compartas tu API key públicamente

## 📚 Más Información

- **Documentación Gemini**: https://ai.google.dev/docs
- **Precios**: https://ai.google.dev/pricing
- **Límites**: https://ai.google.dev/gemini-api/docs/quota
