"""Consultas de verificacion sobre los datos scrapeados."""

from sqlmodel import Session, func, select

from models import Categoria, Libro


def total_items(session: Session) -> int:
    """Retorna el numero total de libros almacenados en la base de datos."""
    statement = select(func.count(Libro.id))
    return session.exec(statement).one()


def items_por_categoria(session: Session) -> list[tuple[str, int]]:
    """Retorna la cantidad de libros por categoria, de mayor a menor."""
    statement = (
        select(Categoria.nombre, func.count(Libro.id))
        .join(Libro, Libro.categoria_id == Categoria.id)
        .group_by(Categoria.nombre)
        .order_by(func.count(Libro.id).desc())
    )
    return list(session.exec(statement).all())


def top_10_por_criterio(session: Session) -> list[Libro]:
    """Retorna los 10 libros con el precio mas alto.

    Se elige precio como criterio numerico porque es el campo mas
    representativo del valor comercial de un libro en el catalogo.
    """
    statement = select(Libro).order_by(Libro.precio.desc()).limit(10)
    return list(session.exec(statement).all())


def estadisticas(session: Session) -> dict:
    """Retorna promedio, minimo y maximo de precio, global y por categoria."""
    global_stmt = select(
        func.avg(Libro.precio),
        func.min(Libro.precio),
        func.max(Libro.precio),
    )
    promedio, minimo, maximo = session.exec(global_stmt).one()

    por_categoria: dict[str, dict[str, float]] = {}
    categoria_stmt = (
        select(
            Categoria.nombre,
            func.avg(Libro.precio),
            func.min(Libro.precio),
            func.max(Libro.precio),
        )
        .join(Libro, Libro.categoria_id == Categoria.id)
        .group_by(Categoria.nombre)
    )
    for nombre, avg_p, min_p, max_p in session.exec(categoria_stmt).all():
        por_categoria[nombre] = {
            "promedio": round(avg_p, 2) if avg_p else 0.0,
            "minimo": min_p,
            "maximo": max_p,
        }

    return {
        "global": {
            "promedio": round(promedio, 2) if promedio else 0.0,
            "minimo": minimo,
            "maximo": maximo,
        },
        "por_categoria": por_categoria,
    }