#!/usr/bin/env python3
"""
Script simple para obtener el valor de GEMINI_API_KEY.
Uso: python get_env.py
"""

import os
from dotenv import load_dotenv

# Cargar .env si existe
load_dotenv()

# Obtener y mostrar la API key
api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print(api_key)
else:
    print("ERROR: GEMINI_API_KEY no está configurada", file=os.sys.stderr)
    os.sys.exit(1)
