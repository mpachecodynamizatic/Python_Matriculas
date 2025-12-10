## Instrucciones para Configurar en Render

### Variables de Entorno REQUERIDAS:

1. Ve a tu servicio en Render Dashboard
2. Click en "Environment" en el menú lateral
3. Añade las siguientes variables:

```
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
LOGIN_USERS=admin:admin123,user:user123
PYTHON_VERSION=3.11.0
```

### Cómo obtener GEMINI_API_KEY:

1. Ve a: https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la API Key generada
5. Pégala en Render como valor de GEMINI_API_KEY

### Verificar configuración:

1. Después de añadir las variables, Render redesplegará automáticamente
2. Revisa los logs en "Logs" para ver si hay errores
3. Busca líneas como:
   - "INFO: Configurando Gemini con API Key..."
   - "INFO: Modelo Gemini configurado correctamente"

### Solución de problemas:

Si ves error "No se encontró GEMINI_API_KEY":
- Verifica que la variable esté escrita exactamente: GEMINI_API_KEY
- Asegúrate de que guardaste los cambios en Render
- Espera a que el redespliegue termine

Si ves error de API de Gemini:
- Verifica que la API Key sea válida
- Comprueba que no haya espacios antes/después de la key
- Verifica tu cuota en Google AI Studio
