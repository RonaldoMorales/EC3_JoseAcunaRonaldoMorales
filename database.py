"""Configuracion del motor de base de datos y utilidades de sesion."""

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///data.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Crea el archivo de base de datos y todas las tablas del modelo."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Retorna una nueva sesion de SQLModel conectada al engine."""
    return Session(engine)