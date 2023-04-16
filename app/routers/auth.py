from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session



from ..database import get_db
from .. import schemas, models , utils, oauth2


router = APIRouter(
    tags = ['Authentication'])

# Design Route where users may log in
@router.post('/login', response_model=schemas.Token)
#T ell he system the structure of infomation it is accepting
# Connect to the database that has the information we need
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    # For the user_credentials, Auth2Pass.. will only return two things, username and password. Even if it collects email, the key will be called username
    # Try to get user by access the table where user information is stored, filter for the first row that matches the email sent by the user
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # Check to make sure the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    # Check to make sure we have been given tht corrrect pass word (this will create a new hash, based on whats given and compare to what's stored in our database)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    #create Token
    # Return Token

    #data here is the information we want to put int he payload
    # Here we are choosing to just encode the user_id
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}