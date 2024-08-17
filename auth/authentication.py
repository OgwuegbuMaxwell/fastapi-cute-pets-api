from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.hashing import Hash
from auth import oauth2

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)




@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    # username is the identifier of the logged-in user
    # 'sub' is a standard JWT claim for the subject of the token
    access_token = oauth2.create_access_token(data={'username': user.username})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
    