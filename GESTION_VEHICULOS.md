# Sistema de Gestión de Vehículos

## 📋 Descripción General

La aplicación ahora incluye un sistema completo de gestión de vehículos que permite:
1. **Capturar** matrículas y kilometrajes de vehículos
2. **Almacenar** los datos en una tabla
3. **Descargar** los datos en formato Excel

## 🔄 Flujo de Trabajo

### 1. Login
- Usuario ingresa con sus credenciales
- Redirección automática a la pantalla de gestión

### 2. Pantalla de Gestión (`/vehiculos`)
- **Tabla de vehículos**: Muestra todos los vehículos registrados
  - Columna 1: Matrícula
  - Columna 2: Kilometraje
- **Botón "Iniciar Captura"**: Abre la pantalla de captura
- **Botón "Descargar Excel"**: Genera archivo Excel con los datos
  - Solo habilitado si hay vehículos registrados

### 3. Pantalla de Captura (`/captura`)
- **Paso 1: Capturar Matrícula**
  - Usuario enfoca la matrícula con la cámara
  - Click en "Capturar Matrícula"
  - Gemini Vision procesa la imagen
  - Resultado se muestra en "Matrícula detectada"
  
- **Paso 2: Capturar Kilometraje**
  - Botón cambia a "Capturar Kilometraje"
  - Usuario enfoca el cuentakilómetros
  - Click en "Capturar Kilometraje"
  - Gemini Vision procesa la imagen
  - Resultado se muestra en "Kilometraje detectado"

- **Guardado automático**
  - Tras capturar ambos datos, se guarda automáticamente
  - Redirección a `/vehiculos` con el nuevo vehículo añadido

### 4. Botón Cerrar
- En cualquier momento durante la captura
- Click en "✖ Cerrar" en el header
- Regresa a `/vehiculos` sin guardar

## 🗄️ Almacenamiento de Datos

### Almacenamiento en Sesión
Los vehículos se almacenan en la sesión de Flask:

```python
session['vehiculos'] = [
    {
        'matricula': '1234ABC',
        'kilometros': '150000',
        'fecha': '2025-12-10 14:30:45'
    },
    # ... más vehículos
]
```

**Características:**
- ✅ Datos por usuario (sesión individual)
- ✅ Persistencia durante la sesión
- ⚠️ Se pierden al cerrar sesión o reiniciar servidor
- ⚠️ No hay persistencia en base de datos (por diseño)

## 📥 Descarga de Excel

### Formato del Archivo

El archivo Excel generado contiene:

| Matrícula | Kilometraje | Fecha de Registro |
|-----------|-------------|-------------------|
| 1234ABC   | 150000      | 2025-12-10 14:30:45 |
| 5678DEF   | 205343      | 2025-12-10 14:35:12 |

### Características del Excel
- **Formato**: `.xlsx` (OpenXML)
- **Nombre**: `vehiculos_YYYYMMDD_HHMMSS.xlsx`
- **Encabezados**: Negrita
- **Columnas ajustadas**: Ancho automático
- **Descarga inmediata**: El navegador descarga automáticamente

## 🎨 Interfaz de Usuario

### Pantalla de Gestión
```
┌─────────────────────────────────────────┐
│  📋 Gestión de Vehículos      👤 admin  │
│                              [Cerrar]    │
├─────────────────────────────────────────┤
│                                          │
│  Vehículos Registrados                  │
│  ┌──────────────────────────────────┐  │
│  │ Matrícula  │ Kilometraje         │  │
│  ├──────────────────────────────────┤  │
│  │ 1234ABC    │ 150000              │  │
│  │ 5678DEF    │ 205343              │  │
│  └──────────────────────────────────┘  │
│  Total: 2 vehículo(s)                   │
│                                          │
│  [📸 Iniciar Captura]  [📥 Descargar]  │
│                                          │
└─────────────────────────────────────────┘
```

### Pantalla de Captura
```
┌─────────────────────────────────────────┐
│  📷 Captura de Vehículo   👤 admin      │
│  Paso 1 de 2: Matrícula      [✖ Cerrar]│
├─────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────┐    │
│  │                                 │    │
│  │       [VIDEO CÁMARA]            │    │
│  │                                 │    │
│  └────────────────────────────────┘    │
│  ⚫ Cámara lista - Captura la matrícula │
│                                          │
│      [📸 Capturar Matrícula]            │
│                                          │
│  Matrícula: -                           │
│  Kilometraje: -                         │
│                                          │
└─────────────────────────────────────────┘
```

## 🔌 API Endpoints

### GET `/vehiculos`
Muestra la pantalla de gestión con la tabla de vehículos.

**Respuesta**: HTML template

### GET `/captura`
Muestra la pantalla de captura de fotos.

**Respuesta**: HTML template

### POST `/agregar_vehiculo`
Agrega un vehículo a la lista en sesión.

**Request Body:**
```json
{
    "matricula": "1234ABC",
    "kilometros": "150000"
}
```

