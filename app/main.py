from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth
from .config import settings

print(settings.database_password)
    

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#request get method url takes this first = '/'
@app.get("/")
def root():
    return {"message":"Welcome to my api!!!!!"}


