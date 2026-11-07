"""Catálogo de productos: contenido, ordenamiento y navegación al detalle.

SauceDemo no tiene buscador, así que el filtrado del catálogo se prueba con el
selector de orden.
"""
import pytest

from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage

pytestmark = pytest.mark.ui

CANTIDAD_DE_PRODUCTOS = 6
PRODUCTO = "Sauce Labs Backpack"

# (valor del selector, atributo que se ordena, ¿de mayor a menor?)
CRITERIOS_DE_ORDEN = [
    pytest.param("az", "nombre", False, id="nombre_a_z"),
    pytest.param("za", "nombre", True, id="nombre_z_a"),
    pytest.param("lohi", "precio", False, id="precio_menor_a_mayor"),
    pytest.param("hilo", "precio", True, id="precio_mayor_a_menor"),
]


def test_catalogo_muestra_los_productos(inventory_page):
    nombres = inventory_page.obtener_nombres_productos()
    precios = inventory_page.obtener_textos_de_precios()

    assert inventory_page.obtener_titulo() == "Products"
    assert len(nombres) == CANTIDAD_DE_PRODUCTOS, f"Productos encontrados: {nombres}"
    assert all(nombre.strip() for nombre in nombres), "Hay productos sin nombre"
    assert all(precio.startswith("$") for precio in precios), f"Precios con formato inesperado: {precios}"


@pytest.mark.parametrize("valor_orden, atributo, descendente", CRITERIOS_DE_ORDEN)
def test_ordenar_productos(inventory_page, valor_orden, atributo, descendente):
    inventory_page.ordenar_por(valor_orden)

    if atributo == "nombre":
        valores = inventory_page.obtener_nombres_productos()
    else:
        valores = inventory_page.obtener_precios_productos()
    assert valores == sorted(valores, reverse=descendente), f"Orden incorrecto: {valores}"


def test_abrir_detalle_de_un_producto_y_volver(inventory_page, driver):
    precios_por_nombre = dict(zip(
        inventory_page.obtener_nombres_productos(),
        inventory_page.obtener_textos_de_precios(),
    ))

    inventory_page.abrir_detalle_producto(PRODUCTO)

    detalle = ProductDetailPage(driver)
    assert detalle.esta_cargada(), f"No se abrió el detalle. URL actual: {driver.current_url}"
    assert detalle.obtener_nombre() == PRODUCTO
    assert detalle.obtener_precio() == precios_por_nombre[PRODUCTO]

    detalle.volver_a_productos()
    assert InventoryPage(driver).esta_cargada(), "No se volvió al catálogo"
