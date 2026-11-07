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
    BOTON_SEGUIR_COMPRANDO = (By.ID, "continue-shopping")

    @staticmethod
    def _boton_quitar(nombre):
        return (
            By.XPATH,
            f"//div[contains(@class,'inventory_item_name') and normalize-space()='{nombre}']"
            "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' cart_item ')]//button",
        )

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def obtener_nombres_productos(self):
        """Nombres de los productos del carrito (lista vacía si no hay ninguno)."""
        self.esperar_visible(self.TITULO)
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRES)]

    def quitar_producto(self, nombre):
        logger.info("Quitando del carrito: %s", nombre)
        cantidad_inicial = self.contar_elementos(self.ITEMS)
        self.hacer_clic(self._boton_quitar(nombre))
        self.esperar_cantidad_elementos(self.ITEMS, cantidad_inicial - 1)

    def iniciar_checkout(self):
        self.hacer_clic(self.BOTON_CHECKOUT)

    def seguir_comprando(self):
        self.hacer_clic(self.BOTON_SEGUIR_COMPRANDO)
