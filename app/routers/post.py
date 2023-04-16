from fastapi import Response, status, HTTPException,Depends,APIRouter
from .. import models, schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags = ['posts'])


# Get one post regardless of who created it
@router.get("/{id}", response_model=schemas.PostOut)
#id:int - helps with validating input
def get_post(id:int, db: Session = Depends(get_db)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,
        isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found" )

    return post 

# Get one post(but only provide that which has been created by the user)
# @router.get("/{id}")
# #id:int - helps with validating input
# def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
#     post = db.query(models.Post).filter(
#         models.Post.id == id).first()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} was not found" )
    
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail=f"Not Authorized to perform requested action")
#     return post 



# # Get all posts
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit:int = 10,
              offset:int = 0,
              search:Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,
        isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(
        limit).offset(offset).all()    
    
    return posts    


# posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(
    #     limit).offset(offset).all()
    
    #Uee join to discover number of votes on a post


    # print(results)
    
    # return posts

# # # Get all posts (for a specific user that's logged in)
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(
#         models.Post.owner_id == current_user.id).all()
#     return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#Below, accept the Pydantic basemodel of post
# user_id: int = Depends(oauth2.get_current_user - saying function is a dependency, forcing users to be logged in before they can create a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id,
                **post.dict())
        #The above replaces the below
        # title=post.title, content=post.content, published=post.published )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorized to perform requested action")

    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Update a Post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorized to perform requested action")
        
    post_query.update(updated_post.dict(),synchronize_session=False) 
    
    db.commit()

    return post_query.first()