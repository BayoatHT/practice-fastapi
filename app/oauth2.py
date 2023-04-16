from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings


#Pass in the url path of the user log in page
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


#SECRET_KEY (random example)
# Provide Algorithm
# Establish expiration time of the token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# pass payload in as "data"
def create_access_token(data: dict):
    # copy data so we don't change the original
    to_encode =data.copy()
    # Create the expiration field (Provide time it will expire from)
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token:str, credentials_exception):

    try:
        #Algorithm in brackets because it my expect list of algorithms 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # This payload is coming from the accesstoken generated from auth.py (right before the retuen)
        # from the login function
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        #Checks to make sure token data matches our schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    


def get_current_user(token:str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):

    #HTTP exception that should be raised if aomthing goes wrong
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user