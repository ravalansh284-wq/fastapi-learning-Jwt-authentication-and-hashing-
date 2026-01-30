from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models,schemas,hashing,jwt_token
from models import User
from schemas import UserCreate,Token
from database import get_db
from typing import List

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = jwt_token.verify_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_admin_user(current_user:User=Depends(get_current_user)):
    user_roles_names=[link.role.name for link in current_user.role_links]
    if "Admin" not in user_roles_names:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return current_user
@app.get('/')
def home():
    return {"message":"Welcome!"}


@app.get("/users/all",response_model=List[schemas.UserResponse])
def get_all_user(db:Session=Depends(get_db),admin:User=Depends(get_admin_user)):
    users=db.query(User).all()
    return users

@app.post('/signup')
def signup(user: UserCreate,db:Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hashing.Hash.bcrypt(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_role = db.query(models.Role).filter(models.Role.name=="User").first()
    if user_role:
        new_link = models.UserRole(user_id=new_user.id,role_id=user_role.id)
        db.add(new_link)
        db.commit()

    return {"msg":"User created successfully"}

@app.post('/login',response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    if not hashing.Hash.verify(user.hashed_password,request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Password"
        )
    
    access_token = jwt_token.create_access_token(data={"sub":user.username})

    return {"access_token":access_token,"token_type":"bearer"} 

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.delete("/users/delete/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db),admin:User=Depends(get_admin_user)):
    user_to_delete=db.query(User).filter(User.id==user_id).first()

    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    db.delete(user_to_delete)
    db.commit()

    return {"msg":f"User {user_id} deleted successfully"}
@app.put("/promote/{username}")
def promote_user(username:str,db:Session=Depends(get_db),current_admin:User=Depends(get_admin_user)):
    user_to_promote=db.query(User).filter(User.username==username).first()

    if not user_to_promote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    
    admin_role=db.query(models.Role).filter(models.Role.name=="Admin").first()
    existing_link=db.query(models.UserRole).filter(
        models.UserRole.user_id==user_to_promote.id,
        models.UserRole.role_id==admin_role.id
    ).first()

    if existing_link:
        return {"msg":f"{username} is already an Admin"}
    
    new_link=models.UserRole(user_id=user_to_promote.id,role_id=admin_role.id)
    db.add(new_link)
    db.commit()

    return {"msg":f"Success {username} has been promoted to Admin"}

@app.post("/posts",response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    new_post=models.Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts',response_model=List[schemas.PostResponse])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

@app.delete('/post/{post_id}')
def delete_post(post_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()

    return {"msg": "Post deleted successfully"}
