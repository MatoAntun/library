"""Model for Loan"""
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .book import Book  # noqa: F401
    from .user import User  # noqa: F401


class Loan(Base):
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    book = relationship("Book")
