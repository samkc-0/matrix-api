import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from app.main import app


@pytest.fixture(scope="session", name="client")
def client():
    with TestClient(app) as client:
        yield client
