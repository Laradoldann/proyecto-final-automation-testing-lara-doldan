"""Fixtures de las pruebas de UI. El navegador ('driver') viene del conftest.py de la raíz."""
import pytest

from config.settings import PASSWORD_VALIDO, PRODUCTO_DE_PRUEBA, USUARIO_VALIDO
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInformacionPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def pagina_login(driver):
    """Página de login ya abierta."""
    pagina = LoginPage(driver)
    pagina.abrir_pagina()
    return pagina


@pytest.fixture
def pagina_inventario(pagina_login, driver):
    """Sesión iniciada con el usuario válido y el catálogo de productos cargado."""
    pagina_login.iniciar_sesion(USUARIO_VALIDO, PASSWORD_VALIDO)
    inventario = InventoryPage(driver)
    assert inventario.esta_cargada(), "No se pudo iniciar sesión para preparar el test"
    return inventario


@pytest.fixture
def pagina_checkout(pagina_inventario, driver):
    """Un producto en el carrito y el formulario de datos del checkout abierto."""
    pagina_inventario.agregar_producto(PRODUCTO_DE_PRUEBA)
    pagina_inventario.ir_al_carrito()
    CartPage(driver).iniciar_checkout()
    pagina = CheckoutInformacionPage(driver)
    assert pagina.esta_cargada(), "No se pudo llegar al checkout para preparar el test"
    return pagina
