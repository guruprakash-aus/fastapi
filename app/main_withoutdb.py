from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel  # type: ignore
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Title of Post 1", "content": "content of post 1", "id": 1},
    {"title": "Favourite Foods", "content": "I like Pizza", "id": 2},
]

def find_post(id):
    """
    Find and return a post by its id from my_posts.
    Returns None if not found.
    """
    return next((p for p in my_posts if p["id"] == id), None)

@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']} content: {payload['content']}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post)
    print(post.dict())

    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    """Retrieve a post by its ID.
    Returns an error message if the post is not found.
    """
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} not found"}  
    return {"post detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post by its ID.
    Returns an error message if the post is not found.
    """
    global my_posts
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    my_posts = [p for p in my_posts if p["id"] != id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """Update a post by its ID.
    Returns an error message if the post is not found.
    """
    post_index = next((index for index, p in enumerate(my_posts) if p["id"] == id), None)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    my_posts[post_index] = post.dict()
    my_posts[post_index]["id"] = id
    return {"data": my_posts[post_index]}