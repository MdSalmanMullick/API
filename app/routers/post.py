from sys import prefix
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import current_user
from starlette.routing import Route
from .. import models, schemas, oauth
from typing import List, Optional
from .. database import get_db
router = APIRouter()
@router.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
@router.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db : Session = Depends(get_db), search: Optional[str] = ""):
        #cursor.execute("""SELECT * FROM posts""")
        #posts=cursor.fetchall()
        posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()
        return posts
@router.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def post(newpost: schemas.PostCreate, db : Session = Depends(get_db), user_id: int =  Depends(oauth.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *""", (newpost.title, newpost.content))
    #new_post=cursor.fetchone()
    #conn.commit()
    #post_dict=newpost.dict()
    #post_dict['id']= randrange(0,99999999)
    #savedposts.append(post_dict)
    new_post = models.Post(owner_id = user_id.id, **newpost.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
@router.get("/posts/{id}", response_model= schemas.PostResponse)
def get_post(id:int,response:Response, db : Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id)))
    #test_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db), user_id: int =  Depends(oauth.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id =%s RETURNING *""",(str(id)))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"not authorized to perform requested action" )
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_posts(id :int, updated_post:schemas.PostCreate, db : Session = Depends(get_db), user_id: int =  Depends(oauth.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title= %s, content=%s WHERE id=%s RETURNING *""",(post.title,post.content,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"not authorized to perform requested action")
    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()