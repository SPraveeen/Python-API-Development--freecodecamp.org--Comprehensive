from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing_extensions import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)


app=FastAPI()



class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating: Optional[int]=None

# while True:
# connecting database
try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                        password='123456789',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successfull")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ",error)
    time.sleep(2)

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"favorite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


#request get method url takes this first = '/'
@app.get("/")
def root():
    return {"message":"Welcome to my api!!!!!"}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return{"data":posts}

#getting all post
@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return{"data":posts}

#create post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

#getting individual post
@app.get("/posts/{id}")
def get_post(id:int,db:Session=Depends(get_db)):
    # manually convert to int even if we gave int as paramenter it will default change to str
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)

    if not post:
        #instead of below lines import http and then use that
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"Post with id: {id} was not found"}
    return{"Post detail":post}

#to delete a post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
    #deleting post
    #find index in the array that has req id
    #my_post.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post= db.query(models.Post).filter(models.Post.id==id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')
    post.delete(synchronize_session=False)
    db.commit()

    # return{'message':'post was successfully deleted'}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s 
    #                WHERE id = %s RETURNING * """,
    #                (post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')
    post_query.update(updated_post.dict(),
                      synchronize_session=False)
    db.commit()
    return{'data':post_query.first()}