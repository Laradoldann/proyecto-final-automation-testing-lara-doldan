"""Clase base de todas las páginas: acciones comunes con esperas explícitas."""
import logging
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import TIMEOUT_UI

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT_UI)

    @property
    def url_actual(self):
        return self.driver.current_url

    # ---------- Navegación ----------
    def abrir(self, url):
        logger.info("Abriendo %s", url)
        self.driver.get(url)

    def esperar_url_contiene(self, fragmento):
        self.wait.until(
            EC.url_contains(fragmento),
            message=f"La URL no llegó a contener '{fragmento}'",
        )

    def esta_en(self, fragmento):
        """True si la URL contiene el fragmento antes de que venza el timeout."""
        try:
            self.esperar_url_contiene(fragmento)
            return True
        except TimeoutException:
            logger.warning("No se llegó a '%s'. URL actual: %s", fragmento, self.url_actual)
            return False

    # ---------- Esperas ----------
    def esperar_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"No se hizo visible el elemento {locator}",
        )

    def esperar_clickeable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"El elemento {locator} no se pudo clickear",
        )

    def esperar_cantidad_elementos(self, locator, cantidad):
        self.wait.until(
            lambda driver: len(driver.find_elements(*locator)) == cantidad,
            message=f"No se llegó a {cantidad} elemento(s) de {locator}",
        )

    def esta_visible(self, locator, timeout=TIMEOUT_UI):
        """True si el elemento se ve en pantalla dentro del timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ---------- Acciones ----------
    def hacer_clic(self, locator):
        logger.info("Clic en %s", locator)
        self.esperar_clickeable(locator).click()

    def escribir(self, locator, texto):
        # No se registra el texto para no dejar contraseñas en el log
        logger.info("Escribiendo en %s", locator)
        campo = self.esperar_visible(locator)
        campo.clear()
        campo.send_keys(texto)

    # ---------- Lectura ----------
    def obtener_texto(self, locator):
        return self.esperar_visible(locator).text

    def obtener_elementos(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"No se encontraron elementos {locator}",
        )

    # ---------- Productos (comunes al catálogo y al carrito) ----------
    @staticmethod
    def locator_nombre_producto(nombre):
        return (By.XPATH, f"//div[contains(@class,'inventory_item_name') and normalize-space()='{nombre}']")

    @classmethod
    def locator_boton_producto(cls, nombre, contenedor):
        """Botón (Add to cart / Remove) del producto dentro de su contenedor: 'inventory_item' o 'cart_item'."""
        xpath_nombre = cls.locator_nombre_producto(nombre)[1]
        return (
            By.XPATH,
            f"{xpath_nombre}/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' {contenedor} ')]//button",
        )

    @staticmethod
    def extraer_monto(texto):
        """Devuelve el número de un texto como 'Item total: $29.99' -> 29.99"""
        coincidencia = re.search(r"\$\s*([\d.]+)", texto)
        if coincidencia is None:
            raise ValueError(f"No se encontró un monto en el texto: '{texto}'")
        return float(coincidencia.group(1))
