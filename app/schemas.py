from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, conint
from datetime import datetime
from pydantic.types import conint

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int  # Assuming a foreign key to a User table
    owner: UserResponse # Include owner details in the response
    model_config = ConfigDict(from_attributes=True) # Enable attribute access for the model

class PostVote(BaseModel):
    Post: PostResponse
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # 0 for downvote, 1 for upvote