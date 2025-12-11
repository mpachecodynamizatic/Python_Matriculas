// Estado de la captura
let pasoActual = 1; // 1 = matrícula, 2 = kilometraje
let matriculaCapturada = '';
let kilometrosCapturados = '';
let stream = null;
let usingCamera = true; // true = cámara, false = imagen cargada
let modoManual = false; // true = inserción manual de kilometraje

// Elementos del DOM
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const btnCapturar = document.getElementById('btn-capturar');
const btnCargar = document.getElementById('btn-cargar');
const btnManual = document.getElementById('btn-manual');
const btnTexto = document.getElementById('btn-texto');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const loader = document.getElementById('loader');
const pasoActualSpan = document.getElementById('paso-actual');
const pasoTextoSpan = document.getElementById('paso-texto');
const resultadosTemp = document.getElementById('resultados-temp');
const matriculaSpan = document.getElementById('matricula-detectada');
const kilometrosSpan = document.getElementById('kilometros-detectados');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const videoContainer = document.getElementById('video-container');
const manualInputSection = document.getElementById('manual-input-section');
const inputKilometraje = document.getElementById('input-kilometraje');
const btnConfirmarManual = document.getElementById('btn-confirmar-manual');
const btnCancelarManual = document.getElementById('btn-cancelar-manual');

// Inicializar cámara al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    iniciarCamara();
    configurarDragAndDrop();
    
    // Event listeners para entrada manual
    btnManual.addEventListener('click', mostrarEntradaManual);
    btnConfirmarManual.addEventListener('click', confirmarKilometrajeManual);
    btnCancelarManual.addEventListener('click', cancelarEntradaManual);
});

// Función para iniciar la cámara
async function iniciarCamara() {
    try {
        statusText.textContent = 'Solicitando acceso a la cámara...';
        
        // Solicitar acceso a la cámara
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment', // Preferir cámara trasera en móviles
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            }
        });
        
        video.srcObject = stream;
        
        // Esperar a que el video esté listo
        video.onloadedmetadata = () => {
            statusIndicator.classList.add('status-ready');
            statusText.textContent = 'Cámara lista - Captura la matrícula';
            btnCapturar.disabled = false;
        };
        
    } catch (error) {
        console.error('Error al acceder a la cámara:', error);
        statusIndicator.classList.add('status-error');
        statusText.textContent = 'Error: No se pudo acceder a la cámara';
        
        alert('No se pudo acceder a la cámara. Por favor:\n' +
              '1. Permite el acceso a la cámara\n' +
              '2. Verifica que estés usando HTTPS\n' +
              '3. Recarga la página');
    }
}

// Función para detener la cámara
function detenerCamara() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

