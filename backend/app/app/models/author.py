from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .book import Book  # noqa: F401

class Author(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    book = relationship("Book")
    # dodaj secoundary kod brisanja da se samo obrise