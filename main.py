from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing_extensions import Optional
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating: Optional[int]=None

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"favorite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
#request get method url takes this first = '/'
@app.get("/")
def root():
    return {"message":"Welcome to my api!!!!!"}

@app.get("/posts")
def get_posts():
    return{"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):
    # print(post)
    # print(post.dict())
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id):
    # manually convert to int() even if we gave int as paramenter it will default change to str
    post=find_post(int(id))
    print(post)
    return{"Post detail":post}

