from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Loan])
def read_books(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve loan.
    """
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

@router.put("/{id}", response_model=schemas.Loan)
def return_book(
    *,
    db: Session = Depends(deps.get_db),
    loan_in: schemas.LoanUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an loan.
    """
    book = crud.book.get(db=db, id=loan_in.book_id)
    loan = crud.loan.get_loan(db=db, loan_in = loan_in)
    print("Test loanl", loan)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not crud.user.get(db=db, id=loan_in.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if int(current_user.role.value) > 1:  # TODO check for user role
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    crud.book.return_book(db=db, db_obj=book)

    return crud.loan.update(db=db, db_obj=loan, obj_in=loan_in)

@router.get("/me", response_model=List[schemas.LoanInDB])
def read_current_user_history(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user history.
    """

    loans = crud.loan.get_history(db, user_id=current_user.id)
    from fastapi.encoders import jsonable_encoder

    print("unutar funckije", jsonable_encoder(loans))

    return loans


@router.get("/user", response_model=List[schemas.Loan])
def read_user_history(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user history.
    """

    loans = crud.loan.get_history(db, user_id=user_id)

    return loans
