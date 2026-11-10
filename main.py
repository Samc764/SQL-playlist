from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import Cancion, CancionBase, crear_db_y_tablas, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield


crear_db_y_tablas()


app = FastAPI(
    title="Playlist API",
    version="1.0.0",
    lifespan=lifespan,
)

session_dependency = Annotated[Session, Depends(get_session)]


@app.post("/playlist/", response_model=Cancion, status_code=status.HTTP_201_CREATED)
@app.post("/canciones/", response_model=Cancion, status_code=status.HTTP_201_CREATED)
def create_cancion(cancion: CancionBase, session: session_dependency):
    nueva_cancion = Cancion.model_validate(cancion)
    session.add(nueva_cancion)
    session.commit()
    session.refresh(nueva_cancion)
    return nueva_cancion


@app.get("/playlist/", response_model=list[Cancion])
@app.get("/canciones/", response_model=list[Cancion])
def listar_canciones(session: session_dependency):
    consulta = select(Cancion)
    return session.exec(consulta).all()


@app.get("/playlist/{cancion_id}", response_model=Cancion)
@app.get("/canciones/{cancion_id}", response_model=Cancion)
def obtener_cancion(cancion_id: int, session: session_dependency):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canción no encontrada",
        )
    return cancion


@app.put("/playlist/{cancion_id}", response_model=Cancion)
@app.put("/canciones/{cancion_id}", response_model=Cancion)
def actualizar_cancion(
    cancion_id: int,
    cancion_actualizada: CancionBase,
    session: session_dependency,
):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canción no encontrada",
        )

    cancion.titulo = cancion_actualizada.titulo
    cancion.artista = cancion_actualizada.artista
    cancion.duracion_segundos = cancion_actualizada.duracion_segundos
    cancion.genero = cancion_actualizada.genero
    cancion.favorita = cancion_actualizada.favorita

    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


@app.delete("/playlist/{cancion_id}", response_model=Cancion)
@app.delete("/canciones/{cancion_id}", response_model=Cancion)
def eliminar_cancion(cancion_id: int, session: session_dependency):
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canción no encontrada",
        )

    datos = Cancion.model_validate(cancion)
    session.delete(cancion)
    session.commit()
    return datos
