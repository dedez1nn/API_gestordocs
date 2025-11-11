from sqlalchemy import create_engine, text

url = "postgresql+psycopg2://api_test_09ef_user:wiOvKcbOo83BRFj34Y6dQFsydbMnTImJ@dpg-d49jau7gi27c73ccos0g-a.frankfurt-postgres.render.com/api_test_09ef"
engine = create_engine(url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchall())
    print("Conectou!")
except Exception as e:
    print("Erro:", e)
