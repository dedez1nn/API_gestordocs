from datetime import datetime
from sqlalchemy import DateTime, create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("postgresql+psycopg2://postgres:mabel123@localhost:5432/api_test")


Base = declarative_base()

class Contador(Base):
    __tablename__ = "contadores"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String, nullable=False, unique=True)
    login = Column("login", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    machine_id = Column("machine_id", String, nullable=False, unique=True)
    senha_app = Column("senha_app", String)
    admin = Column("admin", Boolean, default=False)
    
    def __init__(self, email, login, senha, machine_id, senha_app=None, admin=False):
        self.email = email
        self.login = login
        self.senha = senha
        self.machine_id = machine_id
        self.senha_app = senha_app
        
class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, unique=True)
    email = Column("email", String, nullable=False, unique=True)
    cnpj = Column("cnpj", String, nullable=False, unique=True)
    contador_id = Column(Integer, ForeignKey("contadores.id"), nullable=True)

    contador = relationship("Contador")
    
    def __init__(self, email, cnpj, nome=None):
        self.cnpj = cnpj
        self.email = email
        self.nome = nome

class LogsEnvio(Base):
    __tablename__ = "logs_envio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("contadores.id", ondelete="CASCADE"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="SET NULL"), nullable=True)
    data_envio = Column(DateTime, default=datetime.utcnow, nullable=False)
    arquivo = Column(String, nullable=True)
    destinatario = Column(String(255), nullable=False)
    
class LogsAcesso(Base):
    __tablename__ = "logs_acesso"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("contadores.id", ondelete="CASCADE"), nullable=False)
    data_acesso = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.data_acesso = datetime.utcnow

'''class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"
    
    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO"),
    )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco
        
class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido'''