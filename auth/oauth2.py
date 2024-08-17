###########################################################

from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from fastapi import Depends
from fastapi import HTTPException, status
import logging

from db import db_user
from db.database import get_db


SECRET_KEY = "Gp6t1mDoUD2MvUh17udplZcFI6V691hlYwFJ7f4A5Gk"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

'''
# Test the token creation
token = create_access_token({"sub": "user_id"})
print("JWT Token:", token)


'''


# get current user and verify token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # print(f"Token Received: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        # Decode the token using the SECRET_KEY and ALGORITHM specified
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        # print(f"This is username: {username}")
        if username is None:
            print("username is none")
            raise credentials_exception
    except JWTError as e:
        # Log the specific JWT error
        # print(f"JWT Error: {e}")
        # This block will execute if jwt.decode() raises JWTError, meaning the token is invalid
        raise credentials_exception

    # print("i got pass verifiction")
    # If no JWTError, fetch the user by username
    user = db_user.get_user_by_username(db, username)
    
    if user is None:
        # user is found in the database, raise an exception
        raise credentials_exception
    return user