**Response Success:**
```json
{
    "success": true,
    "vehiculo": {
        "matricula": "1234ABC",
        "kilometros": "150000",
        "fecha": "2025-12-10 14:30:45"
    }
}
```

**Response Error:**
```json
{
    "success": false,
    "error": "Se requieren matrícula y kilómetros"
}
```

### GET `/descargar_excel`
Genera y descarga un archivo Excel con los vehículos.

**Respuesta**: Archivo `.xlsx` (descarga directa)

**Error si no hay datos:**
```json
{
    "success": false,
    "error": "No hay vehículos para descargar"
}
```

## 📝 Archivos Principales

### Templates
- `templates/vehiculos.html` - Pantalla de gestión
- `templates/captura.html` - Pantalla de captura dual

### JavaScript
- `static/js/captura.js` - Lógica de captura paso a paso
  - Manejo de cámara
  - Captura secuencial (matrícula → kilometraje)
  - Comunicación con API
  - Redirección automática

### CSS
- `static/css/style.css` - Estilos actualizados
  - Tabla de vehículos
  - Botones de acción
  - Pantalla de captura
  - Responsive design

### Backend
- `app.py` - Rutas y lógica de negocio
  - `/vehiculos` - Gestión
  - `/captura` - Captura
  - `/agregar_vehiculo` - API guardar
  - `/descargar_excel` - Generación Excel

## 🔒 Seguridad

### Autenticación
- Todas las rutas requieren login (`@login_required`)
- Sesión individual por usuario
- Datos aislados por sesión

### Validación
- Validación de campos requeridos (matrícula y kilometraje)
- Limpieza de datos por Gemini Vision
- Formato de matrícula europeo
- Rango de kilometraje válido

## 📱 Compatibilidad

### Desktop
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari

### Mobile
- ✅ Chrome (Android/iOS)
- ✅ Safari (iOS)
- ⚠️ Requiere HTTPS para acceso a cámara

## 🎯 Casos de Uso

### Caso 1: Inspección de Flota
1. Inspector inicia sesión
2. Accede a `/vehiculos`
3. Click en "Iniciar Captura"
4. Captura matrícula del primer vehículo
5. Captura kilometraje del primer vehículo
6. Automáticamente vuelve a la lista
7. Repite para cada vehículo
8. Al finalizar, descarga Excel con todos los datos

### Caso 2: Registro Individual
1. Usuario inicia sesión
2. Ve la tabla vacía
3. Click en "Iniciar Captura"
4. Captura ambos datos
5. Vehículo aparece en la tabla
6. Puede descargar Excel inmediatamente

### Caso 3: Error en Captura
1. Usuario captura matrícula (Paso 1)
2. Intenta capturar kilometraje pero falla
3. Click en "✖ Cerrar"
4. Vuelve a `/vehiculos` sin guardar
5. Datos no se agregan a la tabla

## 🔧 Dependencias Nuevas

### Python
- `openpyxl==3.1.2` - Generación de archivos Excel

### Instalación
```bash
pip install openpyxl==3.1.2
```

O usar el script de instalación actualizado:
```bash
.\install.bat
```

## 📊 Mejoras Futuras Sugeridas

### Persistencia
- [ ] Guardar en base de datos SQLite
- [ ] Opción de exportar/importar CSV
- [ ] Historial de sesiones

### Funcionalidades
- [ ] Editar vehículos existentes
- [ ] Eliminar vehículos de la lista
- [ ] Filtrar/buscar en la tabla
- [ ] Ordenar por columnas
- [ ] Paginación para listas grandes

### UX
- [ ] Preview de imagen capturada
- [ ] Opción de recapturar
- [ ] Confirmación antes de guardar
- [ ] Notificaciones toast
- [ ] Animaciones de transición

### Exportación
- [ ] Exportar a PDF
- [ ] Exportar a CSV
- [ ] Incluir imágenes en el Excel
- [ ] Múltiples hojas por categoría

## 🐛 Troubleshooting

### "No hay vehículos para descargar"
- **Causa**: No se han capturado vehículos
- **Solución**: Captura al menos un vehículo antes de descargar

### La cámara no se inicia
- **Causa**: Permisos de cámara denegados o HTTP en móvil
- **Solución**: 
  - Usar HTTPS
  - Permitir acceso a cámara en configuración del navegador
  - Recargar la página

### Los datos no se guardan entre sesiones
- **Comportamiento esperado**: Los datos están en sesión
- **Solución**: Esto es por diseño. Para persistencia, se requiere base de datos

### Error al generar Excel
- **Causa**: `openpyxl` no instalado
- **Solución**: `pip install openpyxl==3.1.2`

## 📖 Documentación Relacionada

- `README.md` - Guía general de instalación
- `SISTEMA_LOGIN.md` - Sistema de autenticación
- `CONFIGURACION_GEMINI.md` - Configuración de Gemini Vision
- `RESUMEN_FUNCIONALIDADES.md` - Resumen técnico completo
