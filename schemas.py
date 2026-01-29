from pydantic import BaseModel,EmailStr
from typing import List,Optional

class RoleBase(BaseModel):
    name:str
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
    class Config:
        from_attributes = True