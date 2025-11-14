import base64

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Contador
from schemas import SenhaAppUpdate
from config import fernet_instance

user_router = APIRouter(
    prefix="/contadores",
    tags=["contadores"],
    dependencies=[Depends(verificar_token)]
)

@user_router.get("/logado")
def get_contador_logado(
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()

    if not contador:
        raise HTTPException(status_code=404, detail="Contador não encontrado")

    return {
        "id": contador.id,
        "email": contador.email,
        "login": contador.login,
        "senha_app": contador.senha_app,
        "admin": contador.admin
    }

@user_router.put("/contador/edit/senha-app")
def atualizar_senha_app(
        senha_update: SenhaAppUpdate,
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()

    if not contador:
        raise HTTPException(status_code=404, detail="Contador não encontrado")

    try:
        senha_criptografada = fernet_instance.encrypt(senha_update.senha_app.encode())

        contador.senha_app = senha_criptografada

        session.commit()

        return {
            "mensagem": "Senha de aplicativo atualizada com sucesso",
            "email": contador.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criptografar senha: {str(e)}")

@user_router.get("/get_senha-app")
def get_contador_senha_app(session: Session = Depends(pegar_sessao), usuario_id: int = Depends(verificar_token)):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=404, detail="Erro: Usuario nao encontrado!")

    try:
        senha_contador = fernet_instance.decrypt(contador.senha_app).decode()

        return {
            "email": contador.email,
            "senha_app": senha_contador
        }
    except:
        raise HTTPException(status_code=400, detail="Erro ao criptografar senha!")


