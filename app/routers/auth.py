from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    """Login endpoint for user authentication."""
    # This is a placeholder for the login logic
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    # If the user is found and the password is correct, return a success message
    
    # In a real application, you would also generate and return a JWT token here
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }