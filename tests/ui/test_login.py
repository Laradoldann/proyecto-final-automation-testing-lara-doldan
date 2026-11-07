"""Login y cierre de sesión en SauceDemo (escenarios positivos y negativos)."""
import pytest

from config.settings import URL_BASE
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_reader import como_parametros, leer_csv

pytestmark = pytest.mark.ui

DATOS_LOGIN = leer_csv("login.csv")
CASOS_EXITO = como_parametros([c for c in DATOS_LOGIN if c["resultado"] == "exito"])
CASOS_ERROR = como_parametros([c for c in DATOS_LOGIN if c["resultado"] == "error"])


@pytest.mark.parametrize("caso", CASOS_EXITO)
def test_login_exitoso(login_page, driver, caso):
    login_page.iniciar_sesion(caso["usuario"], caso["password"])

    inventario = InventoryPage(driver)
    assert inventario.esta_cargada(), f"No se llegó al catálogo. URL actual: {driver.current_url}"
    assert inventario.obtener_titulo() == "Products"


@pytest.mark.parametrize("caso", CASOS_ERROR)
def test_login_con_datos_invalidos(login_page, driver, caso):
    login_page.iniciar_sesion(caso["usuario"], caso["password"])

    mensaje = login_page.obtener_mensaje_error()
    assert caso["mensaje_error"] in mensaje, f"Mensaje inesperado: '{mensaje}'"
    assert "/inventory.html" not in driver.current_url, "El login no debería haber avanzado al catálogo"


def test_acceso_directo_al_catalogo_sin_iniciar_sesion(login_page, driver):
    driver.get(URL_BASE + "inventory.html")

    mensaje = login_page.obtener_mensaje_error()
    assert "when you are logged in" in mensaje, f"Mensaje inesperado: '{mensaje}'"


def test_cerrar_sesion(inventory_page, driver):
    inventory_page.cerrar_sesion()

    assert LoginPage(driver).esta_cargada(), "Después de cerrar sesión debería verse el login"
    assert "/inventory.html" not in driver.current_url
