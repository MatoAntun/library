from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Book])
def read_books(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
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
    author_id: int
) -> Any:
    """
    Create new book.
    """
    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=author_id)
    return book


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
    if not crud.user.is_superuser(current_user): #TODO check for user role
        raise HTTPException(status_code=400, detail="Not enough permissions")
    book = crud.book.update(db=db, db_obj=book, obj_in=book_in)
    return book


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
    book = crud.book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    book = crud.book.remove(db=db, id=id)
    return book
