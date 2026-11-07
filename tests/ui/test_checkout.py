"""Proceso de compra completo: datos del cliente, resumen y confirmación."""
import pytest

from config.settings import PRODUCTO_DE_PRUEBA
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletoPage,
    CheckoutInformacionPage,
    CheckoutResumenPage,
)
from pages.inventory_page import InventoryPage
from utils.data_reader import como_parametros, leer_json

pytestmark = pytest.mark.ui

DATOS_CHECKOUT = leer_json("checkout.json")
COMPRAS_EXITOSAS = como_parametros(DATOS_CHECKOUT["compra_exitosa"])
DATOS_INVALIDOS = como_parametros(DATOS_CHECKOUT["datos_invalidos"])

MENSAJE_DE_COMPRA_EXITOSA = "Thank you for your order!"


@pytest.mark.parametrize("cliente", COMPRAS_EXITOSAS)
def test_compra_completa(pagina_checkout, driver, cliente):
    pagina_checkout.completar_formulario(
        cliente["nombre"], cliente["apellido"], cliente["codigo_postal"]
    )
    pagina_checkout.continuar()

    resumen = CheckoutResumenPage(driver)
    assert resumen.esta_cargada(), f"No se llegó al resumen. URL actual: {resumen.url_actual}"
    assert resumen.obtener_nombres_productos() == [PRODUCTO_DE_PRUEBA]
    resumen.finalizar_compra()

    confirmacion = CheckoutCompletoPage(driver)
    assert confirmacion.esta_cargada(), f"No se llegó a la confirmación. URL actual: {confirmacion.url_actual}"
    assert confirmacion.obtener_mensaje_confirmacion() == MENSAJE_DE_COMPRA_EXITOSA

    confirmacion.volver_a_productos()
    inventario = InventoryPage(driver)
    assert inventario.esta_cargada()
    assert inventario.obtener_cantidad_carrito() == 0, "El carrito debería quedar vacío después de comprar"


@pytest.mark.parametrize("cliente", DATOS_INVALIDOS)
def test_checkout_con_datos_incompletos(pagina_checkout, cliente):
    pagina_checkout.completar_formulario(
        cliente["nombre"], cliente["apellido"], cliente["codigo_postal"]
    )
    pagina_checkout.continuar()

    mensaje = pagina_checkout.obtener_mensaje_error()
    assert cliente["mensaje_error"] in mensaje, f"Mensaje inesperado: '{mensaje}'"
    assert "/checkout-step-one.html" in pagina_checkout.url_actual, "No debería avanzar al resumen"


def test_resumen_calcula_bien_subtotal_y_total(pagina_inventario, driver):
    productos = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]
    for producto in productos:
        pagina_inventario.agregar_producto(producto)
    pagina_inventario.ir_al_carrito()
    CartPage(driver).iniciar_checkout()

    informacion = CheckoutInformacionPage(driver)
    informacion.completar_formulario("Ana", "Perez", "1425")
    informacion.continuar()

    resumen = CheckoutResumenPage(driver)
    assert resumen.esta_cargada()
    assert sorted(resumen.obtener_nombres_productos()) == sorted(productos)

    subtotal = resumen.obtener_subtotal()
    assert subtotal == pytest.approx(sum(resumen.obtener_precios_productos()))
    assert resumen.obtener_total() == pytest.approx(subtotal + resumen.obtener_impuesto())


def test_cancelar_checkout_vuelve_al_carrito(pagina_checkout, driver):
    pagina_checkout.cancelar()

    carrito = CartPage(driver)
    assert carrito.esta_cargada(), f"No se volvió al carrito. URL actual: {carrito.url_actual}"
    assert carrito.obtener_nombres_productos() == [PRODUCTO_DE_PRUEBA]
