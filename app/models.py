from enum import unique
from pydantic.main import BaseModel
from sqlalchemy.orm import relationship

from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import false, null
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True,nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner =  relationship("User")
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True,nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
