from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings





# # Responsible for creating tables, everytime server runs
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    #function that runs before every request
    CORSMiddleware,
    # Specify domains that can talk to our API
    allow_origins=origins,
    #
    allow_credentials=True,
    # permission for specific HTTP methods (PUT, GET etc)
    allow_methods=["*"],
    #
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!!!"}








    
