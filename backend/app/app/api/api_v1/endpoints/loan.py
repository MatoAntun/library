from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Loan])
def read_loan(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve loans.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    books = crud.loan.get_multi(db, skip=skip, limit=limit)

    return books


@router.post("/", response_model=schemas.Loan)
def create_loan(
    *,
    db: Session = Depends(deps.get_db),
    loan_in: schemas.LoanCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new loan.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    book_id = loan_in.book_id
    book = crud.book.get(db=db, id=book_id)

    if not crud.user.get(db=db, id=loan_in.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if crud.loan.get_loans(db=db, user_id=loan_in.user_id, book_id=book_id):
        raise HTTPException(status_code=405, detail="Book already borowed")

    if not len(crud.loan.filter_loans(db=db, user_id=loan_in.user_id)) < 3:
        raise HTTPException(status_code=405, detail="Only 3 book per user allowed")

    if not book.hard_copies > 0:
        raise HTTPException(status_code=405, detail="No book avaliable")

    crud.book.loan_book(db=db, db_obj=book)
    loan = crud.loan.create(db=db, obj_in=loan_in)

    return loan


@router.put("/{id}", response_model=schemas.LoanInDB)
def return_book(
    *,
    db: Session = Depends(deps.get_db),
    loan_in: schemas.LoanUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Return an loaned book.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    book = crud.book.get(db=db, id=loan_in.book_id)
    loan = crud.loan.get_loan(db=db, loan_in=loan_in)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not crud.user.get(db=db, id=loan_in.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    crud.book.return_book(db=db, db_obj=book)

    loan_returned = crud.loan.return_loan(db=db, db_obj=loan)

    return loan_returned


@router.get("/me", response_model=List[schemas.LoanInDB])
def read_current_user_history(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user loan history. Ordered by date of creation.
    """

    loans = crud.loan.get_history(db, user_id=current_user.id)

    return loans


@router.get("/user", response_model=List[schemas.LoanInDB])
def read_user_history(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get user loan history. Ordered by date of creation.
    """
    if int(current_user.role.value) > 1:
        loans = crud.loan.get_history(db, user_id=user_id)

    return loans


@router.get("/not_avaliable", response_model=List[schemas.Book])
def read_out_of_stock(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get out of stock.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    books = crud.book.out_of_stock(db=db)

    return books


@router.delete("/", response_model=schemas.Loan)
def delete_book(
    *,
    db: Session = Depends(deps.get_db),
    loan_in: schemas.LoanUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an loan.
    """
    if int(current_user.role.value) > 1:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    loan = crud.loan.loan_by_id(db=db, loan_in=loan_in)
    if not loan:
        raise HTTPException(
            status_code=404, detail="Loan can not be deleted before book returned"
        )

    return crud.loan.remove(db=db, db_obj=loan)
