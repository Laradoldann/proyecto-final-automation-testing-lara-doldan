"""Carrito de compras: agregar, quitar y carrito vacío."""
import pytest

from pages.cart_page import CartPage

pytestmark = pytest.mark.ui

PRODUCTOS = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]


@pytest.mark.parametrize("producto", PRODUCTOS[:2])
def test_agregar_un_producto_al_carrito(pagina_inventario, driver, producto):
    pagina_inventario.agregar_producto(producto)

    pagina_inventario.esperar_cantidad_carrito(1)
    assert pagina_inventario.obtener_texto_boton(producto) == "Remove"

    pagina_inventario.ir_al_carrito()
    carrito = CartPage(driver)
    assert carrito.esta_cargada()
    assert carrito.obtener_nombres_productos() == [producto]


def test_agregar_varios_productos_al_carrito(pagina_inventario, driver):
    for producto in PRODUCTOS:
        pagina_inventario.agregar_producto(producto)

    pagina_inventario.esperar_cantidad_carrito(len(PRODUCTOS))
    pagina_inventario.ir_al_carrito()

    nombres_en_carrito = CartPage(driver).obtener_nombres_productos()
    assert sorted(nombres_en_carrito) == sorted(PRODUCTOS)


def test_quitar_un_producto_desde_el_carrito(pagina_inventario, driver):
    producto_a_quitar, producto_que_queda = PRODUCTOS[0], PRODUCTOS[1]
    pagina_inventario.agregar_producto(producto_a_quitar)
    pagina_inventario.agregar_producto(producto_que_queda)
    pagina_inventario.ir_al_carrito()

    carrito = CartPage(driver)
    carrito.quitar_producto(producto_a_quitar)

    assert carrito.obtener_nombres_productos() == [producto_que_queda]


def test_carrito_sin_productos_esta_vacio(pagina_inventario, driver):
    pagina_inventario.ir_al_carrito()

    carrito = CartPage(driver)
    assert carrito.esta_cargada()
    assert carrito.obtener_nombres_productos() == []
    assert pagina_inventario.obtener_cantidad_carrito() == 0
