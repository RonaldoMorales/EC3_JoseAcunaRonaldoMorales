"""Scraper de libros desde books.toscrape.com."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_categoria(
    categoria_nombre: str = "Nonfiction",
    minimo_items: int = 50,
) -> list[dict]:
    """Navega desde el home hasta una categoria y extrae sus libros."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    books_data = []

    try:
        driver.get(BASE_URL)

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.side_categories")
            )
        )

        categoria_link = wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, categoria_nombre)
            )
        )
        categoria_link.click()

        while len(books_data) < minimo_items:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "article.product_pod")
                )
            )

            books = driver.find_elements(
                By.CSS_SELECTOR,
                "article.product_pod",
            )

            for book in books:
                try:
                    link = book.find_element(
                        By.CSS_SELECTOR,
                        "h3 > a",
                    )

                    titulo = link.get_attribute("title")

                    precio = book.find_element(
                        By.CSS_SELECTOR,
                        "p.price_color",
                    ).text

                    precio = precio.replace("£", "").strip()
                    precio = float(precio)

                    rating_class = book.find_element(
                        By.CSS_SELECTOR,
                        "p.star-rating",
                    ).get_attribute("class")

                    valoracion = 0
                    for palabra, valor in RATING_MAP.items():
                        if palabra in rating_class:
                            valoracion = valor
                            break

                    disponibilidad = book.find_element(
                        By.CSS_SELECTOR,
                        "p.instock.availability",
                    ).text

                    disponible = "In stock" in disponibilidad

                    url_detalle = link.get_attribute("href")

                    book_data = {
                        "titulo": titulo,
                        "precio": precio,
                        "valoracion": valoracion,
                        "disponible": disponible,
                        "categoria": categoria_nombre,
                        "url_detalle": url_detalle,
                    }

                    books_data.append(book_data)

                except Exception as e:
                    print(f"Error al procesar un libro: {e}")
                    continue

            try:
                siguiente = driver.find_element(
                    By.CSS_SELECTOR,
                    "li.next > a",
                )
            except Exception:
                print("No hay mas paginas, fin de la paginacion.")
                break

            siguiente.click()

    finally:
        driver.quit()

    return books_data