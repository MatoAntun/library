"""Model for Notes"""
from sqlite3 import DatabaseError
import uuid
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .book import Book  # noqa: F401

class Loan(Base):
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    returned_at = Column(DateTime, onupdate=datetime.datetime.utcnow, nullable=True)
    book = relationship("Book")
