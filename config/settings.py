"""Configuración central. Cada valor se puede cambiar con una variable de entorno."""
import os
from pathlib import Path

# ---------- Rutas ----------
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = RAIZ_PROYECTO / "data"
CARPETA_REPORTES = RAIZ_PROYECTO / "reports"
CARPETA_CAPTURAS = CARPETA_REPORTES / "screenshots"

# ---------- UI: SauceDemo ----------
URL_BASE = os.getenv("BASE_URL", "https://www.saucedemo.com/")
TIMEOUT_UI = int(os.getenv("UI_TIMEOUT", "10"))  # segundos de las esperas explícitas

# Usuario de demo que SauceDemo publica en su página de login
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"

# Producto que usan los tests que necesitan algo en el carrito
PRODUCTO_DE_PRUEBA = "Sauce Labs Backpack"

# ---------- API: JSONPlaceholder ----------
URL_API = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT_API = int(os.getenv("API_TIMEOUT", "10"))
