from fastapi import FastAPI,Response,status,HTTPException
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
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


#request get method url takes this first = '/'
@app.get("/")
def root():
    return {"message":"Welcome to my api!!!!!"}

#getting all post
@app.get("/posts")
def get_posts():
    return{"data":my_posts}

#create post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    # print(post)
    # print(post.dict())
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

#getting individual post
@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    # manually convert to int even if we gave int as paramenter it will default change to str
    post=find_post(id)
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
def delete_post(id: int):
    #deleting post
    #find index in the array that has req id
    #my_post.pop(index)
    index=find_index_post(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')

    my_posts.pop(index)
    # return{'message':'post was successfully deleted'}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index=find_index_post(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return{'data':post_dict}