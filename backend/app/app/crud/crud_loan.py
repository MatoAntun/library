import datetime
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanInDB, LoanUpdate


class CRUDLoan(CRUDBase[Loan, LoanCreate, LoanUpdate]):
    def loan_by_id(self, db: Session, *, loan_in: LoanUpdate) -> LoanInDB:
        loan = (
            db.query(self.model)
            .filter(
                and_(Loan.user_id == loan_in.user_id, Loan.book_id == loan_in.book_id)
            )
            .first()
        )
        return loan

    def get_loan(self, db: Session, *, loan_in: LoanUpdate) -> LoanInDB:
        loan = (
            db.query(self.model)
            .filter(
                and_(Loan.user_id == loan_in.user_id, Loan.book_id == loan_in.book_id)
            )
            .filter(Loan.returned_at.is_(None))
            .first()
        )
        return loan

    def filter_loans(self, db: Session, *, user_id: int) -> List[Loan]:
        return (
            db.query(self.model)
            .filter(and_(Loan.user_id == user_id, Loan.returned_at.is_(None)))
            .all()
        )

    def get_loans(self, db: Session, *, user_id: int, book_id: int) -> List[Loan]:
        return (
            db.query(self.model)
            .filter(and_(Loan.user_id == user_id, Loan.book_id == book_id))
            .filter(Loan.returned_at.is_(None))
            .all()
        )

    def return_loan(self, db: Session, *, db_obj: Loan) -> Loan:
        setattr(db_obj, "returned_at", datetime.datetime.utcnow())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_history(self, db: Session, *, user_id: int) -> List[Loan]:
        return (
            db.query(Loan)
            .filter(Loan.user_id == user_id)
            .order_by(Loan.created_at)
            .all()
        )

    def remove(self, db: Session, *, db_obj: Loan) -> LoanInDB:
        db.delete(db_obj)
        db.commit()
        return db_obj


loan = CRUDLoan(Loan)
