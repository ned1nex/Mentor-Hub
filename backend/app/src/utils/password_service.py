from datetime import datetime
from uuid import uuid4
import bcrypt
import jwt


class PasswordTokenService:
    def generate_token(self, instance_id: str) -> str:
        """Генерируем токен"""
        payload = {
            "company_id": instance_id,
            "iat": datetime.utcnow(),
            "jti": str(uuid4())
        }
        
        return jwt.encode(
            payload=payload,
            algorithm="HS256",
            key=str(uuid4())
        )
    
    def hash_password(self, password: str) -> str:
        """Хешируем пароль"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()  # Store as string

    def verify_password(self, your_password: str, true_password: str) -> bool:
        """Проверяем пароль"""
        return bcrypt.checkpw(
            your_password.encode(),  # Plain password needs to be encoded
            true_password.encode()  # Stored hash needs to be encoded back to bytes
        )

    