from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: BookCreate, author_id: int
    ) -> Book:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj    
    
    def loan_book(
        self, db: Session, *, db_obj: Book
    ) -> Book:
        obj_in_data = jsonable_encoder(db_obj)
        setattr(db_obj, 'hard_copies', obj_in_data.get("hard_copies") - 1)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj    

    def return_book(
        self, db: Session, *, db_obj: Book
    ) -> Book:
        obj_in_data = jsonable_encoder(db_obj)
        setattr(db_obj, 'hard_copies', obj_in_data.get("hard_copies") + 1)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj  

book = CRUDBook(Book)
