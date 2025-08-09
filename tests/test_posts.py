from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    """Test getting all posts."""
    print("Testing getting all posts")
    response = authorized_client.get("/posts/")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    # assert isinstance(response.json(), list)
    assert len(response.json()) == len(test_posts)

    def validate_post(post):
        """Helper function to validate post schema."""
        # Unpack the nested 'Post' dict and add 'votes'
        return schemas.PostResponse(**post['Post'], votes=post['votes'])

    posts_map = map(validate_post, response.json())
    posts = list(posts_map)
    print("Posts:", posts)
    assert isinstance(posts, list)

    for post in posts:
        assert post.id is not None
        assert post.title is not None
        assert post.content is not None
        assert post.created_at is not None
        assert post.owner_id is not None
        assert post.owner.email is not None

def test_unauthorized_user_get_all_posts(client):
    """Test getting all posts without authorization."""
    print("Testing unauthorized user getting all posts")
    response = client.get("/posts/")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not authenticated'


def test_unauthorized_user_get_post(client, test_posts):
    """Test getting a post without authorization."""
    print("Testing unauthorized user getting a post")
    response = client.get(f"/posts/{test_posts[0].id}")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not authenticated'

def test_get_one_post_not_found(authorized_client, test_posts):
    """Test getting a post that does not exist."""
    print("Testing getting a post that does not exist")
    response = authorized_client.get("/posts/999999")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json().get('detail') == 'Post with id: 999999 not found'

def test_get_one_post(authorized_client, test_posts):
    """Test getting a specific post."""
    print("Testing getting a specific post")
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200

    retrieved_post = schemas.PostResponse(**response.json()['Post'])  # Validate response schema
    # retrieved_post = post['Post']
    assert retrieved_post.id == test_posts[0].id
    assert retrieved_post.title == test_posts[0].title
    assert retrieved_post.content == test_posts[0].content
    assert retrieved_post.created_at is not None
    assert retrieved_post.owner_id == test_posts[0].owner_id
    assert retrieved_post.owner.email == test_posts[0].owner.email


@pytest.mark.parametrize("title, content, published, rating, status_code", [
    ("New Post", "This is a new post", True, 5, 201),
    ("Another Post", "Content for another post", False, None, 201),
    ("", "Content without title", True, 3, 422),  # Invalid
    ("Valid Post", "", True, 4, 422),  # Invalid
    ("Post with None rating", "Content with None rating", True, None, 201),
    ("Post with negative rating", "Content with negative rating", True, -1, 422)  # Invalid
])
def test_create_post(authorized_client, test_user, title, content, published, rating, status_code):
    """Test creating a new post."""
    print("Testing creating a new post")
    post_data = {
        "title": title,
        "content": content,
        "published": published,
        "rating": rating
    }
    response = authorized_client.post("/posts/", json=post_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == status_code
    if status_code == 201:
        new_post = schemas.PostResponse(**response.json())  # Validate response schema
        assert new_post.title == title
        assert new_post.content == content
        assert new_post.published == published
        assert new_post.rating == rating
        assert new_post.owner_id == test_user['id']
        assert new_post.owner.email == test_user['email']
    elif status_code == 422:
        detail = response.json().get('detail')
        if isinstance(detail, str):
            assert detail == "Title and content are required"
        else:
            assert detail[0].get('msg') == 'field required' or \
                detail[0].get('msg') == 'Input should be a valid integer' or \
                detail[0].get('msg') == 'Input should be greater than or equal to 0'
            
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    """Test creating a post with default published value as True."""
    print("Testing creating a post with default published value as True")
    post_data = {
        "title": "Post with default published",
        "content": "Content for post with default published"
    }
    response = authorized_client.post("/posts/", json=post_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 201
    new_post = schemas.PostResponse(**response.json())  # Validate response schema
    assert new_post.title == post_data['title']
    assert new_post.content == post_data['content']
    assert new_post.published is True  # Default should be True
    assert new_post.owner_id == test_user['id']
    assert new_post.owner.email == test_user['email']

def test_unauthorized_user_create_post(client):
    """Test creating a post without authorization."""
    print("Testing unauthorized user creating a post")
    post_data = {
        "title": "Unauthorized Post",
        "content": "Content for unauthorized post"
    }
    response = client.post("/posts/", json=post_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not authenticated'

def test_unauthorized_delete_post(client, test_posts):
    """Test deleting a post without authorization."""
    print("Testing unauthorized user deleting a post")
    response = client.delete(f"/posts/{test_posts[0].id}")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not authenticated'

def test_delete_post(authorized_client, test_posts):
    """Test deleting a post."""
    print("Testing deleting a post")
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    print("Response status code:", response.status_code)
    # print("Response JSON:", response.json())
    
    assert response.status_code == 204  # No content on successful deletion

    # Verify the post is deleted
    get_response = authorized_client.get(f"/posts/{test_posts[0].id}")
    print("Get response status code:", get_response.status_code)
    assert get_response.status_code == 404
    assert get_response.json().get('detail') == f"Post with id: {test_posts[0].id} not found"

def test_delete_non_existent_post(authorized_client):
    """Test deleting a post that does not exist."""
    print("Testing deleting a post that does not exist")
    response = authorized_client.delete("/posts/999999")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json().get('detail') == 'Post with id: 999999 not found'

def test_update_post(authorized_client, test_posts):
    """Test updating a post."""
    print("Testing updating a post")
    post_id = test_posts[0].id
    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": False,
        "rating": 4
    }
    response = authorized_client.put(f"/posts/{post_id}", json=update_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    
    assert response.status_code == 200
    updated_post = schemas.PostResponse(**response.json())  # Validate response schema
    assert updated_post.id == post_id
    assert updated_post.title == update_data['title']
    assert updated_post.content == update_data['content']
    assert updated_post.published == update_data['published']
    assert updated_post.rating == update_data['rating']
    assert updated_post.owner_id == test_posts[0].owner_id
    assert updated_post.owner.email == test_posts[0].owner.email

def test_update_post_not_found(authorized_client):
    """Test updating a post that does not exist."""
    print("Testing updating a post that does not exist")
    response = authorized_client.put("/posts/999999", json={"title": "New Title"})
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json().get('detail') == 'Post with id: 999999 not found'

def test_update_post_not_owner(authorized_client, test_posts, test_user):
    """Test updating a post that the user does not own."""
    print("Testing updating a post that the user does not own")
    unauthorized_user = {
        "email": "unauthorized@example.com",
        "password": "password"
    }
    response = authorized_client.put("/posts/999999", json={"title": "New Title"})
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json().get('detail') == 'Post with id: 999999 not found'

    # Create a new user and try to update the post
    new_user_response = authorized_client.post("/users/", json=unauthorized_user)
    print("New user response status code:", new_user_response.status_code)
    assert new_user_response.status_code == 201
    new_user = schemas.UserResponse(**new_user_response.json())
    print("New User Response headers: ",new_user_response.headers)
    print("New user created:", new_user)
    # After creating the user
    login_data = {
        "username": unauthorized_user["email"],
        "password": unauthorized_user["password"]
    }
    login_response = authorized_client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    unauthorized_client = authorized_client
    unauthorized_client.headers.update({"Authorization": f"Bearer {access_token}"})
    # unauthorized_client.headers.update({"Authorization": f"Bearer {new_user_response.json()['access_token']}"})
    response = unauthorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "Unauthorized Update"})
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 403
    assert response.json().get('detail') == 'Not authorized to update this post'

