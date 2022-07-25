from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class LoanBase(BaseModel):
    user_id: int
    book_id: int

# Properties to receive on Loan creation
class LoanCreate(LoanBase):
    pass

# Properties to receive on Loan update
class LoanUpdate(LoanBase):
    pass


# Properties shared by models stored in DB
class LoanInDBBase(LoanBase):

    class Config:
        orm_mode = True


# Properties to return to client
class Loan(LoanInDBBase):
    created_at: datetime


# Properties properties stored in DB
class LoanInDB(LoanInDBBase):
    created_at: datetime
    returned_at: Optional[datetime]
