""" Module containing Role enumeration """
from enum import Enum

class RoleEnum(str, Enum):
    """ Role enumeration """

    SUPER_ADMIN = 0
    LIBRARIAN = 1
    USER = 2
