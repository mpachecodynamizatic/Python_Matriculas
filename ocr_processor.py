import google.generativeai as genai
import pytesseract
import requests
import base64
import os
from PIL import Image
import cv2
import numpy as np
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Tesseract (Windows)
# Si Tesseract está en PATH, no es necesario configurar
# Si no, descomentar y ajustar la ruta:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración de Gemini
def get_gemini_model():
    """Obtiene el modelo de Gemini configurado"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

class OCRProcessor:
    def __init__(self, motor='gemini'):
        """
        Inicializa el procesador OCR
        
        Args:
            motor: Motor OCR a usar ('gemini', 'tesseract' o 'ocrspace')
        """
        self.motor = motor
        self.model = None
        self.ocrspace_api_key = os.getenv('OCRSPACE_API_KEY', 'K87899142388957')  # API key gratuita por defecto
        
        if motor == 'gemini':
            try:
                self.model = get_gemini_model()
            except Exception as e:
                print(f"Advertencia: No se pudo inicializar Gemini: {e}")
                print("Cambiando a Tesseract...")
                self.motor = 'tesseract'
    
    def extraer_texto_ocr(self, imagen_path, tipo_ocr):
        """
        Extrae texto de una imagen usando el motor configurado
        
        Args:
            imagen_path: Ruta a la imagen o array numpy
            tipo_ocr: Tipo de OCR ('matricula' o 'cuentakilometros')
            
        Returns:
            dict: Resultado del OCR con texto y confianza
        """
        if self.motor == 'gemini' and self.model:
            return self._extraer_texto_gemini(imagen_path, tipo_ocr)
        elif self.motor == 'ocrspace':
            return self._extraer_texto_ocrspace(imagen_path, tipo_ocr)
        else:
            return self._extraer_texto_tesseract(imagen_path, tipo_ocr)
    
    def _extraer_texto_gemini(self, imagen_path, tipo_ocr):
        """Extrae texto usando Gemini Vision API"""
        try:
            # Cargar imagen (puede ser ruta o array numpy)
            if isinstance(imagen_path, str):
                # Es una ruta de archivo
                img = Image.open(imagen_path)
            elif isinstance(imagen_path, np.ndarray):
                # Es un array de OpenCV (BGR)
                # Convertir de BGR a RGB
                img_rgb = cv2.cvtColor(imagen_path, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img_rgb)
            else:
                raise ValueError("imagen_path debe ser una ruta de archivo o array numpy")
            
            # Definir prompts específicos según el tipo
            if tipo_ocr == 'matricula':
                prompt = """Analiza esta imagen de una matrícula de vehículo europea.
                Extrae ÚNICAMENTE los caracteres de la matrícula (letras y números).
                Responde solo con los caracteres encontrados, sin espacios ni guiones.
                Si no detectas una matrícula clara, responde 'NO_DETECTADO'."""
            else:  # cuentakilometros
                prompt = """Analiza esta imagen del cuentakilómetros de un vehículo.
                Extrae ÚNICAMENTE los números del odómetro principal (los kilómetros totales).
                Ignora cualquier otro número (velocidad, rpm, combustible, etc.).
                Responde solo con los dígitos encontrados, sin espacios, puntos ni comas.
                Si no detectas números claros del odómetro, responde 'NO_DETECTADO'."""
            
            # Generar contenido con Gemini
            response = self.model.generate_content([prompt, img])
            
            # Procesar respuesta
            texto = response.text.strip()
            
            # Validar respuesta
            if not texto or texto == 'NO_DETECTADO':
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'gemini',
                    'error': 'No se detectó texto válido'
                }
            
            # Limpiar texto según el tipo
            if tipo_ocr == 'matricula':
                texto = self.limpiar_matricula(texto)
            else:
                texto = self.limpiar_cuentakilometros(texto)
            
            return {
                'texto': texto,
                'confianza': 0.95,  # Gemini es muy confiable
                'metodo': 'gemini'
            }
            
        except Exception as e:
            return {
                'texto': '',
                'confianza': 0.0,
                'metodo': 'gemini',
                'error': str(e)
            }
    
    def _extraer_texto_ocrspace(self, imagen_path, tipo_ocr):
        """Extrae texto usando OCR.space API (gratuita - 25,000 peticiones/mes)"""
        try:
            # Convertir imagen a base64
            if isinstance(imagen_path, str):
                with open(imagen_path, 'rb') as f:
                    imagen_data = base64.b64encode(f.read()).decode()
            elif isinstance(imagen_path, np.ndarray):
                # Convertir array numpy a bytes
                _, buffer = cv2.imencode('.jpg', imagen_path)
                imagen_data = base64.b64encode(buffer).decode()
            else:
                raise ValueError("imagen_path debe ser una ruta o array numpy")
            
            # Llamar a OCR.space API
            url = 'https://api.ocr.space/parse/image'
            payload = {
                'apikey': self.ocrspace_api_key,
                'base64Image': f'data:image/jpeg;base64,{imagen_data}',
                'language': 'spa',
                'isOverlayRequired': False,
                'OCREngine': 2  # Motor 2 para mejor precisión
            }
            
            response = requests.post(url, data=payload, timeout=30)
            result = response.json()
            
            if result.get('IsErroredOnProcessing', True):
                error_msg = result.get('ErrorMessage', ['Error desconocido'])[0]
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'ocrspace',
                    'error': error_msg
                }
            
            # Extraer texto
            parsed_results = result.get('ParsedResults', [])
            if not parsed_results:
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'ocrspace',
                    'error': 'No se detectó texto'
                }
            
            texto = parsed_results[0].get('ParsedText', '').strip()
            
            if not texto:
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'ocrspace',
                    'error': 'No se detectó texto válido'
                }
            
            # Limpiar texto según el tipo
            if tipo_ocr == 'matricula':
                texto = self.limpiar_matricula(texto)
            else:
                texto = self.limpiar_cuentakilometros(texto)
            
            # Validar que después de limpiar aún hay texto
            if not texto:
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'ocrspace',
                    'error': 'No se detectó texto válido después de procesar'
                }
            
            return {
                'texto': texto,
                'confianza': 0.80,
                'metodo': 'ocrspace'
            }
            
        except requests.exceptions.Timeout:
            return {
                'texto': '',
                'confianza': 0.0,
                'metodo': 'ocrspace',
                'error': 'Timeout en la API (30s)'
            }
        except Exception as e:
            return {
                'texto': '',
                'confianza': 0.0,
                'metodo': 'ocrspace',
                'error': str(e)
            }
    
    def _extraer_texto_tesseract(self, imagen_path, tipo_ocr):
        """Extrae texto usando Tesseract OCR"""
        try:
            # Cargar imagen (puede ser ruta o array numpy)
            if isinstance(imagen_path, str):
                # Es una ruta de archivo
                img = cv2.imread(imagen_path)
            elif isinstance(imagen_path, np.ndarray):
                # Es un array de OpenCV (BGR)
                img = imagen_path
            else:
                raise ValueError("imagen_path debe ser una ruta de archivo o array numpy")
            
            # Preprocesar imagen para mejorar OCR
            img_procesada = self._preprocesar_imagen_tesseract(img, tipo_ocr)
            
            # Configurar Tesseract según el tipo
            if tipo_ocr == 'matricula':
                # Para matrículas: solo letras y números
                config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            else:
                # Para kilometraje: solo números
                config = '--psm 7 -c tessedit_char_whitelist=0123456789'
            
            # Extraer texto
            texto = pytesseract.image_to_string(img_procesada, config=config, lang='eng')
            texto = texto.strip()
            
            # Limpiar texto según el tipo
            if tipo_ocr == 'matricula':
                texto = self.limpiar_matricula(texto)
            else:
                texto = self.limpiar_cuentakilometros(texto)
            
            if texto:
                return {
                    'texto': texto,
                    'confianza': 0.75,  # Tesseract tiene menor confianza que Gemini
                    'metodo': 'tesseract'
                }
            else:
                return {
                    'texto': '',
                    'confianza': 0.0,
                    'metodo': 'tesseract',
                    'error': 'No se detectó texto válido'
                }
                
        except Exception as e:
            return {
                'texto': '',
                'confianza': 0.0,
                'metodo': 'tesseract',
                'error': str(e)
            }
    
    def _preprocesar_imagen_tesseract(self, img, tipo_ocr):
        """Preprocesa la imagen para mejorar el OCR de Tesseract"""
        # Convertir a escala de grises
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Aplicar threshold adaptativo
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Reducir ruido
        gray = cv2.medianBlur(gray, 3)
        
        # Dilatar para unir caracteres cercanos (útil para matrículas)
        if tipo_ocr == 'matricula':
            kernel = np.ones((2, 2), np.uint8)
            gray = cv2.dilate(gray, kernel, iterations=1)
        
        return gray
    
    def limpiar_matricula(self, texto):
        """Limpia y valida el formato de matrícula"""
        # Eliminar espacios, guiones y caracteres no alfanuméricos
        texto = re.sub(r'[^A-Z0-9]', '', texto.upper())
        
        # Validar formato europeo típico (4 números + 3 letras o similar)
        if len(texto) < 4 or len(texto) > 10:
            return ''
        
        return texto
    
    def limpiar_cuentakilometros(self, texto):
        """Limpia y valida los números del cuentakilómetros"""
        # Extraer solo dígitos
        texto = re.sub(r'[^0-9]', '', texto)
        
        # Validar rango razonable (entre 0 y 999999 km)
        if not texto or len(texto) > 6:
            return ''
        
        # Eliminar ceros a la izquierda pero mantener al menos un dígito
        texto = texto.lstrip('0') or '0'
        
        return texto
    
    def procesar_matricula(self, imagen_path):
        """
        Procesa una imagen de matrícula
        
        Args:
            imagen_path: Ruta a la imagen
            
        Returns:
            dict: Resultado del procesamiento
        """
        resultado = self.extraer_texto_ocr(imagen_path, 'matricula')
        texto = resultado.get('texto', '')
        
        if texto:
            return {
                'exito': True,
                'matricula': texto,
                'confianza': resultado.get('confianza', 0.0),
                'metodo': resultado.get('metodo', 'gemini')
            }
        else:
            return {
                'exito': False,
                'error': resultado.get('error', 'No se pudo detectar la matrícula'),
                'metodo': resultado.get('metodo', 'gemini')
            }
    
    def procesar_cuentakilometros(self, imagen_path):
        """
        Procesa una imagen de cuentakilómetros
        
        Args:
            imagen_path: Ruta a la imagen
            
        Returns:
            dict: Resultado del procesamiento
        """
        resultado = self.extraer_texto_ocr(imagen_path, 'cuentakilometros')
        texto = resultado.get('texto', '')
        
        if texto:
            return {
                'exito': True,
                'kilometros': texto,
                'confianza': resultado.get('confianza', 0.0),
                'metodo': resultado.get('metodo', 'gemini')
            }
        else:
            return {
                'exito': False,
                'error': resultado.get('error', 'No se pudieron detectar los kilómetros'),
                'metodo': resultado.get('metodo', 'gemini')
            }
