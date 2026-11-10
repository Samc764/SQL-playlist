from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

DATA_BASE_URL = "sqlite:///playlist.db"
connect_args = {"check_same_thread": False}

engine = create_engine(DATA_BASE_URL, connect_args=connect_args, echo=False)


class ArtistaBase(SQLModel):
    nombre: str = Field(index=True, unique=True)
    pais: str | None = None


class Artista(ArtistaBase, table=True):
    __tablename__: str = "artistas"
    id: int | None = Field(default=None, primary_key=True)
    canciones: list["Cancion"] = Relationship(back_populates="artista")


class CancionBase(SQLModel):
    titulo: str = Field(index=True)
    genero: str | None = Field(default=None, index=True)
    duracion_segundos: int = Field(gt=0)
    favorita: bool = Field(default=False)
    artista_id: int = Field(foreign_key="artistas.id", index=True)


class Cancion(CancionBase, table=True):
    __tablename__: str = "canciones"
    id: int | None = Field(default=None, primary_key=True)
    artista: Artista | None = Relationship(back_populates="canciones")


class CancionPublica(CancionBase):
    id: int


class ArtistaPublico(ArtistaBase):
    id: int


class ArtistaConCanciones(ArtistaPublico):
    canciones: list[CancionPublica] = []


class CancionConArtista(CancionPublica):
    artista: ArtistaPublico | None = None


Artista.model_rebuild()
Cancion.model_rebuild()


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)


crear_db_y_tablas()


def get_session():
    with Session(engine) as session:
        yield session
