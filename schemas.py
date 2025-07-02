from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
        
        
        
from fastapi_users import schemas
from uuid import UUID

# class UserRead(schemas.BaseUser[UUID]):
#     pass

# class UserCreate(schemas.BaseUserCreate):
#     pass

# class UserUpdate(schemas.BaseUserUpdate):
#     pass

class UserRead(schemas.BaseUser[UUID]):
    is_superuser: bool = False

class UserCreate(schemas.BaseUserCreate):
    is_superuser: Optional[bool] =None

class UserUpdate(schemas.BaseUserUpdate):
    is_superuser: Optional[bool] = None

