import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from Backend.main import app
from Backend.database import Base
from Backend.dependencies import get_db
from Backend import models
from Backend.hashing import Hash
from Backend import models, oauth2

# Test database
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

@pytest.fixture
def auth_headers(client, db):
    user = models.User(
        name="Test User",
        email="test@example.com",
        password="test"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    app.dependency_overrides[oauth2.get_current_user] = lambda: user

    return {"Authorization": "Bearer test-token"}