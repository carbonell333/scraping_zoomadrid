import time
import csv
import os
import ntpath
import argparse
from urllib.parse import urljoin, urlparse

import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

URL = "https://www.zoomadrid.com/descubre-el-zoo/animales-y-continentes/animales"
RUTA_CSV = "animales_zoomadrid.csv"
CARPETA_IMAGENES = "imagenes"

# --- FUNCIONES ---

def rechazar_cookies(driver):
    """Rechaza las cookies en el banner si aparece."""
    try:
        btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        )
        driver.execute_script("arguments[0].click();", btn)
    except TimeoutException:
        pass

def pulsar_muestrame_mas(driver):
    """Pulsa 'Muéstrame más' para mostrar todas los botones 'Ver Detalles'."""
    while True:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class,'cmp-button__text') and normalize-space()='Muéstrame más']/ancestor::a[1]"
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1.0)
        except TimeoutException:
            break

def obtener_urls_detalles(driver):
    """Devuelve todos los urls de 'Ver Detalles' (sin duplicados)."""
    anchors = driver.find_elements(
        By.XPATH,
        "//span[contains(@class,'cmp-button__text') and normalize-space()='Ver Detalles']/ancestor::a[1][@href]"
    )
    hrefs = [a.get_attribute("href") for a in anchors if a.get_attribute("href")]
    vistos, salida = set(), []
    for h in hrefs:
        if h not in vistos:
            vistos.add(h); salida.append(h)
    return salida

def nombre_archivo_desde_url(u: str) -> str:
    """Devuelve el nombre de archivo a partir de la URL."""
    return ntpath.basename(urlparse(u).path) or "imagen.jpg"

def descargar_imagen(img_url: str, base_url: str, nombre_archivo: str, user_agent: str = "Mozilla/5.0") -> str:
    """Descarga la imagen en CARPETA_IMAGENES/ con nombre 'nombre_archivo'."""
    if not img_url:
        return ""
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    url_completa = urljoin(base_url, img_url)
    ruta = os.path.join(CARPETA_IMAGENES, nombre_archivo)
    try:
        r = requests.get(url_completa, timeout=15, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        with open(ruta, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return nombre_archivo
    except Exception:
        return ""

def obtener_texto(driver, xpath: str) -> str:
    elems = driver.find_elements(By.XPATH, xpath)
    return elems[0].text.strip() if elems else ""

def obtener_url_imagen(driver) -> str:
    """Intenta primero la imagen de la galería; si no, usa og:image."""
    elems = driver.find_elements(
        By.XPATH,
        "(//div[contains(@class,'attraction-image')]//img[contains(@class,'img-fluid')])[1]"
    )
    if elems:
        src = elems[0].get_attribute("src") or ""
        if src:
            return src
    og = driver.find_elements(By.CSS_SELECTOR, "meta[property='og:image'][content]")
    if og:
        return og[0].get_attribute("content") or ""
    return ""

def extraer_datos_ficha(driver):
    """Extrae datos de una ficha de animal (incluye image_url y estado de conservación)."""
    nombre      = obtener_texto(driver, "//h1[contains(@class,'attraction-title')]")
    cientifico  = obtener_texto(driver, "//span[normalize-space()='Nombre científico:']/following-sibling::span")
    clase       = obtener_texto(driver, "//span[normalize-space()='Clase:']/following-sibling::span")
    continente  = obtener_texto(driver, "//span[normalize-space()='Continente:']/following-sibling::span")
    habitat     = obtener_texto(driver, "//span[normalize-space()='Hábitat:']/following-sibling::span")
    dieta       = obtener_texto(driver, "//span[normalize-space()='Dieta:']/following-sibling::span")
    peso        = obtener_texto(driver, "//span[normalize-space()='Peso:']/following-sibling::span")
    tamano      = obtener_texto(driver, "//span[normalize-space()='Tamaño:']/following-sibling::span")

    estado = ""
    for css in [
        "div.tag1[style*='background-color'] .tagElement",
        "div.tag1[class*='color#'] .tagElement",
        "div.tag1.active .tagElement, div.tag1.selected .tagElement",
    ]:
        elems = driver.find_elements(By.CSS_SELECTOR, css)
        if elems:
            txt = elems[0].text.strip()
            if txt:
                estado = txt
                break

    image_url = obtener_url_imagen(driver)

    return {
        "nombre": nombre,
        "nombre_cientifico": cientifico,
        "clase": clase,
        "continente": continente,
        "habitat": habitat,
        "dieta": dieta,
        "peso": peso,
        "tamano": tamano,
        "estado_conservacion": estado,
        "image_url": image_url,
        "url": driver.current_url,
    }

# --- CHROME/FIREFOX ---

def crear_driver(browser: str = "chrome"):
    browser = (browser or "chrome").lower()
    if browser == "firefox":
        options = FirefoxOptions()
        # options.add_argument("-headless")  # si quieres headless
        options.set_preference("dom.webdriver.enabled", True)
        options.page_load_strategy = "eager"
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    else:
        # Chrome por defecto
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1440,900")
        # options.add_argument("--headless=new")  # si quieres headless en Chrome
        options.page_load_strategy = "eager"
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--browser", choices=["chrome", "firefox"], default="firefox", help="Navegador a usar")
    return p.parse_args()

# --- MAIN()---

def main():
    args = parse_args()
    driver = crear_driver(args.browser)
    driver.get(URL)

    # User agent real del navegador (se reutiliza en requests)
    user_agent = driver.execute_script("return navigator.userAgent")

    rechazar_cookies(driver)
    pulsar_muestrame_mas(driver)

    urls = obtener_urls_detalles(driver)
    print(f"🔗 Se encontraron {len(urls)} animales.")

    resultados = []

    for i, url in enumerate(urls [:3], 1):
        driver.get(url)
        time.sleep(0.8)

        datos = extraer_datos_ficha(driver)

        base = nombre_archivo_desde_url(datos["image_url"]) or f"imagen_{i:03d}.jpg"
        nombre_fichero = f"{i:03d}-{base}"
        guardado = descargar_imagen(datos["image_url"], base_url=url, nombre_archivo=nombre_fichero, user_agent=user_agent)
        datos["image_file"] = guardado

        resultados.append(datos)
        print(f"[{i}/{len(urls)}] {datos['nombre']} -> img: {guardado}")

    if resultados:
        with open(RUTA_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        print(f"Guardado en {RUTA_CSV}")
        print(f"Imágenes en ./{CARPETA_IMAGENES}")

    driver.quit()

if __name__ == "__main__":
    main()