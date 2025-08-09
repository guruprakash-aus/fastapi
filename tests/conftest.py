from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.db import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)
# Base = declarative_base()

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def session():
    """Fixture to provide a database session for tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    


@pytest.fixture()
def client(session):
    """Fixture to provide a test client for FastAPI."""
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    """Fixture to create a test user."""
    print("Creating a test user")
    user_data = {
        "email": "guru@gmail.com",
        "password": "password123"
    }
    response = client.post(
        "/users/", json=user_data
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 201
    new_user = response.json()
    assert new_user['email'] == user_data["email"]
    new_user['password'] = user_data["password"]  # Add password for login
    return new_user


@pytest.fixture
def token(test_user):
    """Fixture to create a JWT token for the test user."""
    print("Creating a JWT token for the test user")
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    """Fixture to provide an authorized client with a JWT token."""
    print("Creating an authorized client with a JWT token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def test_posts(test_user, session):
    """Fixture to create test posts."""
    print("Creating test posts")
    post_data = [
        {"title": "Post 1", "content": "Content 1", "published": True, "owner_id": test_user['id']},
        {"title": "Post 2", "content": "Content 2", "published": False, "owner_id": test_user['id']},
        {"title": "Post 3", "content": "Content 3", "published": True, "owner_id": test_user['id']},
    ]

    def create_post_model(post_data):
        """Helper function to create post models."""
        return models.Post(**post_data)

    post_map = map(create_post_model, post_data)
    post_data = list(post_map)


    # for post in post_data:
    #     new_post = models.Post(**post)
    #     session.add(new_post)

    session.add_all(post_data)
    session.commit()
    returned_posts = session.query(models.Post).all()
    print("Test posts created successfully")
    return returned_posts