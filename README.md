# EC3 — Web Scraping con Selenium y SQLModel

Proyecto de la asignatura **Programación Científica**

Scrapea el catálogo de libros de [books.toscrape.com](https://books.toscrape.com) usando **Selenium WebDriver** y persiste los datos en una base de datos relacional con **SQLModel** + SQLite.

## Integrantes

- José Acuña
- Ronaldo Morales

## Requisitos

- Python 3.11+
- Google Chrome instalado
- Entorno virtual (conda o venv)

## Instalación

```bash
conda create -n EC3 python=3.11
conda activate EC3
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Esto:
1. Crea la base de datos `data.db` y sus tablas
2. Abre Chrome por debajo, navega desde el home de books.toscrape.com hasta la categoría "Nonfiction", y recorre la paginación extrayendo al menos 50 libros
3. Persiste los libros en la base de datos 
4. Ejecuta las 4 consultas de verificación y muestra los resultados en consola

## Estructura

| Archivo | Descripción |
|---|---|
| `models.py` | Entidades SQLModel (`Categoria`, `Libro`) |
| `database.py` | Engine, creación de tablas y `get_session()` |
| `scraper.py` | Lógica de Selenium: navegación, paginación y extracción |
| `seed.py` | Llama al scraper y persiste los datos en la BD |
| `queries.py` | 4 consultas de verificación requeridas |
| `main.py` | Punto de entrada del proyecto |
| `requirements.txt` | Dependencias del proyecto |


