"""Punto de entrada del proyecto EC3: scraping + persistencia + consultas."""

from database import create_db_and_tables, get_session
from queries import (
    estadisticas,
    items_por_categoria,
    top_10_por_criterio,
    total_items,
)
from seed import seed_libros


def main() -> None:
    """Crea la base de datos, ejecuta el scraping y muestra las consultas."""
    print("Creando base de datos y tablas...")
    create_db_and_tables()

    print("Ejecutando scraping y guardando datos...")
    seed_libros(categoria_nombre="Nonfiction", minimo_items=50)

    session = get_session()

    try:
        print("\n--- Consulta 1: Total de items ---")
        print(total_items(session))

        print("\n--- Consulta 2: Items por categoria ---")
        for nombre, cantidad in items_por_categoria(session):
            print(f"{nombre}: {cantidad}")

        print("\n--- Consulta 3: Top 10 por precio ---")
        for libro in top_10_por_criterio(session):
            print(f"{libro.titulo} - £{libro.precio}")

        print("\n--- Consulta 4: Estadisticas ---")
        print(estadisticas(session))

    finally:
        session.close()


if __name__ == "__main__":
    main()