from app import schemas
from .db import client, session
import pytest
from jose import jwt
from app.config import settings

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



def test_read_root(client):
    """Test the root endpoint."""
    print("Testing the root endpoint")
    response = client.get("/")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello World "}
    assert response.json().get("message") == "Hello World "


def test_create_user(client):
    """Test user creation."""
    print("Testing user creation")
    response = client.post(
        "/users/", json={"email": "sample@gmail.com", "password": "samplepassword"}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    # assert response.json().get("email") == "sample@gmail.com"
    # assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())  # Validate response schema
    assert new_user.email == "sample@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    """Test user login."""
    print("Testing user login")
    response = client.post(
        "/auth/login/", data={"username": test_user['email'], "password": test_user['password']}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    login_response = schemas.Token(**response.json())  # Validate response schema
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    # assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"