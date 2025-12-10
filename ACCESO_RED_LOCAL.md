# Configuración de Acceso desde Red Local

## 🌐 Acceso Remoto a la Aplicación

La aplicación está configurada para ser accesible desde cualquier dispositivo en tu red local.

## 📋 Requisitos Previos

1. **Misma red WiFi/LAN**: Todos los dispositivos deben estar conectados a la misma red
2. **Firewall configurado**: Permitir conexiones en el puerto 5000

---

## 🔧 Configuración del Firewall (Windows)

### Opción 1: Configuración Automática (Recomendado)

Ejecuta este comando en PowerShell como **Administrador**:

```powershell
New-NetFirewallRule -DisplayName "Flask OCR App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow -Profile Private,Domain
```

### Opción 2: Configuración Manual

1. Abre **Windows Defender Firewall** → "Configuración avanzada"
2. Click en **Reglas de entrada** → **Nueva regla...**
3. Selecciona **Puerto** → Siguiente
4. **TCP** → Puerto local específico: **5000** → Siguiente
5. **Permitir la conexión** → Siguiente
6. Marca: **Privado** y **Dominio** → Siguiente
7. Nombre: `Flask OCR App` → Finalizar

### Opción 3: Script Automático

Usa el archivo `configurar_firewall.bat` (ejecutar como Administrador)

---

## 📱 Cómo Acceder desde Otros Dispositivos

### Paso 1: Obtener tu IP Local

Cuando ejecutes `.\run.bat`, verás:

```
📱 Accede desde otros dispositivos en la red local:
   → http://192.168.1.XXX:5000
```

### Paso 2: Acceder desde Móvil/Tablet/PC

1. Abre el navegador en el dispositivo móvil
2. Escribe la URL: `http://192.168.1.XXX:5000`
3. Permite el acceso a la cámara cuando se solicite

---

## 🔍 Verificar tu IP Local

### Windows (CMD/PowerShell):
```bash
ipconfig
```
Busca: **Dirección IPv4** en la sección de tu adaptador de red WiFi/Ethernet

### Ejemplo de salida:
```
Adaptador de LAN inalámbrica Wi-Fi:
   Dirección IPv4. . . . . . . . . : 192.168.1.105  ← Esta es tu IP
```

---

## 🛡️ Seguridad

### Recomendaciones:

✅ **Solo red privada**: Usa esta configuración solo en redes de confianza (hogar/oficina)  
✅ **Firewall activo**: Mantén el perfil "Público" bloqueado en el firewall  
✅ **No exponer a Internet**: No abras el puerto 5000 en tu router  
❌ **Evita redes públicas**: No uses en cafeterías, aeropuertos, etc.

### Niveles de Seguridad:

| Red | Seguridad | Recomendación |
|-----|-----------|---------------|
| Red doméstica | ✅ Alta | Seguro |
| Red de oficina | ⚠️ Media | Verificar políticas |
| Red pública | ❌ Baja | No usar |

---

## 🔒 Restricciones Adicionales (Opcional)

### Limitar acceso a IPs específicas

Edita `app.py` y añade antes de `app.run()`:

```python
from flask import request, abort

@app.before_request
def limit_remote_addr():
    # Solo permitir estas IPs
    allowed_ips = ['192.168.1.100', '192.168.1.101', '127.0.0.1']
    if request.remote_addr not in allowed_ips:
        abort(403)  # Acceso denegado
```

### Requerir contraseña

Instala Flask-HTTPAuth:
```bash
pip install Flask-HTTPAuth
```

Añade autenticación en `app.py`:
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "tu_contraseña_segura"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Protege las rutas
@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

---

## 🚨 Solución de Problemas

### Problema: "No se puede acceder desde el móvil"

**Soluciones**:

1. **Verifica la IP**: 
   - Ejecuta `ipconfig` y confirma la IP
   - Usa la IP que empieza con `192.168.x.x` o `10.x.x.x`

2. **Verifica el firewall**:
   ```powershell
   Get-NetFirewallRule -DisplayName "Flask OCR App"
   ```

3. **Verifica que el servidor esté escuchando**:
   ```powershell
   netstat -an | findstr ":5000"
   ```
   Debe mostrar: `0.0.0.0:5000` o `[::]:5000`

4. **Ping desde el móvil**:
   - Instala una app de "Network Tools" o "Ping"
   - Haz ping a la IP de tu PC
   - Si no responde, hay problema de red

---

### Problema: "Firewall bloquea la conexión"

**Solución temporal** (no recomendado para producción):
```powershell
# Deshabilitar firewall temporalmente (solo para probar)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Volver a habilitar después
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**Solución permanente**: Configura la regla del firewall correctamente

---

### Problema: "ERR_CONNECTION_REFUSED"

**Causas comunes**:
- Servidor Flask no está ejecutándose
- Puerto incorrecto (debe ser 5000)
- IP incorrecta
- Dispositivos en redes diferentes

**Verificación**:
```powershell
# Ver si Flask está escuchando
netstat -ano | findstr ":5000"
```

---

## 📊 Puertos Alternativos

Si el puerto 5000 está en uso, cambia en `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Cambia a 8080 u otro
```

**No olvides**:
- Actualizar la regla del firewall con el nuevo puerto
- Usar la nueva URL: `http://IP:8080`

---

## 🌐 Acceso desde Navegadores Móviles

### Requisitos de Cámara:

Los navegadores modernos requieren:
- ✅ **HTTPS** o **localhost** para acceso a cámara
- ⚠️ Con **HTTP + IP local** algunos navegadores pueden bloquear la cámara

### Soluciones:

1. **Chrome/Edge Android**: Suele funcionar con `http://IP:5000`
2. **Safari iOS**: Puede requerir HTTPS
3. **Firefox Mobile**: Funciona con HTTP local

### Para usar HTTPS (avanzado):

```python
# Genera certificado autofirmado
app.run(
    debug=True, 
    host='0.0.0.0', 
    port=5000,
    ssl_context='adhoc'  # Requiere: pip install pyopenssl
)
```

**Nota**: Los certificados autofirmados mostrarán advertencia de seguridad.

---

## ✅ Verificación Final

Lista de comprobación:

- [ ] Firewall configurado (puerto 5000 abierto)
- [ ] Servidor Flask ejecutándose
- [ ] IP local identificada
- [ ] Dispositivos en la misma red WiFi
- [ ] Navegador moderno en el dispositivo móvil

---

## 🎯 Ejemplo de Uso

**Escenario**: Acceder desde un móvil

1. PC con IP: `192.168.1.105`
2. Ejecutar: `.\run.bat` en el PC
3. En el móvil, abrir navegador
4. Ir a: `http://192.168.1.105:5000`
5. Permitir acceso a cámara
6. ¡Listo para usar!

---

## 📞 Comandos Útiles

```powershell
# Ver IP local
ipconfig

# Ver reglas de firewall
Get-NetFirewallRule -DisplayName "*Flask*"

# Ver conexiones activas
netstat -ano | findstr ":5000"

# Ping desde otro dispositivo
ping 192.168.1.105

# Ver procesos escuchando en puerto 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess
```

---

¡Disfruta del acceso remoto a tu aplicación OCR! 📱✨
