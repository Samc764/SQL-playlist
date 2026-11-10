# SQL Playlist API

API REST para gestionar una playlist con FastAPI + SQLModel + SQLite.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la API

```bash
fastapi dev main.py
```

o:

```bash
python -m fastapi dev main.py
```

Abre la documentación interactiva en:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Endpoints

- POST /playlist/
- GET /playlist/
- GET /playlist/{id}
- PUT /playlist/{id}
- DELETE /playlist/{id}

También están disponibles las rutas equivalentes en /canciones/.

## Modelo

```python
class CancionBase(SQLModel):
    titulo: str
    artista: str
    duracion_segundos: int | None = None
    genero: str | None = None
    favorita: bool = False
```

## Verificación

```bash
python -m pytest -q
```
