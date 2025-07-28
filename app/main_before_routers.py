from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .db import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5472",
            database="fastapi_postgres_db",
            user="fastapi_db",
            password="fastapi_db_password",
            cursor_factory=RealDictCursor,
        )
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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
    # return {"message": "SQLAlchemy is working!"}


@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )
    # return {"message": "Posts retrieved successfully", "data": posts}
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # Unpack the Post model to create a new Post instance
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create post",
        )
    return new_post

    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # if not new_post:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create post"
    #     )
    # return {"data": new_post}


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    """Retrieve a post by its ID.
    Returns an error message if the post is not found.
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return post



    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    # print(post)
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} not found",
    #     )
    # return {"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """Delete a post by its ID.
    Returns an error message if the post is not found.
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    db.delete(post)
    db.commit()



    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if not deleted_post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} not found",
    #     )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """Update a post by its ID.
    Returns an error message if the post is not found.
    """
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    # Update the existing post with only teh fields that are provided in the request
    # This allows partial updates
    # Use the PostUpdate schema to ensure only valid fields are updated

    for key, value in post.dict(exclude_unset=True).items():
        setattr(existing_post, key, value)
    db.commit()
    db.refresh(existing_post)
    return existing_post

    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if not updated_post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} not found",
    #     )
    # return {"data": updated_post}
    # return {
    #     "message": f"Post with id: {id} updated successfully",
    #     "updated_post": updated_post,
    # }

# User Routes

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Hash the password before storing it
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    # Create a new User instance and add it to the database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    """Retrieve a user by their ID."""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    return user