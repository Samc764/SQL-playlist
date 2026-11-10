from sqlmodel import Field, Session, SQLModel, create_engine

DATA_BASE_URL = "sqlite:///playlist.db"
connect_args = {"check_same_thread": False}

engine = create_engine(DATA_BASE_URL, connect_args=connect_args, echo=False)


class CancionBase(SQLModel):
    titulo: str = Field(index=True)
    artista: str = Field(index=True)
    genero: str | None = Field(default=None, index=True)
    duracion_segundos: int = Field(gt=0)
    favorita: bool = Field(default=False)


class Cancion(CancionBase, table=True):
    __tablename__: str = "canciones"
    id: int | None = Field(default=None, primary_key=True)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)


crear_db_y_tablas()


def get_session():
    with Session(engine) as session:
        yield session
