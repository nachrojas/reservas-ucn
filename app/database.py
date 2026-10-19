from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Define la ruta del archivo SQLite local
DATABASE_URL = "sqlite:///./reservas.db"

# Crea el motor de conexión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Configura la fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass