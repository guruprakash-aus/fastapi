from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_read_root(client):
#     """Test the root endpoint."""
#     print("Testing the root endpoint")
#     response = client.get("/")
#     print("Response status code:", response.status_code)
#     print("Response JSON:", response.json())
#     assert response.status_code == 200
#     # assert response.json() == {"message": "Hello World "}
#     assert response.json().get("message") == "Hello World "


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

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 404),
    ('guru@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 404),
    (None, 'password123', 404),
    ('guru@gmail.com', None, 403),
    (None, None, 404)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    print("Testing incorrect login with email:", email, "and password:", password)
    res = client.post(
        "/auth/login/", data={"username": email, "password": password}
    )
    assert res.status_code == status_code

