@echo off
echo ============================================================
echo CONFIGURACION DE FIREWALL PARA ACCESO EN RED LOCAL
echo ============================================================
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Este script requiere permisos de Administrador
    echo.
    echo Por favor:
    echo 1. Click derecho en este archivo
    echo 2. Selecciona "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo [INFO] Configurando regla de firewall...
echo.

REM Eliminar regla existente si existe
netsh advfirewall firewall delete rule name="Flask OCR App" >nul 2>&1

REM Crear nueva regla para permitir conexiones entrantes en puerto 5000
netsh advfirewall firewall add rule ^
    name="Flask OCR App" ^
    dir=in ^
    action=allow ^
    protocol=TCP ^
    localport=5000 ^
    profile=private,domain ^
    description="Permite acceso a la aplicacion Flask OCR desde la red local"

if %errorLevel% equ 0 (
    echo [OK] Regla de firewall creada exitosamente!
    echo.
    echo La aplicacion ahora es accesible desde otros dispositivos
    echo en la red local en el puerto 5000.
    echo.
    echo IMPORTANTE:
    echo - Solo funciona en redes Privadas y de Dominio
    echo - Las redes Publicas permanecen bloqueadas por seguridad
    echo.
) else (
    echo [ERROR] No se pudo crear la regla de firewall
    echo.
    echo Intenta configurarla manualmente:
    echo 1. Abre "Windows Defender Firewall"
    echo 2. Click en "Configuracion avanzada"
    echo 3. "Reglas de entrada" - "Nueva regla"
    echo 4. Puerto TCP 5000
    echo 5. Permitir la conexion
    echo.
)

echo.
echo ============================================================
echo Para verificar la regla:
echo netsh advfirewall firewall show rule name="Flask OCR App"
echo ============================================================
echo.

pause
