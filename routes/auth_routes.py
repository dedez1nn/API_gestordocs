from fastapi import APIRouter, Depends, HTTPException
from db.models import Contador
from api.dependencies import pegar_sessao, verificar_token
from core.config import SECRET_KEY, ALGORITHM, bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES
from db.schemas import ContadorSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
import hashlib

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario: int, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(tz=timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    return jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

def autenticar_usuario(login, senha, session):
    usuario = session.query(Contador).filter(Contador.login == login).first()

    if not usuario or not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    return {"mensagem": "Autenticacao Acessada", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(contador_schema: ContadorSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Contador).filter(Contador.email == contador_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email ja cadastrado")
    senha_criptografada = bcrypt_context.hash(contador_schema.senha)
    machine_id_cript = hashlib.sha256(contador_schema.machine_id.encode()).hexdigest()
    novo_usuario = Contador(
        email=contador_schema.email,
        login=contador_schema.login,
        senha=senha_criptografada,
        machine_id=machine_id_cript,
        senha_app=None,
        admin=False
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuario cadastrado com sucesso {contador_schema.login}"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.login, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha invalidos")

    if usuario.machine_id is None:
        usuario.machine_id = login_schema.machine_id
        session.commit()
    else:
        if usuario.machine_id != login_schema.machine_id:
            raise HTTPException(status_code=403, detail="Dispositivo nao autorizado")

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "email": usuario.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email nao cadastrado ou credenciais invalidas")
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Contador = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "bearer"}
