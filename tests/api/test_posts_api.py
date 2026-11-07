"""Endpoints /posts de JSONPlaceholder: GET, POST y DELETE.

La API simula las escrituras sin guardarlas, así que POST y DELETE se validan por su respuesta.
"""
import pytest

from utils.data_reader import como_parametros, leer_json

pytestmark = pytest.mark.api

CAMPOS_DE_UN_POST = {"userId": int, "id": int, "title": str, "body": str}
POSTS_NUEVOS = como_parametros(leer_json("posts_api.json")["posts_nuevos"])


def validar_estructura_de_post(post):
    assert isinstance(post, dict), f"Se esperaba un objeto JSON y llegó: {post}"
    for campo, tipo in CAMPOS_DE_UN_POST.items():
        assert campo in post, f"Falta el campo '{campo}' en {post}"
        assert isinstance(post[campo], tipo), f"'{campo}' debería ser {tipo.__name__}: {post[campo]!r}"


# ---------- GET ----------
def test_listar_todos_los_posts(cliente_api):
    respuesta = cliente_api.listar_posts()

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert len(posts) == 100
    for post in posts:
        validar_estructura_de_post(post)


@pytest.mark.parametrize("id_post", [1, 50, 100])
def test_obtener_un_post_existente(cliente_api, id_post):
    respuesta = cliente_api.obtener_post(id_post)

    assert respuesta.status_code == 200
    assert "application/json" in respuesta.headers["Content-Type"]
    post = respuesta.json()
    validar_estructura_de_post(post)
    assert post["id"] == id_post


@pytest.mark.parametrize("id_post", [0, 9999])
def test_obtener_un_post_inexistente_devuelve_404(cliente_api, id_post):
    respuesta = cliente_api.obtener_post(id_post)

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


@pytest.mark.parametrize("id_usuario, cantidad_esperada", [(1, 10), (5, 10), (999, 0)])
def test_filtrar_posts_por_usuario(cliente_api, id_usuario, cantidad_esperada):
    respuesta = cliente_api.listar_posts(userId=id_usuario)

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert len(posts) == cantidad_esperada
    assert all(post["userId"] == id_usuario for post in posts)


# ---------- POST ----------
@pytest.mark.parametrize("caso", POSTS_NUEVOS)
def test_crear_un_post(cliente_api, caso):
    datos = caso["datos"]

    respuesta = cliente_api.crear_post(datos)

    assert respuesta.status_code == 201
    creado = respuesta.json()
    assert creado["title"] == datos["title"]
    assert creado["body"] == datos["body"]
    assert creado["userId"] == datos["userId"]
    assert creado["id"] == 101, "JSONPlaceholder asigna siempre el id 101 al recurso simulado"


# ---------- DELETE ----------
def test_eliminar_un_post(cliente_api):
    respuesta = cliente_api.eliminar_post(1)

    assert respuesta.status_code == 200
    assert respuesta.json() == {}
