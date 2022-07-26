from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/search")
def search_books(
    search: str = "",
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> schemas.BookSchema:
    """
    Retrieve books.
    """

    books = crud.book.search(db, search=search)

    return books


@router.get("/", response_model=List[schemas.Book])
def read_books(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve books.
    """
    books = crud.book.get_multi(db, skip=skip, limit=limit)

    return books


@router.post("/", response_model=schemas.Book)
def create_book(
    *,
    db: Session = Depends(deps.get_db),
    book_in: schemas.BookCreate,
    current_user: models.User = Depends(deps.get_current_user),
    author_id: int,
) -> Any:
    """
    Create new book.
    """
    if not crud.author.get(db, id=author_id):
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.book.create_with_author(db=db, obj_in=book_in, author_id=author_id)


@router.put("/{id}", response_model=schemas.Book)
def update_book(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    book_in: schemas.BookUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an book.
    """
    book = crud.book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not crud.user.is_superuser(current_user):  # TODO check for user role
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.book.update(db=db, db_obj=book, obj_in=book_in)


@router.delete("/{id}", response_model=schemas.Book)
def delete_book(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an book.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    book = crud.book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return crud.book.remove(db=db, id=id)
