"""Página de login de SauceDemo."""
import logging

from selenium.webdriver.common.by import By

from config.settings import TIMEOUT_UI, URL_BASE
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def abrir_pagina(self):
        self.abrir(URL_BASE)
        self.esperar_visible(self.BOTON_LOGIN)

    def iniciar_sesion(self, usuario, password):
        logger.info("Iniciando sesión con el usuario '%s'", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_PASSWORD, password)
        self.hacer_clic(self.BOTON_LOGIN)

    def obtener_mensaje_error(self):
        return self.obtener_texto(self.MENSAJE_ERROR)

    def esta_cargada(self):
        """True si se ve el formulario de login."""
        return self.esta_visible(self.BOTON_LOGIN, timeout=TIMEOUT_UI)
