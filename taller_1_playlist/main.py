from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import Cancion, CancionBase, crear_db_y_tablas, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield


app = FastAPI(
    title="Taller 1 - Mi Playlist",
    version="1.0.0",
    lifespan=lifespan,
)

session_dependency = Annotated[Session, Depends(get_session)]


@app.post("/canciones/", response_model=Cancion, status_code=status.HTTP_201_CREATED)
def create_cancion(datos: CancionBase, session: session_dependency):
    nueva = Cancion.model_validate(datos)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@app.get("/canciones/", response_model=list[Cancion])
def listar_canciones(session: session_dependency):
    return session.exec(select(Cancion)).all()


@app.get("/canciones/{cancion_id}", response_model=Cancion)
def obtener_cancion(cancion_id: int, session: session_dependency):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canción {cancion_id} no encontrada",
        )
    return cancion


@app.put("/canciones/{cancion_id}", response_model=Cancion)
def actualizar_cancion(
    cancion_id: int,
    datos: CancionBase,
    session: session_dependency,
):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canción {cancion_id} no encontrada",
        )

    cancion.titulo = datos.titulo
    cancion.artista = datos.artista
    cancion.genero = datos.genero
    cancion.duracion_segundos = datos.duracion_segundos
    cancion.favorita = datos.favorita

    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


@app.delete("/canciones/{cancion_id}", response_model=Cancion)
def eliminar_cancion(cancion_id: int, session: session_dependency):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canción {cancion_id} no encontrada",
        )

    datos = Cancion.model_validate(cancion)
    session.delete(cancion)
    session.commit()
    return datos