// Capturar matrícula (paso 1)
async function capturarMatricula() {
    try {
        btnCapturar.disabled = true;
        mostrarLoader('Procesando matrícula...');
        
        // Capturar imagen
        const imageData = capturarImagen();
        
        // Enviar al servidor
        const response = await fetch('/ocr/matricula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const resultado = await response.json();
        
        ocultarLoader();
        
        if (resultado.exito) {
            matriculaCapturada = resultado.matricula;
            matriculaSpan.textContent = matriculaCapturada;
            resultadosTemp.style.display = 'block';
            
            // Preparar para paso 2
            prepararPaso2();
            
        } else {
            alert('Error al procesar matrícula: ' + (resultado.error || 'Error desconocido'));
            btnCapturar.disabled = false;
        }
        
    } catch (error) {
        console.error('Error:', error);
        ocultarLoader();
        alert('Error al capturar matrícula: ' + error.message);
        btnCapturar.disabled = false;
    }
}

// Capturar kilometraje (paso 2)
async function capturarKilometraje() {
    try {
        btnCapturar.disabled = true;
        mostrarLoader('Procesando kilometraje...');
        
        // Capturar imagen
        const imageData = capturarImagen();
        
        // Enviar al servidor
        const response = await fetch('/ocr/cuentakilometros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const resultado = await response.json();
        
        ocultarLoader();
        
        if (resultado.exito) {
            kilometrosCapturados = resultado.kilometros;
            kilometrosSpan.textContent = kilometrosCapturados;
            
            // Guardar vehículo y volver
            await guardarVehiculo();
            
        } else {
            alert('Error al procesar kilometraje: ' + (resultado.error || 'Error desconocido'));
            btnCapturar.disabled = false;
        }
        
    } catch (error) {
        console.error('Error:', error);
        ocultarLoader();
        alert('Error al capturar kilometraje: ' + error.message);
        btnCapturar.disabled = false;
    }
}

// Guardar vehículo en el servidor
async function guardarVehiculo() {
    try {
        mostrarLoader('Guardando vehículo...');
        
        const response = await fetch('/agregar_vehiculo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                matricula: matriculaCapturada,
                kilometros: kilometrosCapturados
            })
        });
        
        const resultado = await response.json();
        
        ocultarLoader();
        
        if (resultado.success) {
            // Detener cámara
            detenerCamara();
            
            // Redirigir a la pantalla de vehículos
            window.location.href = '/vehiculos';
        } else {
            alert('Error al guardar vehículo: ' + resultado.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        ocultarLoader();
        alert('Error al guardar vehículo: ' + error.message);
    }
}

// Capturar imagen del video
function capturarImagen() {
    // Ajustar canvas al tamaño del video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Dibujar frame del video en el canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convertir a base64
    return canvas.toDataURL('image/jpeg', 0.9);
}

// Convertir imagen cargada a base64
function imagenCargadaABase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Configurar drag and drop
function configurarDragAndDrop() {
    // Prevenir comportamiento por defecto
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        videoContainer.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Resaltar zona de drop
    ['dragenter', 'dragover'].forEach(eventName => {
        videoContainer.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        videoContainer.addEventListener(eventName, unhighlight, false);
    });
    
    // Manejar drop
    videoContainer.addEventListener('drop', handleDrop, false);
    
    // Botón cargar imagen
    btnCargar.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Click en drop zone
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Manejar selección de archivo
    fileInput.addEventListener('change', handleFiles, false);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    dropZone.style.display = 'flex';
    dropZone.classList.add('highlight');
}

function unhighlight(e) {
    dropZone.classList.remove('highlight');
    setTimeout(() => {
        if (!dropZone.classList.contains('highlight')) {
            dropZone.style.display = 'none';
        }
    }, 100);
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles({ target: { files: files } });
}

async function handleFiles(e) {
    const files = e.target.files;
    if (files.length === 0) return;
    
    const file = files[0];
    
    // Validar que sea una imagen
    if (!file.type.startsWith('image/')) {
        alert('Por favor, selecciona un archivo de imagen válido');
        return;
    }
    
    try {
        // Detener cámara si está activa
        if (stream) {
            detenerCamara();
        }
        
        // Ocultar video, mostrar canvas con la imagen
        video.style.display = 'none';
        canvas.style.display = 'block';
        dropZone.style.display = 'none';
        
        // Cargar imagen en el canvas
        const img = new Image();
        const imageData = await imagenCargadaABase64(file);
        
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            
            // Cambiar modo
            usingCamera = false;
            btnCapturar.disabled = false;
            btnCapturar.querySelector('.btn-icon').textContent = '🔍';
            btnTexto.textContent = pasoActual === 1 ? 'Procesar Matrícula' : 'Procesar Kilometraje';
            statusText.textContent = 'Imagen cargada - Lista para procesar';
            statusIndicator.classList.add('status-ready');
        };
        
        img.src = imageData;
        
    } catch (error) {
        console.error('Error cargando imagen:', error);
        alert('Error al cargar la imagen: ' + error.message);
    }
}

// Capturar o procesar según el modo
btnCapturar.addEventListener('click', async function() {
    if (usingCamera) {
        // Modo cámara: capturar
        if (pasoActual === 1) {
            await capturarMatricula();
        } else {
            await capturarKilometraje();
        }
    } else {
        // Modo imagen cargada: procesar
        if (pasoActual === 1) {
            await procesarMatriculaImagen();
        } else {
            await procesarKilometrajeImagen();
        }
    }
});

