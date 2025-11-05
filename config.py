# config.py
from datetime import timedelta
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

# Chave secreta para JWT
SECRET_KEY = os.getenv("SECRET_KEY", "chave_default_para_dev")  # valor padrão só para dev

# Algoritmo de assinatura JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Tempo de expiração do access token em minutos
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Tempo de expiração do refresh token em dias
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
