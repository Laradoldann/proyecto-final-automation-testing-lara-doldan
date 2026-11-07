"""Página de detalle de un producto de SauceDemo."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    FRAGMENTO_URL = "/inventory-item.html"

    NOMBRE = (By.CSS_SELECTOR, ".inventory_details_name")
    PRECIO = (By.CSS_SELECTOR, ".inventory_details_price")
    BOTON_VOLVER = (By.ID, "back-to-products")

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def obtener_nombre(self):
        return self.obtener_texto(self.NOMBRE)

    def obtener_precio(self):
        return self.obtener_texto(self.PRECIO)

    def volver_a_productos(self):
        self.hacer_clic(self.BOTON_VOLVER)
