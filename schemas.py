from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ContadorSchema(BaseModel):
    email: str
    login: str
    senha: Optional[str] 
    machine_id: str
    senha_app: Optional[str]
    admin: Optional[bool] = False

    class Config:
        orm_mode = True
        from_attributes = True

class ClienteSchema(BaseModel):
    nome: Optional[str]
    email: str
    cnpj: str

    class Config:
        orm_mode = True
        from_attributes = True

class LogsEnvioSchema(BaseModel):
    usuario_id: int
    cliente_id: Optional[int]
    data_envio: Optional[datetime] = None
    arquivo: Optional[str]
    destinatario: str

    class Config:
        orm_mode = True
        from_attributes = True

class LogsAcessoSchema(BaseModel):
    id: Optional[int]
    usuario_id: int
    data_acesso: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
        
class LoginSchema(BaseModel):
    login: str
    senha: str
    machine_id: str
    
    class Config:
        from_attributes = True

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    cnpj: Optional[str] = None

    class Config:
        from_attributes = True


class SenhaAppUpdate(BaseModel):
    senha_app: str

    class Config:
        from_attributes = True


class AnexoBase64(BaseModel):
    nome_arquivo: str = Field(..., examples=["documento.pdf"])
    conteudo_base64: str = Field(..., description="PDF em formato base64")
    tipo_mime: str = Field(default="application/pdf", examples=["application/pdf"])

    class Config:
        from_attributes = True


class EmailSender(BaseModel):
    destinatario: str
    assunto: str
    corpo_email: Optional[str] = None
    anexo: AnexoBase64

    class Config:
        from_attributes = True

'''class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str 
    ativo: Optional[bool]
    admin: Optional[bool]
    
    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    usuario: int
    
    class Config:
        from_attributes = True
        
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True'''