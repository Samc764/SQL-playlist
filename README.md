# API de artistas y canciones

API REST con FastAPI + SQLModel para gestionar artistas y canciones con una base de datos SQLite.

## Requisitos

- Python 3.10+
- pip

## Instalar y ejecutar

```bash
cd /workspaces/SQL-playlist
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

Abre la documentación interactiva:

- http://127.0.0.1:8000/docs

## Endpoints

### Artistas

- POST /artistas/
- GET /artistas/
- GET /artistas/{artista_id}
- PUT /artistas/{artista_id}
- DELETE /artistas/{artista_id}

### Canciones

- POST /canciones/
- GET /canciones/
- GET /canciones/{cancion_id}
- PUT /canciones/{cancion_id}
- DELETE /canciones/{cancion_id}

## Modelo principal

```python
class Artista(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    nacionalidad: str | None = None

class Cancion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    duracion_segundos: int = Field(gt=0)
    genero: str | None = None
    favorita: bool = False
    artista_id: int = Field(foreign_key="artistas.id")
```

## Verificación

```bash
python -m pytest -q
```
