# API – GestorDocs  
API responsável pela comunicação entre o sistema de automação de e-mails e o banco de dados principal.  
Desenvolvida em **FastAPI**, utilizando **SQLAlchemy ORM** e **PostgreSQL**, essa API fornece endpoints para cadastro de usuários, armazenamento de documentos, envio automatizado de e-mails e integração direta com o aplicativo desktop.

---

## Tecnologias Utilizadas

- **FastAPI** — Framework moderno e rápido para criação de APIs REST.
- **SQLAlchemy ORM** — ORM utilizado para modelagem, consultas e relacionamento de dados.
- **PostgreSQL** — Banco de dados principal da aplicação.
- **Alembic** — Ferramenta utilizada para gerenciamento de migrações.
- **Pydantic** — Validação e tipagem de dados nos endpoints.
- **Uvicorn/Gunicorn** — Servidor ASGI para produção.

---

## Estrutura Geral (exemplo)

```
/app
 ├── main.py
 ├── database.py
 ├── models/
 ├── routers/
 ├── schemas/
 └── utils/
```

---

## Funcionalidades Principais

- Cadastro, edição e remoção de usuários.
- Registro e gerenciamento de documentos vinculados.
- Integração com o automatizador de envio de e-mails.
- Endpoints organizados por rotas separadas.
- Conexão otimizada com PostgreSQL usando SQLAlchemy.
- Migrações automáticas com Alembic.
- Respostas rápidas e validadas via FastAPI + Pydantic.

---

## Segurança

- Estrutura pronta para incluir autenticação JWT.
- Sanitização e validação rigorosa de dados.
- Configuração de CORS e controle de acesso.

---

## Build & Deploy

A API é totalmente compatível com deploy em plataformas como Render, Railway e Docker.  
Exemplo de comando de execução:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Banco de Dados

- Configurado com SQLAlchemy ORM.
- Uso de sessionmaker para controle de transações.
- Migrações gerenciadas via Alembic.
- Suporte a PostgreSQL hospedado em nuvem.

---

## Integração com o Aplicativo Desktop

A API atua como ponto central para:

- Armazenar registros no banco.
- Consultar usuários para disparo automático de e-mails.
- Controlar o fluxo dos documentos processados.
- Garantir sincronização entre desktop e servidor.

---

## Licença

Projeto de uso pessoal/estudo.  
Sinta-se à vontade para enviar PRs ou sugestões.
