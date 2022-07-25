"""Validing user permission"""
from fastapi import Depends, HTTPException

from app import models
from app.api import deps
from app.models.enums.role import RoleEnum


class Permission:
    """Validate user permission"""

    def __init__(self):
        self.scope = [RoleEnum.SUPER_ADMIN.name]

    def validate_permission(
        self, current_user: models.User = Depends(deps.get_current_user)
    ):
        if current_user.role.name not in self.scope:
            raise HTTPException(
                status_code=400, detail="The user doesn't have enough privileges"
            )
