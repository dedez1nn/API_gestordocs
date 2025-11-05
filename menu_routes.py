from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Cliente, Contador

class MenuRoutes:
    def __init__(self):
        self.router = APIRouter(
            prefix="/buscar",
            tags=["buscar"],
            dependencies=[Depends(verificar_token)]
        )

        self.router.add_api_route("/", self.home, methods=["GET"])
        self.router.add_api_route("/clientes", self.listar_clientes, methods=["GET"])
        self.router.add_api_route("/clientes/editar", self.editar_clientes, methods=["P"])

    async def home(self):
        return {"mensagem": "Buscar acessado"}

    async def listar_clientes(
        self,
        db: Session = Depends(pegar_sessao),
        usuario_id: int = Depends(verificar_token)
    ):
        usuario = db.query(Contador).filter(Contador.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        clientes = db.query(Cliente).all()
        resultado = [
            {
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "cnpj": c.cnpj
            }
            for c in clientes
        ]
        return resultado

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