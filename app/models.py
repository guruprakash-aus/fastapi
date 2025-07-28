from .db import Base
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean, default=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default="now()", onupdate="now()"
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )  # Assuming a foreign key to a User table

    owner = relationship("User")  # Establishing a relationship with the User model


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default="now()", onupdate="now()"
    )


# Votes Model
class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
