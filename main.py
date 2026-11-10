from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import (
    Artista,
    ArtistaBase,
    ArtistaConCanciones,
    Cancion,
    CancionBase,
    CancionConArtista,
    crear_db_y_tablas,
    get_session,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield


crear_db_y_tablas()


app = FastAPI(
    title="Artistas y Canciones",
    version="1.0.0",
    lifespan=lifespan,
)

session_dependency = Annotated[Session, Depends(get_session)]


@app.post("/artistas/", response_model=Artista, status_code=status.HTTP_201_CREATED)
def create_artista(artista: ArtistaBase, session: session_dependency):
    existe = session.exec(select(Artista).where(Artista.nombre == artista.nombre)).first()
    if existe is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un artista con ese nombre",
        )

    nuevo_artista = Artista.model_validate(artista)
    session.add(nuevo_artista)
    session.commit()
    session.refresh(nuevo_artista)
    return nuevo_artista


@app.get("/artistas/", response_model=list[Artista])
def listar_artistas(session: session_dependency):
    return session.exec(select(Artista)).all()


@app.get("/artistas/{artista_id}", response_model=ArtistaConCanciones)
def obtener_artista(artista_id: int, session: session_dependency):
    artista = session.get(Artista, artista_id)
    if artista is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El artista {artista_id} no existe",
        )
    return artista


@app.delete("/artistas/{artista_id}", response_model=Artista)
def eliminar_artista(artista_id: int, session: session_dependency):
    artista = session.get(Artista, artista_id)
    if artista is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El artista {artista_id} no existe",
        )
    if artista.canciones:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un artista que tenga canciones",
        )

    datos = Artista.model_validate(artista)
    session.delete(artista)
    session.commit()
    return datos


@app.post("/canciones/", response_model=Cancion, status_code=status.HTTP_201_CREATED)
def create_cancion(datos: CancionBase, session: session_dependency):
    artista = session.get(Artista, datos.artista_id)
    if artista is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El artista {datos.artista_id} no existe",
        )

    nueva_cancion = Cancion.model_validate(datos)
    session.add(nueva_cancion)
    session.commit()
    session.refresh(nueva_cancion)
    return nueva_cancion


@app.get("/canciones/", response_model=list[Cancion])
def listar_canciones(artista_id: int | None = None, session: session_dependency = None):
    consulta = select(Cancion)
    if artista_id is not None:
        consulta = consulta.where(Cancion.artista_id == artista_id)
    return session.exec(consulta).all()


@app.get("/canciones/{cancion_id}", response_model=CancionConArtista)
def obtener_cancion(cancion_id: int, session: session_dependency):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La canción {cancion_id} no existe",
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
            detail=f"La canción {cancion_id} no existe",
        )

    artista = session.get(Artista, datos.artista_id)
    if artista is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El artista {datos.artista_id} no existe",
        )

    cancion.titulo = datos.titulo
    cancion.genero = datos.genero
    cancion.duracion_segundos = datos.duracion_segundos
    cancion.favorita = datos.favorita
    cancion.artista_id = datos.artista_id

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
            detail=f"La canción {cancion_id} no existe",
        )

    datos = Cancion.model_validate(cancion)
    session.delete(cancion)
    session.commit()
    return datos
