from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.author import Author
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.schemas.book_author import BookSchema


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

    def loan_book(self, db: Session, *, db_obj: Book) -> Book:
        obj_in_data = jsonable_encoder(db_obj)
        setattr(db_obj, "hard_copies", obj_in_data.get("hard_copies") - 1)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def return_book(self, db: Session, *, db_obj: Book) -> Book:
        obj_in_data = jsonable_encoder(db_obj)
        setattr(db_obj, "hard_copies", obj_in_data.get("hard_copies") + 1)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def out_of_stock(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Book]:
        return (
            db.query(self.model)
            .filter(self.model.hard_copies == 0)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(self, db: Session, *, search: str) -> BookSchema:

        return (
            db.query(self.model)
            .options(joinedload(self.model.author))
            .where(self.model.author_id == Author.id)
            .filter(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    Author.name.ilike(f"%{search}%"),
                )
            )
            .all()
        )


book = CRUDBook(Book)
