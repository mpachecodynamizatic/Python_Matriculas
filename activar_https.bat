@echo off
echo ============================================================
echo CONFIGURACION HTTPS PARA ACCESO MOVIL
echo ============================================================
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

echo [INFO] Verificando PyOpenSSL...
pip show pyopenssl >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Instalando PyOpenSSL...
    pip install pyopenssl==24.0.0
) else (
    echo [OK] PyOpenSSL ya instalado
)

echo.
echo [INFO] Generando certificados SSL...
python generar_certificado.py

echo.
echo ============================================================
echo CONFIGURACION COMPLETADA
echo ============================================================
echo.
echo Ahora puedes ejecutar: .\run.bat
echo.
echo La aplicacion se iniciara con HTTPS habilitado.
echo.
echo IMPORTANTE AL ACCEDER DESDE EL MOVIL:
echo.
echo 1. Usa https:// (no http://)
echo    Ejemplo: https://192.168.x.x:5000
echo.
echo 2. Veras una advertencia de seguridad (NORMAL)
echo.
echo 3. Acepta la advertencia:
echo    - Chrome: "Avanzado" - "Continuar al sitio"
echo    - Safari: "Mostrar detalles" - "visitar este sitio"
echo    - Firefox: "Avanzado" - "Aceptar el riesgo"
echo.
echo 4. Permite acceso a la camara cuando se solicite
echo.
echo ============================================================
echo.
pause
