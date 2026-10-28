from collections.abc import Generator
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings


class Base(DeclarativeBase):
    pass


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_engine(database_url: str | None = None):
    url = database_url or get_settings().database_url
    connect_args = {}
    engine_kwargs = {}

    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        if ":memory:" in url or url == "sqlite://":
            engine_kwargs["poolclass"] = StaticPool

    return create_engine(url, connect_args=connect_args, **engine_kwargs)


def get_session_factory(engine=None):
    target_engine = engine or get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=target_engine)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
