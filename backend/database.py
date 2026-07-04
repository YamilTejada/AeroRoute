import os #Trabajar con los archivos del SO (Nos servirá para trabajar .env)
from dotenv import load_dotenv #Buscar archivo .env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# 1. Cargar las variables de entorno del archivo .env
load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")

is_sqlite = False

try:
    if not HOST or not USER:
        raise ValueError("Variables de entorno para PostgreSQL incompletas.")
    
    # Construir la URL de conexión segura
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
    
    # Probar conexión inmediatamente
    with engine.connect() as conn:
        pass
    print("Conexión exitosa a PostgreSQL (Supabase).")
except Exception as e:
    print(f"No se pudo conectar a PostgreSQL: {e}")
    print("Cambiando a base de datos local SQLite (Opción B)...")
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_airports.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    is_sqlite = True

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
