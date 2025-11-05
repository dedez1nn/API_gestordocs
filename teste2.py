from sqlalchemy import create_engine, text  # note o import de text

db = create_engine("postgresql+psycopg2://postgres:mabel-francesa-roteador@localhost:5432/api_test")

with db.connect() as conn:
    result = conn.execute(text("SELECT 1"))  # use text()
    print(result.fetchone())
