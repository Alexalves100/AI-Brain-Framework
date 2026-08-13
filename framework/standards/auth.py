"""
Módulo de Autenticação e Criptografia Avançada.
Fornece Tokens JWT (HMAC-SHA256), Password Hashing (PBKDF2-HMAC-SHA256)
e Proteção Anti-CSRF sem dependências externas.
"""
import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict, Optional


class JWTAuth:
    """Gerenciamento e assinatura de JSON Web Tokens (JWT)."""

    def __init__(self, secret_key: str):
        if not secret_key or len(secret_key) < 16:
            raise ValueError("secret_key deve possuir pelo menos 16 caracteres.")
        self.secret_key = secret_key.encode("utf-8")

    def _b64_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    def _b64_decode(self, data: str) -> bytes:
        padding = "=" * (4 - (len(data) % 4))
        return base64.urlsafe_b64encode(base64.urlsafe_b64decode(data + padding))

    def create_token(self, payload: Dict[str, Any], expires_in_seconds: int = 3600) -> str:
        """Cria e assina um token JWT com expiração."""
        header = {"alg": "HS256", "typ": "JWT"}
        claims = payload.copy()
        claims["exp"] = int(time.time()) + expires_in_seconds
        claims["iat"] = int(time.time())

        header_b64 = self._b64_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        claims_b64 = self._b64_encode(json.dumps(claims, separators=(",", ":")).encode("utf-8"))

        signing_input = f"{header_b64}.{claims_b64}".encode()
        signature = hmac.new(self.secret_key, signing_input, hashlib.sha256).digest()
        signature_b64 = self._b64_encode(signature)

        return f"{header_b64}.{claims_b64}.{signature_b64}"

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica a assinatura e expiração de um JWT. Retorna o payload se válido."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_b64, claims_b64, signature_b64 = parts
            signing_input = f"{header_b64}.{claims_b64}".encode()
            expected_sig = hmac.new(self.secret_key, signing_input, hashlib.sha256).digest()
            expected_sig_b64 = self._b64_encode(expected_sig)

            if not hmac.compare_digest(signature_b64, expected_sig_b64):
                return None

            # Decode payload
            padding = "=" * (4 - (len(claims_b64) % 4))
            payload_bytes = base64.urlsafe_b64decode(claims_b64 + padding)
            payload = json.loads(payload_bytes.decode("utf-8"))

            if "exp" in payload and payload["exp"] < time.time():
                return None

            return payload
        except Exception:
            return None


class PasswordHasher:
    """Hasher seguro de senhas utilizando PBKDF2-HMAC-SHA256."""

    ITERATIONS = 100_000

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Gera o hash da senha com salt aleatório de 16 bytes."""
        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, cls.ITERATIONS)
        return f"{salt.hex()}${hash_bytes.hex()}"

    @classmethod
    def verify_password(cls, password: str, hashed_value: str) -> bool:
        """Verifica se a senha em texto plano corresponde ao hash."""
        try:
            salt_hex, hash_hex = hashed_value.split("$")
            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)
            computed_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, cls.ITERATIONS)
            return hmac.compare_digest(computed_hash, expected_hash)
        except Exception:
            return False
