from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Cliente, Contador
from schemas import ClienteUpdate

client_router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    dependencies=[Depends(verificar_token)]
)

@client_router.get("/buscar")
def listar_clientes(
    db: Session = Depends(pegar_sessao),
    usuario_id: int = Depends(verificar_token)
):
    return listar_clientes_logica(db, usuario_id)

def listar_clientes_logica(db: Session, usuario_id: int):
    contador = db.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    clientes = db.query(Cliente).filter(Cliente.contador_id == usuario_id).all()

    return [
        {"id": c.id, "nome": c.nome, "email": c.email, "cnpj": c.cnpj}
        for c in clientes
    ]

@client_router.put("/editar/{cliente_id}")  # ✅ CORRIGIDO: cliente_id na URL
def editar_clientes(
    cliente_id: int,  # ✅ Agora vem da URL
    novo_cliente: ClienteUpdate,
    session: Session = Depends(pegar_sessao),
    usuario_id: int = Depends(verificar_token)
):
    if not session.query(Contador).filter(Contador.id == usuario_id).first():
        raise HTTPException(status_code=401, detail="Acesso não autorizado")

    cliente = session.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.contador_id == usuario_id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Atualizar apenas os campos que foram fornecidos
    if novo_cliente.nome is not None:
        cliente.nome = novo_cliente.nome
    if novo_cliente.email is not None:
        cliente.email = novo_cliente.email
    if novo_cliente.cnpj is not None:
        cliente.cnpj = novo_cliente.cnpj

    session.commit()
    session.refresh(cliente)

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "cnpj": cliente.cnpj
    }

@client_router.post("/criar")
def criar_cliente(
        cliente_data: dict,
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
):
    """Cria um novo cliente para o contador logado"""
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=401, detail="Contador não encontrado")

    cliente_existente_cnpj = session.query(Cliente).filter(
        Cliente.cnpj == cliente_data["cnpj"],
        Cliente.contador_id == usuario_id
    ).first()

    if cliente_existente_cnpj:
        raise HTTPException(status_code=400, detail="Já existe um cliente com este CNPJ")

    cliente_existente_email = session.query(Cliente).filter(
        Cliente.email == cliente_data["email"],
        Cliente.contador_id == usuario_id
    ).first()

    if cliente_existente_email:
        raise HTTPException(status_code=400, detail="Já existe um cliente com este email")

    # ✅ CORREÇÃO: Criar cliente sem contador_id no construtor
    novo_cliente = Cliente(
        nome=cliente_data["nome"],
        email=cliente_data["email"],
        cnpj=cliente_data["cnpj"]
    )

    novo_cliente.contador_id = usuario_id

    session.add(novo_cliente)
    session.commit()
    session.refresh(novo_cliente)

    return {
        "id": novo_cliente.id,
        "nome": novo_cliente.nome,
        "email": novo_cliente.email,
        "cnpj": novo_cliente.cnpj,
        "contador_id": novo_cliente.contador_id
    }

@client_router.delete("/excluir/{cliente_id}")
def excluir_cliente(
    cliente_id: int,
    session: Session = Depends(pegar_sessao),
    usuario_id: int = Depends(verificar_token)
):
    contador = session.query(Contador).filter(Contador.id == usuario_id).first()
    if not contador:
        raise HTTPException(status_code=401, detail="Contador não encontrado")

    cliente = session.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.contador_id == usuario_id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(cliente)
    session.commit()

    return {
        "mensagem": "Cliente excluído com sucesso",
        "cliente_id": cliente_id
    }