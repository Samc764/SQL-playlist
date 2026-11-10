# Taller 1 - Mi Playlist

## Ejecutar

```bash
cd taller_1_playlist
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
fastapi dev main.py
```

Abre:

- http://127.0.0.1:8000/docs

## Endpoints

- POST /canciones/
- GET /canciones/
- GET /canciones/{cancion_id}
- PUT /canciones/{cancion_id}
- DELETE /canciones/{cancion_id}

## Modelo

```python
class CancionBase(SQLModel):
    titulo: str
    artista: str
    genero: str | None = None
    duracion_segundos: int = Field(gt=0)
    favorita: bool = False
```
