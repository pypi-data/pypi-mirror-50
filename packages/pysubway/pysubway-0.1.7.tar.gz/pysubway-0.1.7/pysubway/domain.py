from typing import Any

from pysubway.model.role import Role
from pysubway.model.role_permission import RolePermission
from pysubway.model.user import User


class PermissionFactory:

    def __new__(self, style: str) -> Any:
        if style.lower() == 'db':
            return PermissionDB
        raise NotImplementedError(f'the style {style} is not supported now.')


class PermissionBase:
    """
    username, email and phone must be all unique.
    """

    def can_do(self, block_uuid: str, username: str = '', email: str = '', phone: str = '') -> None:
        raise NotImplementedError('')


class PermissionDB:

    def __init__(self, User: User, Role: Role, RolePermission: RolePermission):
        self.User = User
        self.Role = Role
        self.RolePermission = RolePermission

    def can_do(self, block_uuid: str, username: str = '', email: str = '', phone: str = '') -> bool:
        role_uuid = self.User.get_role(username=username, email=email, phone=phone)
        if not role_uuid:
            return False
        return self.RolePermission.the_role_can_do(role_uuid, block_uuid)
