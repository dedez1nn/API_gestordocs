from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Cliente, Contador, LogsEnvio

logs_router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    dependencies=[Depends(verificar_token)]
)

@logs_router.get("/")
async def home():
    return {"mensagem": "Buscar acessado"}

@logs_router.get("/pegar_envios")
def consultar_todos_envios(
    session: Session = Depends(pegar_sessao),
    usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    envios = session.query(LogsEnvio).filter(
        LogsEnvio.usuario_id == usuario_id
    ).order_by(LogsEnvio.data_envio.desc()).all()

    logs_formatados = []
    for envio in envios:
        logs_formatados.append({
            "destinatario": envio.destinatario,
            "data": envio.data_envio.strftime("%d/%m/%Y") if envio.data_envio else "N/A",
            "hora": envio.data_envio.strftime("%H:%M") if envio.data_envio else "N/A",
            "arquivo": envio.arquivo,
            "data_envio": envio.data_envio.isoformat() if envio.data_envio else None
        })

    return {
        "total_envios": len(envios),
        "logs": logs_formatados
    }
@logs_router.post("/salvar_envio")
def salvar_log_envio(
        log_data: dict,
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=401, detail="Contador não encontrado")

    # Buscar cliente pelo CNPJ se fornecido
    cliente_id = None
    if log_data.get("cnpj_cliente"):
        cliente = session.query(Cliente).filter(
            Cliente.cnpj == log_data["cnpj_cliente"],
            Cliente.contador_id == usuario_id
        ).first()
        if cliente:
            cliente_id = cliente.id

    # Criar log de envio
    novo_log = LogsEnvio(
        usuario_id=usuario_id,
        cliente_id=cliente_id,
        destinatario=log_data["destinatario"],
        arquivo=log_data["arquivo"],
        data_envio=datetime.now()
    )

    session.add(novo_log)
    session.commit()
    session.refresh(novo_log)

    return {
        "id": novo_log.id,
        "destinatario": novo_log.destinatario,
        "arquivo": novo_log.arquivo,
        "data_envio": novo_log.data_envio
    }