from dotenv import load_dotenv
from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import AuthRoutes
from menu_routes import MenuRoutes

auth_routes = AuthRoutes()
menu_routes = MenuRoutes()
app.include_router(auth_routes.router)
app.include_router(menu_routes.router)