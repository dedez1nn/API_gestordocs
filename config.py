import os
import base64
import hashlib
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
KEY_APP = os.getenv("KEY_APP")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def criar_chave_fernet(senha: str):
    hash_bytes = hashlib.sha256(senha.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)

CHAVE_FERNET = criar_chave_fernet(KEY_APP)
fernet_instance = Fernet(CHAVE_FERNET)

# Contexto de hash de senha
bcrypt_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# OAuth2 esquema padrão
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")