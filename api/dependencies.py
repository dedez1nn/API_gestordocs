from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from core.config import ALGORITHM, SECRET_KEY, oauth2_schema
from db.models import Contador, db
from sqlalchemy.orm import sessionmaker


def pegar_sessao():
    try:
        SessionLocal = sessionmaker(bind=db)
        session = SessionLocal()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    print(f"Verificando token: {token}") 

    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token decodificado: {dic_info}") 

        id_contador = dic_info.get("sub")
        exp = dic_info.get("exp")

        print(f"ID do contador: {id_contador}")
        print(f"Expiração (timestamp): {exp}")

        if exp:
            from datetime import datetime
            exp_time = datetime.fromtimestamp(exp)
            now = datetime.now()

    except JWTError as e:
        print(f"Erro JWT: {e}")
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do Token")

    contador = session.query(Contador).filter(Contador.id == id_contador).first()
    if not contador:
        print(f"Contador não encontrado: {id_contador}")
        raise HTTPException(status_code=401, detail="Acesso Negado")

    print(f"Token válido para usuário: {contador.login}")
    return contador.id