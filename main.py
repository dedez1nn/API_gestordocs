from fastapi import FastAPI
app = FastAPI()

from auth_routes import auth_router
from logs_routes import logs_router
from user_routes import user_router
from client_routes import client_router

app.include_router(auth_router)
app.include_router(logs_router)
app.include_router(user_router)
app.include_router(client_router)