"""Página del carrito de SauceDemo."""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    FRAGMENTO_URL = "/cart.html"

    TITULO = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    NOMBRES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def obtener_nombres_productos(self):
        """Nombres de los productos del carrito (lista vacía si no hay ninguno)."""
        self.esperar_visible(self.TITULO)
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRES)]

    def quitar_producto(self, nombre):
        logger.info("Quitando del carrito: %s", nombre)
        cantidad_inicial = len(self.obtener_elementos(self.ITEMS))
        self.hacer_clic(self.locator_boton_producto(nombre, "cart_item"))
        self.esperar_cantidad_elementos(self.ITEMS, cantidad_inicial - 1)

    def iniciar_checkout(self):
        self.hacer_clic(self.BOTON_CHECKOUT)
