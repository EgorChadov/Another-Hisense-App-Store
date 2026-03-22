import uvicorn
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CERT_FILE = BASE_DIR / "cert.pem"
KEY_FILE = BASE_DIR / "key.pem"

# HTTPS settings
USE_HTTPS = True
HTTPS_PORT = 443
HTTP_PORT = 80


def generate_self_signed_cert():
    """Generate self-signed certificate if not exists."""
    if CERT_FILE.exists() and KEY_FILE.exists():
        print(f"Using existing certificate: {CERT_FILE}")
        return True

    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        import datetime

        print("Generating self-signed certificate...")

        # Generate private key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Hisense App Store"),
            x509.NameAttribute(NameOID.COMMON_NAME, "vidaahub.com"),
        ])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("vidaahub.com"),
                    x509.DNSName("*.vidaahub.com"),
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                ]),
                critical=False,
            )
            .sign(key, hashes.SHA256(), default_backend())
        )

        # Save private key
        with open(KEY_FILE, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Save certificate
        with open(CERT_FILE, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        print(f"Certificate generated: {CERT_FILE}")
        return True

    except ImportError:
        print("ERROR: 'cryptography' package not installed.")
        print("Run: pip install cryptography")
        return False
    except Exception as e:
        print(f"ERROR generating certificate: {e}")
        return False


if __name__ == "__main__":
    import ipaddress  # for certificate generation

    if USE_HTTPS:
        if generate_self_signed_cert():
            print(f"Starting HTTPS server on port {HTTPS_PORT}...")
            uvicorn.run(
                "app.main:app",
                host="0.0.0.0",
                port=HTTPS_PORT,
                reload=True,
                log_level="info",
                ssl_keyfile=str(KEY_FILE),
                ssl_certfile=str(CERT_FILE),
            )
        else:
            print("Failed to setup HTTPS, falling back to HTTP...")
            uvicorn.run(
                "app.main:app",
                host="0.0.0.0",
                port=HTTP_PORT,
                reload=True,
                log_level="info",
            )
    else:
        print(f"Starting HTTP server on port {HTTP_PORT}...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=HTTP_PORT,
            reload=True,
            log_level="info",
        )
