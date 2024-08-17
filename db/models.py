from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbPost', back_populates='user')


class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
    comments = relationship("DbComment", back_populates="post")
    
    
class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("DbPost", back_populates='comments')
    





##################################################################################################################

### Database Relationships Explanation ###

# DbUser and DbPost
'''

The DbUser and DbPost classes define a typical one-to-many relationship between users and posts using SQLAlchemy ORM, where:

DbUser represents the user who can have multiple posts.
DbPost represents individual posts by users. Each post includes an image_url, image_url_type, caption, and timestamp.
Relationship Details:

DbUser.items: This is a relationship attribute in DbUser that represents a collection of posts related to the user. It uses the relationship function from SQLAlchemy to establish a link to the DbPost model.
back_populates='user' in DbUser.items indicates that the user attribute in the DbPost model is linked back to this relationship, ensuring bidirectional access.

DbPost.user: This is a relationship attribute in DbPost that points back to the associated DbUser (i.e., the creator of the post).
ForeignKey('user.id') in the user_id field defines that this column in the post table references the id field of the user table, establishing the foreign key constraint.
back_populates='items' in DbPost.user ensures that changes to the user's details or the post details are synchronized between DbUser.items and DbPost.user.

'''