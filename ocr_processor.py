import google.generativeai as genai
import os
from PIL import Image
import cv2
import numpy as np
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Gemini
def get_gemini_model():
    """Obtiene el modelo de Gemini configurado"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        error_msg = "No se encontró GEMINI_API_KEY en las variables de entorno"
        print(f"ERROR: {error_msg}")
        print(f"Variables de entorno disponibles: {list(os.environ.keys())}")
        raise ValueError(error_msg)
    
    print(f"INFO: Configurando Gemini con API Key: {api_key[:10]}...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("INFO: Modelo Gemini configurado correctamente")
        return model
    except Exception as e:
        print(f"ERROR al configurar Gemini: {str(e)}")
        raise

class OCRProcessor:
    def __init__(self, motor='gemini'):
        """
        Inicializa el procesador OCR con Gemini
        
        Args:
            motor: Motor OCR a usar (solo 'gemini' soportado)
        """
        self.motor = motor
        self.model = None
        
        print(f"INFO: Inicializando OCRProcessor con motor: {motor}")
        if motor == 'gemini':
            try:
                self.model = get_gemini_model()
                print("INFO: OCRProcessor inicializado correctamente")
            except Exception as e:
                error_msg = f"No se pudo inicializar Gemini: {e}"
                print(f"ERROR: {error_msg}")
                raise ValueError(error_msg)
    
    def extraer_texto_ocr(self, imagen_path, tipo_ocr):
        """
        Extrae texto de una imagen usando Gemini Vision
        
        Args:
            imagen_path: Ruta a la imagen o array numpy
            tipo_ocr: Tipo de OCR ('matricula' o 'cuentakilometros')
            
        Returns:
            dict: Resultado del OCR con texto y confianza
        """
        return self._extraer_texto_gemini(imagen_path, tipo_ocr)
    
    def _extraer_texto_gemini(self, imagen_path, tipo_ocr):
        """Extrae texto usando Gemini Vision API"""
        try:
            print(f"INFO: Procesando imagen con Gemini - Tipo: {tipo_ocr}")
            
            # Cargar imagen (puede ser ruta o array numpy)
            if isinstance(imagen_path, str):
                # Es una ruta de archivo
                img = Image.open(imagen_path)
                print(f"INFO: Imagen cargada desde archivo: {imagen_path}")
            elif isinstance(imagen_path, np.ndarray):
                # Es un array de OpenCV (BGR)
                # Convertir de BGR a RGB
                img_rgb = cv2.cvtColor(imagen_path, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img_rgb)
                print(f"INFO: Imagen convertida desde numpy array - Shape: {imagen_path.shape}")
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
            print(f"INFO: Enviando petición a Gemini API...")
            response = self.model.generate_content([prompt, img])
            print(f"INFO: Respuesta recibida de Gemini")
            
            # Procesar respuesta
            texto = response.text.strip()
            print(f"INFO: Texto extraído: '{texto}'")
            
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
            error_msg = str(e)
            print(f"ERROR en _extraer_texto_gemini: {error_msg}")
            print(f"Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return {
                'texto': '',
                'confianza': 0.0,
                'metodo': 'gemini',
                'error': error_msg
            }
    
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
