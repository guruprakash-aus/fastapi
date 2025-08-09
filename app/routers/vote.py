from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, db, models, oauth2
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db_session: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    print(f"Current user: {current_user.id}, Vote: {vote}")
    
    # Check if the post exists
    post = db_session.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist",
        )
    
    
    # Check if the user has already voted on this post
    existing_vote = db_session.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    ).first()
    print(f"Existing vote: {existing_vote}")

    if vote.dir == 1:
        # User is trying to upvote
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted on this post",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db_session.add(new_vote)
        db_session.commit()
        return {"message": "Vote added successfully"}
    else:
        # User is trying to downvote
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )
        db_session.delete(existing_vote)
        db_session.commit()
        return {"message": "Vote removed successfully"}
    
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(
    vote: schemas.Vote,
    db_session: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    print(f"Current user: {current_user.id}, Vote to delete: {vote}")
    
    # Check if the user has voted on this post
    existing_vote = db_session.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    ).first()
    
    if not existing_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote does not exist",
        )
    
    db_session.delete(existing_vote)
    db_session.commit()
    print("Vote deleted successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)