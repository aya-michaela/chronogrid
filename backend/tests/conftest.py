import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./test_chronogrid.db"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from fastapi.testclient import TestClient
from database import Base, engine
import main


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    main.init_db()
    with TestClient(main.app) as c:
        yield c


@pytest.fixture()
def token(client):
    r = client.post("/auth/login", json={"email": "aya@canalplus.ci", "password": "aya123"})
    return r.json()["access_token"]


@pytest.fixture()
def auth(token):
    return {"Authorization": f"Bearer {token}"}
