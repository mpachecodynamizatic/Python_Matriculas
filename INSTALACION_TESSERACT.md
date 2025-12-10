# Instalación de Tesseract OCR en Windows

## ⚠️ Importante
Para usar el motor **Tesseract OCR**, necesitas instalar Tesseract en tu sistema Windows.

## 📥 Descarga e Instalación

### Opción 1: Instalador Oficial (Recomendado)

1. **Descargar Tesseract**
   - Ve a: https://github.com/UB-Mannheim/tesseract/wiki
   - Descarga: `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (64-bit)
   - O la versión más reciente disponible

2. **Ejecutar el instalador**
   - Haz doble clic en el archivo descargado
   - Acepta los términos de licencia
   - **IMPORTANTE**: Durante la instalación, anota la ruta de instalación
   - Por defecto: `C:\Program Files\Tesseract-OCR`
   - Marca la opción "Additional language data" si quieres otros idiomas

3. **Completar instalación**
   - Click en "Install"
   - Espera a que termine
   - Click en "Finish"

### Opción 2: Con Chocolatey

Si tienes Chocolatey instalado:

```powershell
choco install tesseract
```

## ⚙️ Configuración en la Aplicación

### Si Tesseract NO está en el PATH

1. Abre `ocr_processor.py`
2. Busca las líneas comentadas al inicio:
```python
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

3. Descomenta y ajusta la ruta según tu instalación:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Si Tesseract SÍ está en el PATH

No necesitas hacer nada, la aplicación lo detectará automáticamente.

## ✅ Verificar Instalación

Abre PowerShell y ejecuta:

```powershell
tesseract --version
```

Deberías ver algo como:
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.43 : libtiff 4.6.0 : zlib 1.3 : libwebp 1.3.2
```

## 🔧 Solución de Problemas

### Error: "tesseract is not installed or it's not in your PATH"

**Solución:**
1. Verifica que Tesseract esté instalado en `C:\Program Files\Tesseract-OCR`
2. Abre `ocr_processor.py`
3. Descomenta y configura la ruta:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Error: "FileNotFoundError: [WinError 2]"

**Solución:**
- La ruta configurada es incorrecta
- Verifica la ubicación real de `tesseract.exe`
- Ajusta la ruta en `ocr_processor.py`

### Tesseract no reconoce texto correctamente

**Soluciones:**
- Asegúrate de tener buena iluminación al capturar
- La imagen debe estar enfocada
- Tesseract funciona mejor con texto horizontal
- Prueba con el motor Gemini para mayor precisión

## 📊 Comparación de Motores

| Característica | Tesseract OCR | Google Gemini 2.5 |
|----------------|---------------|-------------------|
| **Costo** | ✅ Gratuito | ⚠️ Cuota limitada |
| **Instalación** | Requiere software | Solo API Key |
| **Precisión Matrículas** | 70-80% | 95%+ |
| **Precisión Kilometraje** | 65-75% | 95%+ |
| **Velocidad** | Rápido (~0.5s) | Medio (~1-2s) |
| **Internet** | ❌ No requiere | ✅ Requiere |
| **Límites** | ∞ Sin límites | Cuota diaria |

## 🎯 Recomendaciones

### Usa Tesseract cuando:
- ✅ Has alcanzado el límite de Gemini
- ✅ No tienes conexión a internet
- ✅ Necesitas procesar muchas imágenes
- ✅ Quieres evitar costos de API

### Usa Gemini cuando:
- ✅ Necesitas máxima precisión
- ✅ Condiciones de iluminación variables
- ✅ Matrículas con formatos complejos
- ✅ Odómetros digitales difíciles

## 🔄 Cambio de Motor

Una vez instalado Tesseract:

1. Inicia la aplicación
2. Ve a la pantalla de "Gestión de Vehículos"
3. En la sección "⚙️ Motor de Reconocimiento"
4. Selecciona "🆓 Tesseract OCR"
5. ¡Listo! Todas las capturas usarán Tesseract

El cambio es instantáneo y se mantiene durante tu sesión.

## 📖 Recursos Adicionales

- **Documentación Tesseract**: https://tesseract-ocr.github.io/
- **GitHub Tesseract**: https://github.com/tesseract-ocr/tesseract
- **Instaladores Windows**: https://github.com/UB-Mannheim/tesseract/wiki

## 💡 Notas

- Tesseract funciona mejor con imágenes en blanco y negro de alto contraste
- La aplicación aplica preprocesamiento automático para mejorar resultados
- Puedes cambiar entre motores en cualquier momento sin reiniciar
- Los datos capturados con cada motor se guardan en la misma tabla
