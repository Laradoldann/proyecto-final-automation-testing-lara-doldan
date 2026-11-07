"""Página de productos (inventario) de SauceDemo."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config.settings import TIMEOUT_UI
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


def _xpath_nombre_producto(nombre):
    return f"//div[contains(@class,'inventory_item_name') and normalize-space()='{nombre}']"


class InventoryPage(BasePage):
    FRAGMENTO_URL = "/inventory.html"

    TITULO = (By.CSS_SELECTOR, ".title")
    NOMBRES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRECIOS = (By.CSS_SELECTOR, ".inventory_item_price")
    ORDEN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ICONO_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link")
    CONTADOR_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")
    MENU = (By.ID, "react-burger-menu-btn")
    ENLACE_LOGOUT = (By.ID, "logout_sidebar_link")

    # Cada botón (Add to cart / Remove) se busca a partir del nombre del producto
    @staticmethod
    def _boton_de_producto(nombre):
        return (
            By.XPATH,
            _xpath_nombre_producto(nombre)
            + "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' inventory_item ')]//button",
        )

    # ---------- Estado de la página ----------
    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL) and self.esta_visible(self.TITULO, timeout=TIMEOUT_UI)

    def obtener_titulo(self):
        return self.obtener_texto(self.TITULO)

    def obtener_nombres_productos(self):
        return [elemento.text for elemento in self.obtener_elementos(self.NOMBRES)]

    def obtener_precios_productos(self):
        return [self.extraer_monto(elemento.text) for elemento in self.obtener_elementos(self.PRECIOS)]

    def obtener_textos_de_precios(self):
        return [elemento.text for elemento in self.obtener_elementos(self.PRECIOS)]

    # ---------- Acciones sobre productos ----------
    def ordenar_por(self, valor):
        """Valores posibles: az, za, lohi, hilo."""
        logger.info("Ordenando productos por '%s'", valor)
        Select(self.esperar_visible(self.ORDEN)).select_by_value(valor)

    def agregar_producto(self, nombre):
        logger.info("Agregando al carrito: %s", nombre)
        self.hacer_clic(self._boton_de_producto(nombre))

    def quitar_producto(self, nombre):
        logger.info("Quitando del carrito: %s", nombre)
        self.hacer_clic(self._boton_de_producto(nombre))

    def obtener_texto_boton(self, nombre):
        return self.obtener_texto(self._boton_de_producto(nombre))

    def abrir_detalle_producto(self, nombre):
        logger.info("Abriendo el detalle de: %s", nombre)
        self.hacer_clic((By.XPATH, _xpath_nombre_producto(nombre)))

    # ---------- Carrito ----------
    def obtener_cantidad_carrito(self):
        """Número del globo rojo del carrito (0 si no se muestra)."""
        contador = self.driver.find_elements(*self.CONTADOR_CARRITO)
        return int(contador[0].text) if contador and contador[0].text else 0

    def esperar_cantidad_carrito(self, cantidad):
        self.wait.until(
            lambda driver: self.obtener_cantidad_carrito() == cantidad,
            message=f"El contador del carrito no llegó a {cantidad}",
        )

    def ir_al_carrito(self):
        self.hacer_clic(self.ICONO_CARRITO)

    # ---------- Menú ----------
    def cerrar_sesion(self):
        logger.info("Cerrando sesión")
        self.hacer_clic(self.MENU)
        self.hacer_clic(self.ENLACE_LOGOUT)
