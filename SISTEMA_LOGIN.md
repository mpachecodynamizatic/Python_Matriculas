# 🔐 Sistema de Login - Guía de Uso

## Descripción

La aplicación ahora incluye un sistema de autenticación mediante login para proteger el acceso al OCR.

## 🎯 Características

- ✅ Login con usuario y contraseña
- ✅ Sesiones seguras con Flask
- ✅ Protección de todas las rutas
- ✅ Botón de cerrar sesión
- ✅ Interfaz moderna y responsive
- ✅ Credenciales configurables

## 👤 Usuarios Predeterminados

Por defecto, la aplicación viene con dos usuarios de prueba:

| Usuario | Contraseña | Nivel |
|---------|-----------|-------|
| `admin` | `admin123` | Administrador |
| `user` | `user123` | Usuario |

## ⚙️ Configuración de Usuarios

### Método 1: Variables de Entorno (Recomendado)

Edita el archivo `.env` y añade/modifica la línea:

```env
LOGIN_USERS=admin:admin123,user:user123,otro:pass456
```

**Formato**: `usuario1:contraseña1,usuario2:contraseña2,...`

### Método 2: Modificar app.py

Edita `app.py` y modifica el diccionario `USUARIOS`:

```python
USUARIOS = {
    'admin': 'admin123',
    'user': 'user123',
    'nuevo_usuario': 'nueva_contraseña'
}
```

⚠️ **Importante**: Reinicia la aplicación después de cambiar las credenciales.

## 🚀 Flujo de Uso

1. **Acceder a la aplicación**:
   - Abre `https://localhost:5000`
   - Serás redirigido al login automáticamente

2. **Iniciar sesión**:
   - Ingresa usuario y contraseña
   - Presiona "Iniciar Sesión"

3. **Usar la aplicación**:
   - Una vez autenticado, accedes a la interfaz OCR
   - Tu nombre de usuario aparece en el header
   
4. **Cerrar sesión**:
   - Haz clic en "Cerrar Sesión" en el header
   - Serás redirigido al login

## 🔒 Seguridad

### Características de Seguridad Implementadas:

- ✅ **Sesiones seguras**: Flask maneja sesiones cifradas
- ✅ **Secret Key**: Clave aleatoria para firmar cookies
- ✅ **Rutas protegidas**: Decorador `@login_required`
- ✅ **Variables de entorno**: Credenciales fuera del código
- ✅ **.gitignore**: El archivo `.env` no se sube a Git

### Recomendaciones para Producción:

1. **Cambiar contraseñas**:
   ```env
   LOGIN_USERS=admin:ContraseñaSegura123!,user:OtraContraseñaSegura456!
   ```

2. **Usar contraseñas fuertes**:
   - Mínimo 12 caracteres
   - Combinar mayúsculas, minúsculas, números y símbolos
   - Evitar palabras del diccionario

3. **Configurar SECRET_KEY fija**:
   ```env
   SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria_aqui
   ```

4. **Considerar hash de contraseñas**:
   - Para mayor seguridad, usar bcrypt o similar
   - Ejemplo:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

5. **HTTPS obligatorio**:
   - La aplicación ya usa HTTPS por defecto
   - Nunca usar HTTP en producción

6. **Limitar intentos de login**:
   - Implementar bloqueo después de X intentos fallidos
   - Usar captcha si es necesario

## 📱 Interfaz de Login

### Desktop
- Diseño centrado con gradiente
- Formulario elegante con animaciones
- Información de usuarios de prueba visible

### Mobile
- Completamente responsive
- Teclado optimizado
- Touch-friendly

## 🛠️ Personalización

### Cambiar Estilos del Login

Edita `templates/login.html` en la sección `<style>`:

```css
/* Cambiar colores del gradiente */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Cambiar colores de botones */
.btn-login {
    background: linear-gradient(135deg, #tu-color1 0%, #tu-color2 100%);
}
```

### Añadir Más Campos

Puedes extender el formulario para incluir:
- Email
- Nombre completo
- Roles/permisos
- Campos personalizados

## 🔄 Gestión de Sesiones

La sesión se mantiene mientras:
- El navegador permanece abierto
- No se cierra sesión manualmente
- No se reinicia el servidor (en desarrollo)

## ❓ Problemas Comunes

### "Usuario o contraseña incorrectos"
- Verifica que estás usando las credenciales correctas
- Revisa el archivo `.env` o `app.py`
- Las credenciales son case-sensitive

### "Error al iniciar sesión"
- Verifica que Flask esté corriendo
- Revisa la consola del servidor para errores
- Asegúrate de que el archivo `.env` existe

### "Redirección infinita"
- Limpia las cookies del navegador
- Reinicia el servidor Flask
- Verifica la configuración de SECRET_KEY

## 📊 Logs y Auditoría

Para producción, considera añadir:
- Log de intentos de login
- Registro de accesos exitosos
- Alertas de seguridad
- Auditoría de acciones

## 🎨 Capturas

### Pantalla de Login
```
┌─────────────────────────────────┐
│         🔐 OCR Application       │
│   Matrículas y Cuentakilómetros │
├─────────────────────────────────┤
│                                 │
│  👤 Usuario: [____________]     │
│  🔒 Contraseña: [__________]    │
│                                 │
│     [  Iniciar Sesión  ]        │
│                                 │
└─────────────────────────────────┘
```

### Header con Usuario
```
┌─────────────────────────────────────────┐
│ 📷 Reconocimiento OCR     👤 admin      │
│ Captura matrículas...    [Cerrar Sesión]│
└─────────────────────────────────────────┘
```

## 📝 Notas Adicionales

- El sistema usa sesiones del lado del servidor
- Las contraseñas se transmiten por HTTPS
- Compatible con todos los navegadores modernos
- Funciona en desktop, tablet y móvil

## 🔮 Mejoras Futuras Posibles

- [ ] Registro de nuevos usuarios
- [ ] Recuperación de contraseña
- [ ] Autenticación de dos factores (2FA)
- [ ] Login con Google/Microsoft
- [ ] Gestión de roles y permisos
- [ ] Panel de administración
- [ ] Historial de actividad
