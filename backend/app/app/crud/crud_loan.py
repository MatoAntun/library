from operator import and_
from typing import List
from app.models.book import Book

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.book import Book
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanUpdate


class CRUDLoan(CRUDBase[Loan, LoanCreate, LoanUpdate]):

    def get_loan(
        self, db: Session, *, loan_in: LoanUpdate
    ) -> List[Loan]:
        loan = (
            db.query(self.model)
            .filter(and_(
                Loan.user_id == loan_in.user_id,
                Loan.book_id == loan_in.book_id,
                )
            )
            .filter(Loan.returned_at == None)
            .first()
        )
        return loan

    def filter_loans(
        self, db: Session, *, user_id: int
    ) -> List[Loan]:
        return (
            db.query(self.model)
            .filter(Loan.user_id == user_id)
            .filter(Loan.returned_at == None)
            .all()
        )

    def get_loans(
        self, db: Session, *, user_id: int, book_id:int
    ) -> List[Loan]:
        return (
            db.query(self.model)
            .filter(and_(
                Loan.user_id == user_id,
                Loan.book_id == book_id
                )
            )
            .filter(Loan.returned_at == None)
            .all()
        )

    def get_history(self, db: Session, *, user_id: int) -> List[Loan]:
        return (db.query(Loan).filter(Loan.user_id == user_id).order_by(Loan.created_at).all())

loan = CRUDLoan(Loan)
