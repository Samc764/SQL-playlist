from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_relacion_artistas_y_canciones():
    response = client.post(
        "/artistas/",
        json={"nombre": "Shakira", "pais": "Colombia"},
    )
    assert response.status_code == 201, response.text
    artista = response.json()
    artista_id = artista["id"]
    assert artista["nombre"] == "Shakira"

    response = client.post(
        "/artistas/",
        json={"nombre": "Shakira", "pais": "Argentina"},
    )
    assert response.status_code == 409, response.text

    response = client.get(f"/artistas/{artista_id}")
    assert response.status_code == 200, response.text
    assert response.json()["canciones"] == []

    response = client.post(
        "/canciones/",
        json={
            "titulo": "Waka Waka",
            "genero": "Pop",
            "duracion_segundos": 210,
            "favorita": False,
            "artista_id": 999,
        },
    )
    assert response.status_code == 404, response.text

    response = client.post(
        "/canciones/",
        json={
            "titulo": "Waka Waka",
            "genero": "Pop",
            "duracion_segundos": 210,
            "favorita": False,
            "artista_id": artista_id,
        },
    )
    assert response.status_code == 201, response.text
    cancion = response.json()
    cancion_id = cancion["id"]
    assert cancion["artista_id"] == artista_id

    response = client.get(f"/artistas/{artista_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["canciones"]) == 1
    assert data["canciones"][0]["titulo"] == "Waka Waka"

    response = client.get(f"/canciones/{cancion_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["artista"]["nombre"] == "Shakira"

    response = client.get("/canciones/?artista_id=1")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1

    response = client.delete(f"/artistas/{artista_id}")
    assert response.status_code == 409, response.text

    response = client.delete(f"/canciones/{cancion_id}")
    assert response.status_code == 200, response.text

    response = client.delete(f"/artistas/{artista_id}")
    assert response.status_code == 200, response.text

    response = client.get(f"/artistas/{artista_id}")
    assert response.status_code == 404, response.text
