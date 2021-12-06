from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from sqlalchemy.sql.elements import True_

from app.database import Base

class Postbase(BaseModel):
    title: str
    content: str

class PostCreate(Postbase):
    pass
class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True
        
class PostResponse(Postbase):
    id: int
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)