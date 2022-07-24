from typing import Optional

from pydantic import BaseModel


# Shared properties
class AuthorBase(BaseModel):
    name: Optional[str] = None

# Properties to receive on author creation
class AuthorCreate(AuthorBase):
    name: str

# Properties to receive on author update
class AuthorUpdate(AuthorBase):
    pass


# Properties shared by models stored in DB
class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Author(AuthorInDBBase):
    pass


# Properties properties stored in DB
class AuthorInDB(AuthorInDBBase):
    pass
