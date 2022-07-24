from .permission import Permission, RoleEnum


class UserPermission(Permission):
    def __init__(self):
        self.scope = [
            RoleEnum.SUPER_ADMIN.name,
            RoleEnum.LIBRARIAN.name,
            RoleEnum.USER.name
        ]
