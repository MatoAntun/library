import numbers
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Book(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    hard_copies = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
