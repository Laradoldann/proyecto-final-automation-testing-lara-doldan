"""Fixtures de las pruebas de API."""
import pytest

from api.jsonplaceholder_client import JsonPlaceholderClient


@pytest.fixture
def cliente_api():
    """Un cliente nuevo por test."""
    cliente = JsonPlaceholderClient()
    yield cliente
    cliente.cerrar()
