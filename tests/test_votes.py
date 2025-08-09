from app import schemas, models
import pytest
import json


@pytest.fixture
def test_vote(test_posts, session, test_user):
    """Fixture to create a test vote."""
    print("Creating a test vote")
    vote_data = {
        "post_id": test_posts[0].id,
        "user_id": test_user['id']
    }
    new_vote = models.Vote(**vote_data)
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    """Test voting on a post."""
    print("Testing voting on a post")
    response = authorized_client.post(
        f"/vote", json={"post_id": test_posts[2].id, "dir": 1}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    """Test voting twice on the same post."""
    print("Testing voting twice on the same post")
    response = authorized_client.post(
        f"/vote", json={"post_id": test_posts[0].id, "dir": 1}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 409
    assert response.json().get("detail") == "User has already voted on this post"

def test_vote_on_non_existent_post(authorized_client):
    """Test voting on a non-existent post."""
    print("Testing voting on a non-existent post")
    response = authorized_client.post(
        f"/vote", json={"post_id": 9999, "dir": 1}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 404
    assert response.json().get("detail") == "Post with id: 9999 does not exist"

def test_delete_vote(authorized_client, test_posts, test_vote):
    """Test deleting a vote."""
    print("Testing deleting a vote")
    response = authorized_client.request(
        "DELETE",
        "/vote",
        data=json.dumps({"post_id": test_posts[0].id, "dir": 1}),
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 204

def test_delete_non_existent_vote(authorized_client, test_posts):
    """Test deleting a non-existent vote."""
    print("Testing deleting a non-existent vote")
    response = authorized_client.request(
        "DELETE",
        "/vote",
        data=json.dumps({"post_id": test_posts[0].id, "dir": 1}),
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 404
    assert response.json().get("detail") == "Vote does not exist"

def test_vote_post_non_existent_post(authorized_client):
    """Test voting on a non-existent post."""
    print("Testing voting on a non-existent post")
    response = authorized_client.post(
        f"/vote", json={"post_id": 9999, "dir": 1}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 404
    assert response.json().get("detail") == "Post with id: 9999 does not exist"

def test_vote_unauthorized_user(client, test_posts):
    """Test voting with an unauthorized user."""
    print("Testing voting with an unauthorized user")
    response = client.post(
        f"/vote", json={"post_id": test_posts[0].id, "dir": 1}
    )
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"