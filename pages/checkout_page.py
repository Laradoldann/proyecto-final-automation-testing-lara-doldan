"""Páginas del proceso de compra de SauceDemo.

El checkout tiene tres pantallas distintas, así que hay una clase por cada una:
datos del cliente, resumen de la compra y confirmación.
"""
import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutInformacionPage(BasePage):
    FRAGMENTO_URL = "/checkout-step-one.html"

    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_CANCELAR = (By.ID, "cancel")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def completar_formulario(self, nombre, apellido, codigo_postal):
        logger.info("Completando datos del cliente (%s %s)", nombre, apellido)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)

    def continuar(self):
        self.hacer_clic(self.BOTON_CONTINUAR)

    def cancelar(self):
        self.hacer_clic(self.BOTON_CANCELAR)

    def obtener_mensaje_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)


class CheckoutResumenPage(BasePage):
    FRAGMENTO_URL = "/checkout-step-two.html"

    NOMBRES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    PRECIOS = (By.CSS_SELECTOR, ".cart_item .inventory_item_price")
    SUBTOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    IMPUESTO = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    BOTON_FINALIZAR = (By.ID, "finish")

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def obtener_nombres_productos(self):
        return [elemento.text for elemento in self.obtener_elementos(self.NOMBRES)]

    def obtener_precios_productos(self):
        return [self.extraer_monto(elemento.text) for elemento in self.obtener_elementos(self.PRECIOS)]

    def obtener_subtotal(self):
        return self.extraer_monto(self.obtener_texto(self.SUBTOTAL))

    def obtener_impuesto(self):
        return self.extraer_monto(self.obtener_texto(self.IMPUESTO))

    def obtener_total(self):
        return self.extraer_monto(self.obtener_texto(self.TOTAL))

    def finalizar_compra(self):
        logger.info("Finalizando la compra")
        self.hacer_clic(self.BOTON_FINALIZAR)


class CheckoutCompletoPage(BasePage):
    FRAGMENTO_URL = "/checkout-complete.html"

    MENSAJE_CONFIRMACION = (By.CSS_SELECTOR, ".complete-header")
    BOTON_VOLVER = (By.ID, "back-to-products")

    def esta_cargada(self):
        return self.esta_en(self.FRAGMENTO_URL)

    def obtener_mensaje_confirmacion(self):
        return self.obtener_texto(self.MENSAJE_CONFIRMACION)

    def volver_a_productos(self):
        self.hacer_clic(self.BOTON_VOLVER)
