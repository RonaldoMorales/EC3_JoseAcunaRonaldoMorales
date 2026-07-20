"""Persistencia de los datos scrapeados en la base de datos."""

from sqlmodel import Session, select

from database import get_session
from models import Categoria, Libro
from scraper import scrape_categoria


def _get_or_create_categoria(session: Session, nombre: str) -> Categoria:
    """Busca una categoria por nombre o la crea si no existe."""
    statement = select(Categoria).where(Categoria.nombre == nombre)
    categoria = session.exec(statement).first()

    if categoria is None:
        categoria = Categoria(nombre=nombre)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)

    return categoria


def seed_libros(
    categoria_nombre: str = "Nonfiction",
    minimo_items: int = 50,
) -> None:
    """Scrapea libros y los guarda en la base de datos sin duplicarlos."""
    libros_data = scrape_categoria(categoria_nombre, minimo_items)

    session = get_session()

    try:
        categoria = _get_or_create_categoria(session, categoria_nombre)

        nuevos = 0
        for datos in libros_data:
            ya_existe = session.exec(
                select(Libro).where(
                    Libro.titulo == datos["titulo"],
                    Libro.categoria_id == categoria.id,
                )
            ).first()

            if ya_existe is not None:
                continue

            libro = Libro(
                titulo=datos["titulo"],
                precio=datos["precio"],
                valoracion=datos["valoracion"],
                disponible=datos["disponible"],
                url_detalle=datos["url_detalle"],
                categoria_id=categoria.id,
            )
            session.add(libro)
            nuevos += 1

        session.commit()
        print(f"Libros nuevos insertados: {nuevos} de {len(libros_data)} scrapeados")

    finally:
        session.close()