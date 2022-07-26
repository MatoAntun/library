"""Model for User"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import Enum

from app.db.base_class import Base
from app.models.enums.role import RoleEnum


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(RoleEnum), nullable=False)
