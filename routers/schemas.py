from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    username : str
    email : str
    password : str
    
# we return this user details to the user
class UserDisplay(BaseModel):
    username: str
    email: str
    class ConfigDict:
        from_attributes = True
 
class PostBase(BaseModel):
    image_url: str
    # Relative or absolute
    # if we get an image from the internet, we will save all of the url
    image_url_type: str
    caption: str
    creator_id: str



# for post display
# only for the post display
class User(BaseModel):
    username: str
    class ConfigDict:
        from_attributes = True

# Comment for Post display
class Comment(BaseModel):
    id:int
    post_id: int
    text: str
    username: str
    timestamp: datetime
    class ConfigDict:
        from_attributes = True

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    # creator_id: str
    timestamp: datetime
    user: User
    comments: List[Comment]
    class ConfigDict:
        from_attributes = True
    

class UserAuth(BaseModel):
    id: int
    username: str
    email: str



class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int


