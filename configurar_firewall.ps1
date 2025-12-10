# Script PowerShell para configurar firewall
# Ejecutar como Administrador

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CONFIGURACION DE FIREWALL PARA ACCESO EN RED LOCAL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Este script requiere permisos de Administrador" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor:" -ForegroundColor Yellow
    Write-Host "1. Abre PowerShell como Administrador" -ForegroundColor Yellow
    Write-Host "2. Ejecuta: .\configurar_firewall.ps1" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[INFO] Configurando regla de firewall..." -ForegroundColor Yellow
Write-Host ""

# Eliminar regla existente si existe
try {
    Remove-NetFirewallRule -DisplayName "Flask OCR App" -ErrorAction SilentlyContinue
} catch {
    # Ignorar si no existe
}

# Crear nueva regla
try {
    New-NetFirewallRule `
        -DisplayName "Flask OCR App" `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort 5000 `
        -Action Allow `
        -Profile Private,Domain `
        -Description "Permite acceso a la aplicacion Flask OCR desde la red local" `
        -Enabled True
    
    Write-Host "[OK] Regla de firewall creada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "La aplicacion ahora es accesible desde otros dispositivos" -ForegroundColor Green
    Write-Host "en la red local en el puerto 5000." -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANTE:" -ForegroundColor Yellow
    Write-Host "- Solo funciona en redes Privadas y de Dominio" -ForegroundColor Yellow
    Write-Host "- Las redes Publicas permanecen bloqueadas por seguridad" -ForegroundColor Yellow
    Write-Host ""
    
} catch {
    Write-Host "[ERROR] No se pudo crear la regla de firewall" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Para verificar la regla:" -ForegroundColor Cyan
Write-Host "Get-NetFirewallRule -DisplayName 'Flask OCR App'" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Mostrar información de la IP local
Write-Host "Tu IP local es:" -ForegroundColor Yellow
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"}).IPAddress
if ($localIP) {
    foreach ($ip in $localIP) {
        Write-Host "  → http://$($ip):5000" -ForegroundColor Green
    }
} else {
    Write-Host "  No se pudo detectar la IP local automáticamente" -ForegroundColor Red
    Write-Host "  Ejecuta 'ipconfig' para verla manualmente" -ForegroundColor Yellow
}
Write-Host ""

Read-Host "Presiona Enter para salir"
