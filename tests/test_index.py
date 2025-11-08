from fastapi import status


def test_server_up(client):
    res = client.get("/breathing")
    assert res.status_code == status.HTTP_200_OK
    body = res.json()
    assert "message" in body
    assert "OK" in body["message"]
