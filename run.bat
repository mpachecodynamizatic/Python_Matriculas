@echo off
echo ============================================================
echo APLICACION OCR - MATRICULAS Y CUENTAKILOMETROS
echo ============================================================
echo.

REM Verificar si el entorno virtual existe
if not exist ".venv" (
    echo [ERROR] Entorno virtual no encontrado
    echo.
    echo [INFO] Ejecuta primero install.bat para configurar el entorno
    echo.
    pause
    exit /b 1
)

echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo ============================================================
echo INFORMACION: Primera Ejecucion
echo ============================================================
echo.
echo En la primera ejecucion, EasyOCR descargara automaticamente
echo los modelos de reconocimiento (aprox. 100-200MB).
echo.
echo Este proceso solo ocurre una vez.
echo Los modelos se guardan en: ~/.EasyOCR/model/
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
echo.

echo [INFO] Iniciando aplicacion Flask...
echo [INFO] Accede a la aplicacion en: http://localhost:5000
echo.
python app.py

echo.
echo [INFO] Aplicacion finalizada
pause