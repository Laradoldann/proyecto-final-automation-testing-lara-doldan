"""Flujos donde una petición usa el resultado de la anterior."""
import pytest

pytestmark = pytest.mark.api


def test_post_usuario_y_comentarios_son_consistentes(cliente_api):
    # 1) Se obtiene un post y de ahí se toma el id de su autor
    respuesta_post = cliente_api.obtener_post(1)
    assert respuesta_post.status_code == 200
    post = respuesta_post.json()

    # 2) Con ese userId se consulta al usuario
    respuesta_usuario = cliente_api.obtener_usuario(post["userId"])
    assert respuesta_usuario.status_code == 200
    usuario = respuesta_usuario.json()
    assert usuario["id"] == post["userId"]
    assert "@" in usuario["email"]

    # 3) Con el id del post se consultan sus comentarios
    respuesta_comentarios = cliente_api.obtener_comentarios_de_post(post["id"])
    assert respuesta_comentarios.status_code == 200
    comentarios = respuesta_comentarios.json()
    assert len(comentarios) > 0
    assert all(comentario["postId"] == post["id"] for comentario in comentarios)


def test_post_creado_no_se_puede_consultar_porque_la_api_no_lo_guarda(cliente_api):
    # 1) Se crea un post y se toma el id que devuelve la API
    respuesta_creacion = cliente_api.crear_post(
        {"userId": 1, "title": "Post temporal", "body": "No debería persistir"}
    )
    assert respuesta_creacion.status_code == 201
    id_creado = respuesta_creacion.json()["id"]

    # 2) Se intenta leer con ese id: JSONPlaceholder solo simula la escritura
    respuesta_consulta = cliente_api.obtener_post(id_creado)
    assert respuesta_consulta.status_code == 404
