"""Fixtures de las pruebas de API."""
import pytest

from api.jsonplaceholder_client import JsonPlaceholderClient


@pytest.fixture
def cliente_api():
    """Cliente nuevo para cada test, así ninguno depende de otro."""
    cliente = JsonPlaceholderClient()
    yield cliente
    cliente.cerrar()
