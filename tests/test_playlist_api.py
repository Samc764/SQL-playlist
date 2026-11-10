from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_playlist_crud():
    response = client.post(
        "/playlist/",
        json={
            "titulo": "Bohemian Rhapsody",
            "artista": "Queen",
            "duracion_segundos": 355,
            "genero": "Rock",
            "favorita": True,
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["titulo"] == "Bohemian Rhapsody"
    assert data["id"] == 1

    response = client.get("/playlist/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1

    response = client.put(
        "/playlist/1",
        json={
            "titulo": "Another One Bites the Dust",
            "artista": "Queen",
            "duracion_segundos": 354,
            "genero": "Rock",
            "favorita": False,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["titulo"] == "Another One Bites the Dust"

    response = client.delete("/playlist/1")
    assert response.status_code == 200, response.text
    assert response.json()["titulo"] == "Another One Bites the Dust"

    response = client.get("/playlist/")
    assert response.status_code == 200, response.text
    assert response.json() == []
