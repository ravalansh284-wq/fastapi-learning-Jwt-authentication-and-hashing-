from pydantic import BaseModel,EmailStr
from typing import List,Optional


class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    class Config:
        from_attributes = True

class UserRoleResponse(BaseModel):
    role: RoleBase
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role_links: List[UserRoleResponse] = []
    posts: List[PostResponse]
    class Config:
        from_attributes = True