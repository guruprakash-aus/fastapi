from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel  # type: ignore
from random import randrange
import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host="localhost", port="5472", database="fastapi_postgres_db", user="fastapi_db", password="fastapi_db_password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed")
        print(f"Error: {e}")
        time.sleep(2)

@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create post"
        )
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    """Retrieve a post by its ID.
    Returns an error message if the post is not found.
    """
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    return {"post detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post by its ID.
    Returns an error message if the post is not found.
    """
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """Update a post by its ID.
    Returns an error message if the post is not found.
    """
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )   
    # return {"data": updated_post}
    return {"message": f"Post with id: {id} updated successfully", "updated_post": updated_post}