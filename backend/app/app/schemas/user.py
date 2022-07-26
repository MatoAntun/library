from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.enums.role import RoleEnum


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_superuser: bool = False
    name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.USER.value


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
