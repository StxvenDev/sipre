import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

USER_NAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

connection_string = quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={HOST},{DB_PORT};"
    f"DATABASE={DATABASE};"
    f"UID={USER_NAME};"
    f"PWD={PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

# DATABASE_URL = f"mssql+pyodbc://{USER_NAME}:{PASSWORD}@{HOST}:1433/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server"

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={connection_string}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def test_connection():
    print(DATABASE_URL)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa:", result.scalar())
    except Exception as e:
        print("❌ Error de conexión:", e)

