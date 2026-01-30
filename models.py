from sqlalchemy import Column,String,Integer,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    hashed_password=Column(String)
    role_links=relationship("UserRole",back_populates="user")
    posts=relationship("Post",back_populates="owner")


class Role(Base):
    __tablename__="roles"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True)
    user_links=relationship("UserRole",back_populates="role")


class UserRole(Base):
    __tablename__="users_roles"
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    role_id=Column(Integer,ForeignKey('roles.id'),primary_key=True)
    user=relationship("User",back_populates="role_links")
    role=relationship("Role",back_populates="user_links")

class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    content=Column(String)
    owner_id = Column(Integer,ForeignKey("users.id"))
    owner=relationship("User",back_populates="posts")


