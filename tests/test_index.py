import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from fastapi import status
from app.main import app



def test_server_up():
    with TestClient(app) as client:
        res = client.get("/breathing")
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert "message" in body
        assert "OK" in body["message"]
