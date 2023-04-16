from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional
# https://docs.pydantic.dev/usage/types/


from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

# Once user successfully created an account, this is part 
# of the package we can send back
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


#what we want from a user before we approve a login
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):    
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    published:bool
    created_at: datetime
    owner_id:int
    owner: UserOut

    # tells pydantic to ignore that data returned 
    # is not starting as a dictionary but an ORM model
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


# For token the user will send us when tryignt o log in
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)