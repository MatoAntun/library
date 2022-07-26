from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.author import AuthorCreate
from app.tests.utils.utils import random_lower_string


def create_random_author(db: Session,) -> models.Author:
    title = random_lower_string()
    author_in = AuthorCreate(title=title)

    return crud.author.create(db=db, obj_in=author_in)
