from fastapi import FastAPI
from . import models
from .db import engine
from .routers import posts, users, auth, vote
from .config import settings

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}
