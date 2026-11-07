"""Capturas de pantalla de las pruebas de UI que fallan."""
import base64
import logging
import re
from datetime import datetime

from config.settings import CARPETA_CAPTURAS

logger = logging.getLogger(__name__)


def armar_nombre_captura(nombre_test, fase):
    """Ej: 2026-11-07_15-30-45_test_login_con_datos_invalidos_usuario_vacio_call.png"""
    marca = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_limpio = re.sub(r"[^\w.-]+", "_", nombre_test).strip("_")
    return f"{marca}_{nombre_limpio}_{fase}.png"


def guardar_captura(navegador, nombre_test, fase):
    """Guarda la captura en reports/screenshots/ y la devuelve en base64 para el reporte."""
    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_CAPTURAS / armar_nombre_captura(nombre_test, fase)
    imagen_png = navegador.get_screenshot_as_png()
    ruta.write_bytes(imagen_png)
    logger.error("Captura guardada: %s", ruta)
    return base64.b64encode(imagen_png).decode("utf-8")
