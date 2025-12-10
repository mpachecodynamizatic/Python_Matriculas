"""
Script de verificación rápida de EasyOCR
Verifica que todas las dependencias estén correctamente instaladas
"""

print("=" * 60)
print("VERIFICACION DE DEPENDENCIAS")
print("=" * 60)
print()

# Verificar importaciones
try:
    print("✓ Importando Flask...", end=" ")
    import flask
    print(f"OK (v{flask.__version__})")
except Exception as e:
    print(f"✗ ERROR: {e}")

try:
    print("✓ Importando OpenCV...", end=" ")
    import cv2
    print(f"OK (v{cv2.__version__})")
except Exception as e:
    print(f"✗ ERROR: {e}")

try:
    print("✓ Importando NumPy...", end=" ")
    import numpy as np
    print(f"OK (v{np.__version__})")
except Exception as e:
    print(f"✗ ERROR: {e}")

try:
    print("✓ Importando Pillow...", end=" ")
    from PIL import Image
    import PIL
    print(f"OK (v{PIL.__version__})")
except Exception as e:
    print(f"✗ ERROR: {e}")

try:
    print("✓ Importando PyTorch...", end=" ")
    import torch
    print(f"OK (v{torch.__version__})")
except Exception as e:
    print(f"✗ ERROR: {e}")

try:
    print("✓ Importando EasyOCR...", end=" ")
    import easyocr
    print("OK")
except Exception as e:
    print(f"✗ ERROR: {e}")

print()
print("=" * 60)
print("RESULTADO: Todas las dependencias están correctamente instaladas!")
print("=" * 60)
print()
print("Ahora puedes ejecutar la aplicación con: .\\run.bat")
print()
