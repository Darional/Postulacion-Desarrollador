import pytest_asyncio, mongomock_motor
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest_asyncio.fixture(scope="session")
async def test_client():

    # Created a Mock of mongoDB
    fake_client = mongomock_motor.AsyncMongoMockClient()
    fake_db = fake_client["usersdb"]
    fake_collection = fake_db["users"]
    fake_collection.create_index("email", unique=True)

    import importlib
    main_mod = importlib.import_module("app.main")
    main_mod.client = fake_client
    main_mod.db = fake_db
    main_mod.users_collection = fake_collection

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
