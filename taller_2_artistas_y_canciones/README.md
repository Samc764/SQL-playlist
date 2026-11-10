# Taller 2 - Artistas y Canciones

## Ejecutar

```bash
cd taller_2_artistas_y_canciones
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
fastapi dev main.py
```

Abre:

- http://127.0.0.1:8000/docs

## Endpoints

### Artistas

- POST /artistas/
- GET /artistas/
- GET /artistas/{artista_id}
- DELETE /artistas/{artista_id}

### Canciones

- POST /canciones/
- GET /canciones/
- GET /canciones/{cancion_id}
- PUT /canciones/{cancion_id}
- DELETE /canciones/{cancion_id}

## Relación

- Un artista tiene muchas canciones
- Cada canción pertenece a un artista mediante `artista_id`

```python
class Artista(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    canciones: list["Cancion"] = Relationship(back_populates="artista")

class Cancion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    artista_id: int = Field(foreign_key="artistas.id")
    artista: Artista | None = Relationship(back_populates="canciones")
```
