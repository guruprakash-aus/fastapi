from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from typing import Optional

from random import randrange

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
    # return {"message": "SQLAlchemy is working!"}


# @router.get("/", response_model=list[schemas.PostResponse])
@router.get("/", response_model=list[schemas.PostVote])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    # Filter posts by the current user
    # This assumes that the Post model has an owner_id field that references the User model
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # If no posts are found, raise a 404 error
    # This is a good practice to ensure that the API returns meaningful responses
    # if not posts:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No posts found",
    #     )

    # No filter is applied, so it returns all posts
    # posts = db.query(models.Post).all()

    # posts = db.query(models.Post).limit(limit).all()
    # posts = db.query(models.Post).offset(skip).limit(limit).all()

    # Search functionality to filter posts by title or content
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search) | models.Post.content.contains(search)
    # ).limit(limit).offset(skip).all()

    # If the search query is empty, return all posts
    # if not search:
    #     posts = db.query(models.Post).limit(limit).offset(skip).all()

    # If the search query is not empty, return filtered posts
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search) | models.Post.content.contains(search)
    # ).limit(limit).offset(skip).all()

    # Get all the posts with votes
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(
            models.Post.title.contains(search) | models.Post.content.contains(search)
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    # If no posts are found, raise a 404 error
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )
    # return {"message": "Posts retrieved successfully", "data": posts}
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # print(current_user.id)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(
        owner_id=current_user.id,  # Associate the post with the current user
        **post.dict(),
    )  # Unpack the Post model to create a new Post instance
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create post",
        )
    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_userid: int = Depends(oauth2.get_current_user),
):
    """Retrieve a post by its ID.
    Returns an error message if the post is not found.
    """

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    
    # Check if the current user is the owner of the post
    if post.Post.owner_id != current_userid.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this post",
        )
    
    # If the post is found, return it
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Delete a post by its ID.
    Returns an error message if the post is not found.
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    # Check if the current user is the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )
    # Delete the post
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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

    # Check if the current user is the owner of the post
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )
    # Update the post with the new values
    for key, value in post.dict(exclude_unset=True).items():
        setattr(existing_post, key, value)
    db.commit()
    db.refresh(existing_post)
    return existing_post
