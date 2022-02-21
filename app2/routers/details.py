from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models,schemas
from . import oauth2
from database import get_db
from typing import List, Optional
from sqlite3 import Cursor

router = APIRouter(
    prefix="/details",
    tags=["Details"]
)

@router.get('/',response_model=List[schemas.Post])
def test_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
limit: int = 10,skip: int = 0,search: Optional[str]= ""):
    posts = db.query(models.Post).filter(models.Post.student_name.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post)
    print(results)

    return  posts
#def get_details():
    #cursor.execute("SELECT * FROM student_details")
    #details= cursor.fetchall()
    #return {"data": Post}




@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id,**post.dict())
    #new_post = models.Post(student_id = post.student_id,student_name = post.student_name,
    #academic_year = post.academic_year,total_fees = post.total_fees,fees_paid = post.fees_paid,
    #balance_fees = post.balance_fees)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

#def create_posts(post: Post):
    #cursor.execute("""INSERT INTO student_details(student_name,academic_year,total_fees,fees_paid,
    #balance_fees) VALUES (%s,%s,%s,%s,%s) RETURNING *""",(post.student_name,post.academic_year,
    #post.total_fees,post.fees_paid,post.balance_fees))
    #new_details=cursor.fetchall()
    #conn.commit()
    #return {"data" : new_details}




@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.student_id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return  post
    
#def get_details(id: int):
    #cursor.execute("""SELECT * FROM student_details WHERE student_id = %s""",(str(id)))
    #test_post=cursor.fetchone()
    #if not test_post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    #return {"data" : test_post}




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.student_id == id)
    post = post_query.first()
    print(current_user.email)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#def delete_post(id: int):
    #cursor.execute("""DELETE FROM student_details WHERE student_id = %s returning *""",(str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    #if not deleted_post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    #return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/test/{id}")
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.student_id == id)
    post = post_query.first()   

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()
    


#def update_post(id: int, post: Post):
    #cursor.execute("""UPDATE student_details SET student_name=%s,academic_year=%s,total_fees=%s,
     #fees_paid=%s,balance_fees=%s WHERE student_id = %s RETURNING *""",(post.student_name,post.academic_year,
     #post.total_fees,post.fees_paid,post.balance_fees,(str(id))))
    #updated_post=cursor.fetchone()
    #conn.commit()

    #if not updated_post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    #return {"data" : updated_post}




#@router.get("/joindata/{student_id}")
#def join_data(student_id: int):
    #cursor.execute("""SELECT * FROM student_details as sd join personal_info as pi on sd.student_id=pi.student_id
    #WHERE sd.student_id = %s""",(str(student_id)))
    #joined_data=cursor.fetchone()
    #return  joined_data
    