from fastapi import FastAPI

app=FastAPI()
#request get method url takes this first = '/'
@app.get("/")
def root():
    return {"message":"Welcome to my api!!!!!"}

@app.get("/posts")
def get_posts():
    return{"data":"This is your posts"}

