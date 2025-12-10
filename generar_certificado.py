"""
Genera certificados SSL autofirmados para HTTPS
Necesario para acceso a cámara desde dispositivos móviles
"""

from OpenSSL import crypto
import os

def generar_certificado():
    """Genera certificado SSL autofirmado"""
    
    print("Generando certificado SSL autofirmado...")
    
    # Crear par de claves
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    
    # Crear certificado
    cert = crypto.X509()
    cert.get_subject().C = "ES"
    cert.get_subject().ST = "Madrid"
    cert.get_subject().L = "Madrid"
    cert.get_subject().O = "Flask OCR App"
    cert.get_subject().OU = "Development"
    cert.get_subject().CN = "localhost"
    
    # Añadir extensiones para compatibilidad
    cert.add_extensions([
        crypto.X509Extension(b"subjectAltName", False, 
                           b"DNS:localhost,IP:127.0.0.1,IP:0.0.0.0"),
    ])
    
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Válido por 1 año
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # Guardar certificado
    with open("cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    # Guardar clave privada
    with open("key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    print("✓ Certificado generado: cert.pem")
    print("✓ Clave privada generada: key.pem")
    print()
    print("IMPORTANTE:")
    print("- Este es un certificado autofirmado")
    print("- Los navegadores mostrarán una advertencia de seguridad")
    print("- Acepta la advertencia para continuar")
    print()

if __name__ == "__main__":
    generar_certificado()
