# Imagen base de Python 3.11 slim
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para OpenCV y healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto (Coolify usa la variable PORT automáticamente)
EXPOSE 5002

# Usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Healthcheck para monitorear el estado de la aplicación
# Verifica que el endpoint /health responda correctamente cada 30 segundos
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5002}/health || exit 1

# Comando de inicio con gunicorn
# Coolify inyectará la variable PORT automáticamente
# Usando formato JSON array para mejor manejo de señales del sistema
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5002} --workers 2 --threads 2 --timeout 120 --access-logfile - --error-logfile - --log-level info"]
