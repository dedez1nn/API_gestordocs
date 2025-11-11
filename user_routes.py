import base64

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Contador
from schemas import SenhaAppUpdate, EmailSender
from config import fernet_instance
from enviar_email import Email

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

@user_router.get("/contador/senha-app")
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


@user_router.post("/enviar_email")
def enviar_email(
        email_schema: EmailSender,
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=404, detail="Erro: Usuario nao encontrado!")

    if not contador.senha_app:
        raise HTTPException(status_code=400, detail="Senha de aplicativo não encontrada!")

    try:
        senha_app_cont = fernet_instance.decrypt(contador.senha_app).decode()

        pdf_bytes = base64.b64decode(email_schema.anexo.conteudo_base64)

        email_obj = Email(
            remetente=contador.email,
            senha=senha_app_cont,
            destinatario=[email_schema.destinatario],
            assunto=email_schema.assunto
        )

        resultado = email_obj.enviar_email_com_anexo_base64(
            corpo_email=email_schema.corpo_email or "",
            pdf_bytes=pdf_bytes,
            nome_arquivo=email_schema.anexo.nome_arquivo
        )

        if resultado == 1:
            return {"status": "success", "message": "Email enviado com sucesso!"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao enviar email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


