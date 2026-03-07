#!/usr/bin/env python3
"""
Script para verificar la configuración de GEMINI_API_KEY.
Uso: python verificar_gemini_key.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

def verificar_api_key():
    """Verifica y muestra información sobre la API key de Gemini"""

    print("=" * 60)
    print("VERIFICACIÓN DE GEMINI API KEY")
    print("=" * 60)
    print()

    # Obtener la API key
    api_key = os.getenv('GEMINI_API_KEY')

    # Verificar si existe
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no está configurada")
        print()
        print("Soluciones:")
        print("  1. Crear archivo .env con: GEMINI_API_KEY=tu_key_aqui")
        print("  2. Exportar variable: export GEMINI_API_KEY=tu_key_aqui")
        print("  3. Configurar en Coolify/Docker como variable de entorno")
        print()
        return False

    # Verificar longitud
    key_length = len(api_key)
    print(f"✅ GEMINI_API_KEY está configurada")
    print(f"   Longitud: {key_length} caracteres")

    # Mostrar preview segura
    if key_length > 12:
        preview = f"{api_key[:8]}...{api_key[-4:]}"
        print(f"   Preview: {preview}")
    else:
        print(f"   ⚠️  ADVERTENCIA: La key parece muy corta ({key_length} chars)")
        print(f"   Preview: {api_key[:4]}...")

    # Verificar formato esperado (keys de Google AI Studio suelen empezar con AIza)
    if api_key.startswith('AIza'):
        print(f"   ✅ Formato correcto (empieza con 'AIza')")
    else:
        print(f"   ⚠️  ADVERTENCIA: No empieza con 'AIza' (formato inesperado)")
        print(f"      Primeros caracteres: {api_key[:6]}...")

    # Verificar espacios
    if api_key != api_key.strip():
        print(f"   ⚠️  ADVERTENCIA: La key tiene espacios al inicio o final")
        return False

    print()
    print("=" * 60)
    print("TODAS LAS VARIABLES DE ENTORNO RELACIONADAS")
    print("=" * 60)
    print()

    # Mostrar otras variables relevantes
    variables = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'PORT': os.getenv('PORT'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'LOGIN_USERS': os.getenv('LOGIN_USERS'),
    }

    for key, value in variables.items():
        if value:
            if key == 'GEMINI_API_KEY':
                # Mostrar preview
                preview = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else f"{value[:4]}..."
                print(f"  {key}: {preview} ({len(value)} chars)")
            elif key == 'SECRET_KEY':
                # Ocultar secret key
                print(f"  {key}: {'*' * min(len(value), 20)} ({len(value)} chars)")
            else:
                # Mostrar completo
                print(f"  {key}: {value}")
        else:
            print(f"  {key}: ❌ No configurada")

    print()
    return True


def test_api_connection():
    """Intenta hacer una llamada de prueba a la API de Gemini"""

    print("=" * 60)
    print("TEST DE CONEXIÓN A GEMINI API")
    print("=" * 60)
    print()

    try:
        import google.generativeai as genai
        from PIL import Image
        import io

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No se puede probar: API key no configurada")
            return False

        print("🔄 Configurando Gemini...")
        genai.configure(api_key=api_key)

        print("🔄 Inicializando modelo gemini-2.5-flash...")
        model = genai.GenerativeModel('gemini-2.5-flash')

        print("🔄 Haciendo llamada de prueba...")
        # Prueba simple con texto
        response = model.generate_content("Responde solo con 'OK' si recibes este mensaje")

        print(f"✅ Conexión exitosa!")
        print(f"   Respuesta: {response.text.strip()}")
        print()

        return True

    except ImportError as e:
        print("⚠️  No se puede probar la conexión:")
        print(f"   Falta instalar: pip install google-generativeai pillow")
        print()
        return None

    except Exception as e:
        print(f"❌ ERROR al conectar con Gemini:")
        print(f"   {type(e).__name__}: {str(e)}")
        print()

        # Analizar error común
        error_str = str(e).lower()
        if 'api_key_invalid' in error_str or 'invalid api key' in error_str:
            print("💡 Causa probable: API key inválida")
            print("   Soluciones:")
            print("   1. Verificar que la key sea correcta")
            print("   2. Generar nueva key en: https://aistudio.google.com/apikey")
            print("   3. Verificar que tenga permisos para Gemini 2.5")
        elif 'quota' in error_str or 'rate limit' in error_str:
            print("💡 Causa probable: Límite de cuota alcanzado")
            print("   Espera unos minutos o verifica tu cuota en Google Cloud")
        elif 'network' in error_str or 'connection' in error_str:
            print("💡 Causa probable: Problema de conexión a internet")

        print()
        return False


if __name__ == '__main__':
    print()

    # Verificar configuración
    config_ok = verificar_api_key()

    if config_ok:
        # Si la configuración está OK, intentar test de conexión
        print()
        respuesta = input("¿Quieres probar la conexión con Gemini API? (s/n): ").strip().lower()

        if respuesta in ['s', 'si', 'y', 'yes']:
            test_api_connection()

    print("=" * 60)
    print("VERIFICACIÓN COMPLETADA")
    print("=" * 60)
    print()

    sys.exit(0 if config_ok else 1)
