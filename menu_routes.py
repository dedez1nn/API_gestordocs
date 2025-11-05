from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Cliente, Contador
from schemas import ClienteUpdate


class MenuRoutes:
    def __init__(self):
        self.router = APIRouter(
            prefix="/buscar",
            tags=["buscar"],
            dependencies=[Depends(verificar_token)]
        )

        self.router.add_api_route("/", self.home, methods=["GET"])
        self.router.add_api_route("/clientes", self.listar_clientes, methods=["GET"])
        self.router.add_api_route("/clientes/editar/{cliente_id}", self.editar_clientes, methods=["PUT"])

    async def home(self):
        return {"mensagem": "Buscar acessado"}

    def listar_clientes(
            self,
            db: Session = Depends(pegar_sessao),
            usuario_id: int = Depends(verificar_token)
    ):
        return self._listar_clientes_logic(db, usuario_id)

    def _listar_clientes_logic(self, db: Session, usuario_id: int):
        contador = db.query(Contador).filter(Contador.id == usuario_id).first()
        if not contador:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        clientes = db.query(Cliente).filter(Cliente.contador_id == usuario_id).all()

        return [
            {"id": c.id, "nome": c.nome, "email": c.email, "cnpj": c.cnpj}
            for c in clientes
        ]

    '''def listar_clientes(
            usuario_id: int = Depends(verificar_token),
            session: Session = Depends(pegar_sessao)  # session DEPOIS de usuario_id
    ):
        # Verifica se o contador existe
        contador = session.query(Contador).filter(Contador.id == usuario_id).first()
        if not contador:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        # Busca os clientes do contador
        clientes = session.query(Cliente).filter(Cliente.contador_id == usuario_id).all()

        return [
            {
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "cnpj": c.cnpj
            }
            for c in clientes
        ]'''

    def editar_clientes(
        cliente_id: int,
        novo_cliente: ClienteUpdate,
        session: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)):
        if not session.query(Contador).filter(Contador.id == usuario_id).first():
            raise HTTPException(status_code=401, detail="Acesso não autorizado")

        cliente = session.query(Cliente).filter(
            Cliente.id == novo_cliente.id,
            Cliente.contador_id == usuario_id
        ).first()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        cliente.nome = novo_cliente.nome
        cliente.email = novo_cliente.email
        cliente.cnpj = novo_cliente.cnpj

        session.commit()
        session.refresh(cliente)

        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "cnpj": cliente.cnpj
        }

'''@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso, ID: {novo_pedido.id}" }

@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado") 
    
    if pedido.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=400, detail="Voce nao tem autorizacao para fazer essa modificacao")
    
    pedido.status = "CANCELADO"
    session.commit()
    
    return {"mensagem": f"Pedido cancelado com sucesso, ID: {pedido.id}",
            "pedido": pedido
            }'''