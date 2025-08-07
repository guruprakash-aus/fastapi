from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .db import engine
from .routers import posts, users, auth, vote
from .config import settings

# Create the database tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# CORS configuration
# origins = [
#     "http://localhost:3000",  # Adjust this to your frontend URL
#     "https://www.google.com",  # Example of another allowed origin
# ]

origins = ["*"]  # Allows all origins, adjust as needed

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

# Include routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Hello World "}
