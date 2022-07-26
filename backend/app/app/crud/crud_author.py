from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.author import Author
from app.models.book import Book
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.schemas.book_author import AuthorSchema


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def search(self, db: Session, *, search: str) -> AuthorSchema:

        return (
            db.query(self.model)
            .options(joinedload(self.model.book))
            .where(self.model.id == Book.author_id)
            .filter(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    Book.title.ilike(f"%{search}%"),
                )
            )
            .all()
        )


author = CRUDAuthor(Author)
