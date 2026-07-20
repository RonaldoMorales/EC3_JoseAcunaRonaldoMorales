"""Entidades SQLModel para los datos scrapeados de books.toscrape.com."""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Categoria(SQLModel, table=True):
    """Categoria tematica de libros (ej. 'Nonfiction', 'Travel')."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False, index=True)

    libros: list["Libro"] = Relationship(back_populates="categoria")


class Libro(SQLModel, table=True):
    """Libro individual extraido del catalogo del sitio."""

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    precio: float = Field(nullable=False)
    valoracion: int = Field(nullable=False)
    disponible: bool = Field(nullable=False)
    url_detalle: Optional[str] = Field(default=None)

    categoria_id: Optional[int] = Field(
        default=None, foreign_key="categoria.id"
    )
    categoria: Optional[Categoria] = Relationship(back_populates="libros")