/**
 * Script para manejo de cámara y captura de imágenes
 * Implementa la lógica de captura y envío a endpoints de OCR
 */

// Variables globales
let videoStream = null;
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const btnMatricula = document.getElementById('btn-matricula');
const btnCuentakilometros = document.getElementById('btn-cuentakilometros');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const resultadoContainer = document.getElementById('resultado-container');
const resultadoContenido = document.getElementById('resultado-contenido');
const btnCerrar = document.getElementById('btn-cerrar');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const loader = document.getElementById('loader');

/**
 * Inicializa la cámara del dispositivo
 */
async function inicializarCamara() {
    try {
        statusText.textContent = 'Solicitando acceso a la cámara...';
        
        // Solicitar acceso a la cámara
        const constraints = {
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: 'environment' // Cámara trasera en móviles
            }
        };
        
        videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = videoStream;
        
        // Esperar a que el video esté listo
        video.onloadedmetadata = () => {
            statusText.textContent = 'Cámara lista ✓';
            statusIndicator.classList.add('active');
            
            // Habilitar botones
            btnMatricula.disabled = false;
            btnCuentakilometros.disabled = false;
        };
        
    } catch (error) {
        console.error('Error al acceder a la cámara:', error);
        statusText.textContent = 'Error: No se puede acceder a la cámara';
        
        // Mostrar mensaje de error más detallado
        mostrarError(
            'No se pudo acceder a la cámara',
            'Asegúrate de que tu dispositivo tiene cámara y de que has dado permisos al navegador.'
        );
    }
}

/**
 * Captura una imagen del video
 * @returns {string} Imagen en formato base64
 */
function capturarImagen() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Dibujar el frame actual del video en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convertir a base64
    const imagenBase64 = canvas.toDataURL('image/jpeg', 0.95);
    
    // Mostrar preview
    previewImage.src = imagenBase64;
    previewContainer.style.display = 'block';
    
    return imagenBase64;
}

/**
 * Procesa la imagen capturada en el endpoint especificado
 * @param {string} endpoint - URL del endpoint (/ocr/matricula o /ocr/cuentakilometros)
 * @param {string} tipo - Tipo de procesamiento ('matrícula' o 'cuentakilómetros')
 */
async function procesarImagen(endpoint, tipo) {
    try {
        // Capturar imagen
        const imagenBase64 = capturarImagen();
        
        // Mostrar loader
        loader.style.display = 'flex';
        
        // Enviar al servidor
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imagenBase64
            })
        });
        
        const resultado = await response.json();
        
        // Ocultar loader
        loader.style.display = 'none';
        
        // Mostrar resultado
        mostrarResultado(resultado, tipo);
        
    } catch (error) {
        console.error('Error al procesar imagen:', error);
        loader.style.display = 'none';
        mostrarError(
            'Error de conexión',
            'No se pudo procesar la imagen. Verifica tu conexión e intenta nuevamente.'
        );
    }
}

/**
 * Muestra el resultado del procesamiento OCR
 * @param {object} resultado - Objeto con el resultado del OCR
 * @param {string} tipo - Tipo de procesamiento
 */
function mostrarResultado(resultado, tipo) {
    resultadoContainer.style.display = 'block';
    
    let html = '';
    
    if (resultado.success) {
        // Determinar nivel de confianza
        let confianzaClase = 'confianza-baja';
        if (resultado.confianza >= 80) {
            confianzaClase = 'confianza-alta';
        } else if (resultado.confianza >= 60) {
            confianzaClase = 'confianza-media';
        }
        
        html = `
            <div class="resultado-item">
                <span class="resultado-label">Tipo:</span>
                <span class="resultado-valor">${tipo}</span>
            </div>
            <div class="resultado-item">
                <span class="resultado-label">Texto Reconocido:</span>
                <span class="resultado-valor resultado-success">${resultado.texto}</span>
            </div>
            <div class="resultado-item">
                <span class="resultado-label">Confianza:</span>
                <span class="confianza-badge ${confianzaClase}">${resultado.confianza}%</span>
            </div>
            <div class="resultado-item">
                <span class="resultado-label">Estado:</span>
                <span class="resultado-valor resultado-success">✓ ${resultado.mensaje}</span>
            </div>
        `;
        
        // Mostrar modo de OCR usado
        if (resultado.modo) {
            const modoIcono = resultado.modo.includes('IA') ? '🤖' : '⚙️';
            document.getElementById('resultado-modo').innerHTML = 
                `${modoIcono} Procesado con: <strong>${resultado.modo}</strong>`;
            document.getElementById('resultado-modo').style.display = 'block';
        }
    } else {
        html = `
            <div class="resultado-item">
                <span class="resultado-label">Tipo:</span>
                <span class="resultado-valor">${tipo}</span>
            </div>
            <div class="resultado-item">
                <span class="resultado-label">Estado:</span>
                <span class="resultado-valor resultado-error">✗ Error</span>
            </div>
            <div class="resultado-item">
                <span class="resultado-label">Mensaje:</span>
                <span class="resultado-valor resultado-error">${resultado.mensaje || resultado.error}</span>
            </div>
        `;
        
        if (resultado.texto) {
            html += `
                <div class="resultado-item">
                    <span class="resultado-label">Texto Parcial:</span>
                    <span class="resultado-valor">${resultado.texto}</span>
                </div>
            `;
        }
        
        // Mostrar modo incluso en error
        if (resultado.modo) {
            const modoIcono = resultado.modo.includes('IA') ? '🤖' : '⚙️';
            document.getElementById('resultado-modo').innerHTML = 
                `${modoIcono} Modo: <strong>${resultado.modo}</strong>`;
            document.getElementById('resultado-modo').style.display = 'block';
        }
    }
    
    resultadoContenido.innerHTML = html;
    
    // Scroll al resultado
    resultadoContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Muestra un mensaje de error
 * @param {string} titulo - Título del error
 * @param {string} mensaje - Mensaje detallado
 */
function mostrarError(titulo, mensaje) {
    resultadoContainer.style.display = 'block';
    
    const html = `
        <div class="resultado-item">
            <span class="resultado-label">Error:</span>
            <span class="resultado-valor resultado-error">${titulo}</span>
        </div>
        <div class="resultado-item">
            <span class="resultado-label">Detalles:</span>
            <span class="resultado-valor">${mensaje}</span>
        </div>
    `;
    
    resultadoContenido.innerHTML = html;
    resultadoContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Oculta el contenedor de resultados
 */
function cerrarResultado() {
    resultadoContainer.style.display = 'none';
    previewContainer.style.display = 'none';
}

// Event Listeners
btnMatricula.addEventListener('click', () => {
    procesarImagen('/ocr/matricula', 'Matrícula');
});

btnCuentakilometros.addEventListener('click', () => {
    procesarImagen('/ocr/cuentakilometros', 'Cuentakilómetros');
});

btnCerrar.addEventListener('click', cerrarResultado);

// Inicializar cámara al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    inicializarCamara();
});

// Detener cámara al cerrar la página
window.addEventListener('beforeunload', () => {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }
});

// Manejo de errores globales
window.addEventListener('error', (event) => {
    console.error('Error global:', event.error);
});

// Soporte para navegadores sin MediaDevices
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    statusText.textContent = 'Tu navegador no soporta acceso a la cámara';
    mostrarError(
        'Navegador no compatible',
        'Por favor, usa un navegador moderno como Chrome, Firefox, Safari o Edge.'
    );
}
