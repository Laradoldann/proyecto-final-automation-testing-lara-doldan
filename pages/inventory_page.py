"""Página de productos (inventario) de SauceDemo."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config.settings import URL_BASE
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


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

    def abrir_directamente(self):
        """Abre la URL del catálogo sin pasar por el login."""
        self.abrir(URL_BASE.rstrip("/") + self.FRAGMENTO_URL)

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL) and self.esta_visible(self.TITULO)

    def obtener_titulo(self):
        return self.obtener_texto(self.TITULO)

    # ---------- Productos ----------
    def obtener_nombres_productos(self):
        return [elemento.text for elemento in self.obtener_elementos(self.NOMBRES)]

    def obtener_textos_de_precios(self):
        return [elemento.text for elemento in self.obtener_elementos(self.PRECIOS)]

    def obtener_precios_productos(self):
        return [self.extraer_monto(texto) for texto in self.obtener_textos_de_precios()]

    def ordenar_por(self, valor):
        """Valores posibles: az, za, lohi, hilo."""
        logger.info("Ordenando productos por '%s'", valor)
        Select(self.esperar_visible(self.ORDEN)).select_by_value(valor)

    def agregar_producto(self, nombre):
        logger.info("Agregando al carrito: %s", nombre)
        self.hacer_clic(self.locator_boton_producto(nombre, "inventory_item"))

    def obtener_texto_boton(self, nombre):
        return self.obtener_texto(self.locator_boton_producto(nombre, "inventory_item"))

    def abrir_detalle_producto(self, nombre):
        logger.info("Abriendo el detalle de: %s", nombre)
        self.hacer_clic(self.locator_nombre_producto(nombre))

    # ---------- Carrito y menú ----------
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

    def cerrar_sesion(self):
        logger.info("Cerrando sesión")
        self.hacer_clic(self.MENU)
        self.hacer_clic(self.ENLACE_LOGOUT)
