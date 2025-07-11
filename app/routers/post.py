from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from typing_extensions import List,Optional
from .. import models,schemas,oauth2
from sqlalchemy import func
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

#getting all post
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                limit:int=10,skip:int=0,search : Optional[str]=""):
    # print(search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts

#create post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends
                 (oauth2.get_current_user)):
    #                (post.title,post.content,post.published))Authorization: Bearer <your_access_token>
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#getting individual post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user:int = Depends
                 (oauth2.get_current_user)):
    # manually convert to int even if we gave int as paramenter it will default change to str
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post=cursor.fetchone()
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    # print(post)

    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        #instead of below lines import http and then use that
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    return post

#to delete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db),current_user:int = Depends
                 (oauth2.get_current_user)):
    #deleting post
    #find index in the array that has req id
    #my_post.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)

    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')
    # to check if that user deleting their post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized " \
        "to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends
                 (oauth2.get_current_user)):
    #                WHERE id = %s RETURNING * """,
    #                (post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} doesnot exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized " \
        "to perform requested action")

    post_query.update(updated_post.dict(),
                      synchronize_session=False)
    db.commit()
    return post_query.first()