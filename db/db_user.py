from db.models import DbUser
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from fastapi.exceptions import HTTPException
from fastapi import status


def create_user(db:Session, request:UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        # we will eed to hash the password
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    # refresh retrieve all the information from the database
    db.refresh(new_user)
    return new_user


# Get  user by username
def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        # Raise an HTTPException with status code 404 and a detail message
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with username {username} not found'
        )
    return user