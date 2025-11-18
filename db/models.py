import os
from datetime import datetime
from sqlalchemy import DateTime, create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
db = create_engine(DATABASE_URL)


Base = declarative_base()

class Contador(Base):
    __tablename__ = "contadores"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String, nullable=False, unique=True)
    login = Column("login", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    machine_id = Column("machine_id", String, nullable=True, unique=True)
    senha_app = Column("senha_app", String)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, email, login, senha, machine_id, senha_app=None, admin=False):
        self.email = email
        self.login = login
        self.senha = senha
        self.machine_id = machine_id
        self.senha_app = senha_app
        self.admin = admin

class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, unique=True)
    email = Column("email", String, nullable=False, unique=True)
    cnpj = Column(String(14), unique=True, index=True)  
    telefone = Column(String(11))
    contador_id = Column(Integer, ForeignKey("contadores.id"), nullable=True)

    contador = relationship("Contador")

    def __init__(self, email, cnpj, nome=None, telefone = None, contador_id = None):
        self.cnpj = cnpj
        self.email = email
        self.nome = nome
        self.contador_id = contador_id
        self.telefone = telefone

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