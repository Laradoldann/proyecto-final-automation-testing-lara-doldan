"""Configuración compartida de pytest: navegador, log de cada test y capturas de pantalla en fallos."""
import logging

import pytest
import pytest_html
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from utils.screenshots import guardar_captura

logger = logging.getLogger(__name__)

# Donde el fixture driver deja el navegador para que el hook de capturas lo encuentre
CLAVE_NAVEGADOR = pytest.StashKey()


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Ejecuta Chrome sin abrir la ventana",
    )


def pytest_html_report_title(report):
    report.title = "Reporte de pruebas - Proyecto final Automation Testing"


@pytest.fixture
def driver(request):
    """Un Chrome nuevo por test, así ningún test depende de otro."""
    opciones = Options()
    opciones.add_argument("--window-size=1920,1080")
    if request.config.getoption("--headless"):
        opciones.add_argument("--headless=new")
    # Evita los avisos de Chrome sobre contraseñas
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])

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
    """Registra el resultado y, si falla el test o su preparación (setup), guarda y adjunta una captura."""
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
        return  # test de API o fallo antes de abrir el navegador

    try:
        imagen_base64 = guardar_captura(navegador, item.name, reporte.when)
    except (WebDriverException, OSError):
        logger.exception("No se pudo guardar la captura de %s", item.nodeid)
        return

    extras = getattr(reporte, "extras", [])
    extras.append(pytest_html.extras.image(imagen_base64))
    reporte.extras = extras