// Procesar matrícula desde imagen cargada
async function procesarMatriculaImagen() {
    try {
        btnCapturar.disabled = true;
        mostrarLoader('Procesando matrícula...');
        
        // La imagen ya está en el canvas, convertir a base64
        const imageData = canvas.toDataURL('image/jpeg', 0.9);
        
        // Enviar al servidor
        const response = await fetch('/ocr/matricula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        
        const resultado = await response.json();
        
        ocultarLoader();
        
        if (resultado.exito) {
            matriculaCapturada = resultado.matricula;
            matriculaSpan.textContent = matriculaCapturada;
            resultadosTemp.style.display = 'block';
            
            // Preparar para paso 2
            prepararPaso2();
            
        } else {
            alert('Error al procesar matrícula: ' + (resultado.error || 'Error desconocido'));
            btnCapturar.disabled = false;
        }
        
    } catch (error) {
        console.error('Error completo:', error);
        ocultarLoader();
        alert('Error al procesar matrícula: ' + error.message);
        btnCapturar.disabled = false;
    }
}

// Procesar kilometraje desde imagen cargada
async function procesarKilometrajeImagen() {
    try {
        btnCapturar.disabled = true;
        mostrarLoader('Procesando kilometraje...');
        
        // La imagen ya está en el canvas, convertir a base64
        const imageData = canvas.toDataURL('image/jpeg', 0.9);
        
        console.log('Enviando imagen de kilometraje, tamaño:', imageData.length);
        
        // Enviar al servidor
        const response = await fetch('/ocr/cuentakilometros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        console.log('Respuesta recibida:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error del servidor:', errorText);
            throw new Error(`Error del servidor (${response.status}): ${errorText.substring(0, 100)}`);
        }
        
        const resultado = await response.json();
        console.log('Resultado:', resultado);
        
        ocultarLoader();
        
        if (resultado.exito) {
            kilometrosCapturados = resultado.kilometros;
            kilometrosSpan.textContent = kilometrosCapturados;
            
            // Guardar vehículo y volver
            await guardarVehiculo();
            
        } else {
            alert('Error al procesar kilometraje: ' + (resultado.error || 'Error desconocido'));
            btnCapturar.disabled = false;
        }
        
    } catch (error) {
        console.error('Error completo:', error);
        ocultarLoader();
        alert('Error al procesar kilometraje: ' + error.message);
        btnCapturar.disabled = false;
    }
}

// Preparar interfaz para paso 2
function prepararPaso2() {
    pasoActual = 2;
    pasoActualSpan.textContent = '2';
    pasoTextoSpan.textContent = 'Kilometraje';
    
    // Verificar si hay stream de cámara activo
    const hayCamara = stream !== null;
    
    if (hayCamara && usingCamera) {
        // Cámara activa - permitir captura desde cámara
        btnTexto.textContent = 'Capturar Kilometraje';
        statusText.textContent = 'Cámara lista - Captura el kilometraje';
        btnCapturar.disabled = false;
        btnCapturar.querySelector('.btn-icon').textContent = '📸';
        video.style.display = 'block';
        canvas.style.display = 'none';
        dropZone.style.display = 'none';
        btnManual.style.display = 'inline-flex'; // Mostrar botón manual en paso 2
    } else {
        // Resetear a modo drag-and-drop
        usingCamera = false;
        btnTexto.textContent = 'Cargar Imagen';
        statusText.textContent = 'Arrastra o selecciona la imagen del kilometraje';
        statusIndicator.classList.remove('status-ready');
        
        // Mostrar drop zone
        canvas.style.display = 'none';
        video.style.display = 'none';
        dropZone.style.display = 'flex';
        btnCapturar.disabled = true;
        btnCapturar.querySelector('.btn-icon').textContent = '📁';
        btnManual.style.display = 'inline-flex'; // Mostrar botón manual en paso 2
        
        // Asegurar que el video-container sea visible
        videoContainer.style.minHeight = '480px';
    }
}

// Mostrar entrada manual de kilometraje
function mostrarEntradaManual() {
    modoManual = true;
    
    // Ocultar cámara/drop-zone
    videoContainer.style.display = 'none';
    document.querySelector('.button-section').style.display = 'none';
    
    // Mostrar entrada manual
    manualInputSection.style.display = 'block';
    inputKilometraje.value = '';
    inputKilometraje.focus();
}

// Confirmar kilometraje manual
async function confirmarKilometrajeManual() {
    const km = inputKilometraje.value.trim();
    
    // Validar entrada
    if (km === '') {
        alert('Por favor, ingresa el kilometraje');
        return;
    }
    
    const kmNumero = parseInt(km);
    if (isNaN(kmNumero) || kmNumero < 0 || kmNumero > 999999) {
        alert('Por favor, ingresa un kilometraje válido (0-999999)');
        return;
    }
    
    // Guardar kilometraje
    kilometrosCapturados = km;
    kilometrosSpan.textContent = kilometrosCapturados;
    
    // Guardar vehículo
    await guardarVehiculo();
}

// Cancelar entrada manual
function cancelarEntradaManual() {
    modoManual = false;
    
    // Ocultar entrada manual
    manualInputSection.style.display = 'none';
    
    // Mostrar cámara/drop-zone
    videoContainer.style.display = 'block';
    document.querySelector('.button-section').style.display = 'flex';
}

// Mostrar loader
function mostrarLoader(mensaje) {
    loader.querySelector('p').textContent = mensaje;
    loader.style.display = 'flex';
}

// Ocultar loader
function ocultarLoader() {
    loader.style.display = 'none';
}

// Limpiar al cerrar
window.addEventListener('beforeunload', function() {
    detenerCamara();
});
