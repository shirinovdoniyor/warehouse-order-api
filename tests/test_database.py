from collections.abc import Generator
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import Base, get_db, get_engine, get_session_factory


class DummyItem(Base):
    __tablename__ = "dummy_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


def test_settings_defaults_and_env_override(monkeypatch):
    default_settings = Settings()
    assert "postgresql" in default_settings.database_url
    assert default_settings.environment == "development"

    monkeypatch.setenv("DATABASE_URL", "sqlite:///./env_test.db")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    get_settings.cache_clear()
    custom_settings = get_settings()
    assert custom_settings.database_url == "sqlite:///./env_test.db"
    assert custom_settings.environment == "testing"
    get_settings.cache_clear()


def test_engine_creation_sqlite_memory():
    engine = get_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        result = conn.exec_driver_sql("SELECT 1").scalar()
        assert result == 1


def test_crud_and_state_change_with_isolated_sqlite():
    test_engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    session_factory = get_session_factory(test_engine)

    with session_factory() as session:
        item = DummyItem(name="First Item")
        session.add(item)
        session.commit()
        session.refresh(item)
        item_id = item.id
        assert item_id is not None

    with session_factory() as session:
        stored = session.scalar(select(DummyItem).where(DummyItem.id == item_id))
        assert stored is not None
        assert stored.name == "First Item"

    with session_factory() as session:
        item2 = DummyItem(name="Temporary Item")
        session.add(item2)
        session.flush()
        session.rollback()

    with session_factory() as session:
        items = session.scalars(select(DummyItem)).all()
        assert len(items) == 1
        assert items[0].name == "First Item"

    Base.metadata.drop_all(bind=test_engine)


def test_get_db_generator_lifecycle():
    gen: Generator[Session, None, None] = get_db()
    session = next(gen)
    assert isinstance(session, Session)
    with pytest.raises(StopIteration):
        next(gen)


def test_fastapi_dependency_override_with_sqlite():
    test_engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    test_session_factory = get_session_factory(test_engine)

    test_app = FastAPI()

    def override_get_db():
        session = test_session_factory()
        try:
            yield session
        finally:
            session.close()

    @test_app.post("/items")
    def create_item(name: str, db: Session = Depends(override_get_db)):
        if not name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        item = DummyItem(name=name)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"id": item.id, "name": item.name}

    client = TestClient(test_app)

    resp = client.post("/items?name=Box")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "name": "Box"}

    bad_resp = client.post("/items?name= ")
    assert bad_resp.status_code == 400
    assert bad_resp.json()["detail"] == "Name cannot be empty"

    Base.metadata.drop_all(bind=test_engine)
