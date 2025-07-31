import pytest, httpx, re
from .data import valid_user, bad_email, bad_password

@pytest.mark.asyncio
async def test_register_ok(test_client):
    resp: httpx.Response = await test_client.post("/register", json=valid_user)
    assert resp.status_code == 201
    body = resp.json()

    # required fields
    for k in ("id", "created", "modified", "last_login", "token", "isactive"):
        assert k in body
    assert len(body["token"].split(".")) == 3
    # password eco
    assert body["password"] == valid_user["password"]

@pytest.mark.asyncio
async def test_register_duplicate(test_client):
    await test_client.post("/register", json=valid_user)          
    resp = await test_client.post("/register", json=valid_user)   
    assert resp.status_code == 409
    assert resp.json() == {'detail': {'mensaje': 'Usuario ya registrado'}}

@pytest.mark.asyncio
async def test_register_bad_email(test_client):
    resp = await test_client.post("/register", json=bad_email)
    assert resp.status_code == 422
    assert "correo" in resp.json()["detail"]["mensaje"].lower()            

@pytest.mark.asyncio
async def test_register_bad_password(test_client):
    resp = await test_client.post("/register", json=bad_password)
    assert resp.status_code == 422
    assert "contraseña" in resp.json()["detail"]["mensaje"].lower()
