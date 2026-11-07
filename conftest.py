"""Configuración compartida de pytest para todo el proyecto.

Acá viven:
- la opción --headless y el fixture del navegador,
- el registro en el log del inicio y resultado de cada test,
- la captura de pantalla automática cuando algo falla (en el test o en su preparación).
"""
import logging

import pytest
import pytest_html
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from utils.screenshots import guardar_captura

logger = logging.getLogger(__name__)

# Clave con la que el fixture 'driver' deja el navegador a mano del hook de capturas
CLAVE_NAVEGADOR = pytest.StashKey()


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Ejecuta Chrome sin abrir la ventana (útil en CI o para ir más rápido)",
    )


def pytest_html_report_title(report):
    report.title = "Reporte de pruebas - Proyecto final Automation Testing"


@pytest.fixture
def driver(request):
    """Abre un Chrome nuevo para CADA test y lo cierra al terminar.

    Con un navegador nuevo por test, ningún test depende del estado de otro.
    """
    opciones = Options()
    opciones.add_argument("--window-size=1920,1080")
    if request.config.getoption("--headless"):
        opciones.add_argument("--headless=new")
    # Evita los avisos de Chrome sobre guardar o cambiar contraseñas
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Selenium Manager (incluido en Selenium 4) descarga el chromedriver que haga falta
    navegador = webdriver.Chrome(options=opciones)
    request.node.stash[CLAVE_NAVEGADOR] = navegador
    logger.info("Navegador iniciado")
    yield navegador
    navegador.quit()
    logger.info("Navegador cerrado")


@pytest.fixture(autouse=True)
def registrar_inicio_del_test(request):
    logger.info("===== INICIO: %s =====", request.node.nodeid)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Registra el resultado de cada test y, si falla, guarda y adjunta una captura.

    Se revisan las fases 'setup' y 'call': así también queda captura cuando falla
    la preparación del test (por ejemplo, un login que no funciona dentro de un fixture).
    """
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when == "call":
        logger.info("Resultado de %s: %s", item.nodeid, reporte.outcome.upper())

    if not reporte.failed or reporte.when not in ("setup", "call"):
        return

    detalle = " ".join(call.excinfo.exconly().split())[:500] if call.excinfo else "sin detalle"
    logger.error("Falló %s (fase %s): %s", item.nodeid, reporte.when, detalle)

    navegador = item.stash.get(CLAVE_NAVEGADOR, None)
    if navegador is None:
        return  # test de API o fallo antes de abrir el navegador: no hay nada que capturar

    try:
        _, imagen_base64 = guardar_captura(navegador, item.name, reporte.when)
    except (WebDriverException, OSError):
        logger.exception("No se pudo guardar la captura de %s", item.nodeid)
        return

    extras = getattr(reporte, "extras", [])
    extras.append(pytest_html.extras.image(imagen_base64))
    reporte.extras = extras
