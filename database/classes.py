## Classes which should be used by SQLAlchemy to create
## database tables, and functions to initialize the database connection.

from sqlalchemy import String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
import globals

engine = None
SessionLocal = None

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    passwordhash: Mapped[str] = mapped_column(String, nullable=False)

def init():
    global engine, SessionLocal

    DB_FILE = globals.DB_FILE_NAME
    engine = create_engine(
        f"sqlite:///{DB_FILE}",
        echo=False,
        future=True
    )

    SessionLocal = sessionmaker(bind=engine, future=True)

    Base.metadata.create_all(engine)

    return SessionLocal
