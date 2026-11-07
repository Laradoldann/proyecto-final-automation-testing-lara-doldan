"""Cliente de la API pública JSONPlaceholder.

Los tests no arman las peticiones a mano: usan estos métodos, y acá queda
centralizado el registro en el log de cada petición y su respuesta.
"""
import logging

import requests

from config.settings import TIMEOUT_API, URL_API

logger = logging.getLogger(__name__)


class JsonPlaceholderClient:
    def __init__(self, url_base=URL_API, timeout=TIMEOUT_API):
        self.url_base = url_base.rstrip("/")
        self.timeout = timeout
        self.sesion = requests.Session()
        # Algunos servicios rechazan el User-Agent por defecto de requests
        self.sesion.headers.update({
            "Accept": "application/json",
            "User-Agent": "automation-testing-framework/1.0",
        })

    def cerrar(self):
        self.sesion.close()

    def _enviar(self, metodo, ruta, **kwargs):
        url = f"{self.url_base}{ruta}"
        logger.info("Petición %s %s", metodo, url)
        try:
            respuesta = self.sesion.request(metodo, url, timeout=self.timeout, **kwargs)
        except requests.RequestException:
            logger.exception("No se pudo completar %s %s", metodo, url)
            raise
        milisegundos = respuesta.elapsed.total_seconds() * 1000
        logger.info("Respuesta %s en %.0f ms", respuesta.status_code, milisegundos)
        logger.debug("Cuerpo de la respuesta: %s", respuesta.text[:500])
        return respuesta

    # ---------- Posts ----------
    def listar_posts(self, **filtros):
        """GET /posts. Los filtros se envían como query string (ej: userId=1)."""
        return self._enviar("GET", "/posts", params=filtros or None)

    def obtener_post(self, id_post):
        return self._enviar("GET", f"/posts/{id_post}")

    def crear_post(self, datos):
        return self._enviar("POST", "/posts", json=datos)

    def eliminar_post(self, id_post):
        return self._enviar("DELETE", f"/posts/{id_post}")

    def obtener_comentarios_de_post(self, id_post):
        return self._enviar("GET", f"/posts/{id_post}/comments")

    # ---------- Usuarios ----------
    def obtener_usuario(self, id_usuario):
        return self._enviar("GET", f"/users/{id_usuario}")
