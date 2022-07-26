from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/search")
def search_authors(
    search: str = "",
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> schemas.AuthorSchema:
    """
    Retrieve and search authors.
    """

    authors = crud.author.search(db, search=search)

    return authors


@router.get("/", response_model=List[schemas.Author])
def read_authors(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve authors.
    """
    authors = crud.author.get_multi(db, skip=skip, limit=limit)

    return authors


@router.post("/", response_model=schemas.Author)
def create_author(
    *,
    db: Session = Depends(deps.get_db),
    author_in: schemas.AuthorCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new author.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    author = crud.author.create(db=db, obj_in=author_in)
    return author


@router.put("/{id}", response_model=schemas.Author)
def update_author(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    author_in: schemas.AuthorUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an author.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    author = crud.author.get(db=db, id=id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if not crud.user.is_superuser(current_user):  # TODO check for user role
        raise HTTPException(status_code=400, detail="Not enough permissions")
    author = crud.author.update(db=db, db_obj=author, obj_in=author_in)
    return author


@router.delete("/{id}", response_model=schemas.Author)
def delete_author(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an author.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    author = crud.author.get(db=db, id=id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    author = crud.author.remove(db=db, id=id)
    return author
