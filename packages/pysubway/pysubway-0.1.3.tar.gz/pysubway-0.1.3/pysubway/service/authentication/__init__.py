from typing import Optional

from .base import AuthenticationBase
from .db import AuthenticationDB
from .file import AuthenticationFile


class AuthenticationFactory:
    """
    file: should configure code book file;
    db:
    Ensure sqlalchemy should be callable when you call the class AuthenticationDB.
    And table block/role/role_permission/user should existed in database.
    """

    def __new__(self, style: str) -> Optional[type]:
        if style.lower() == 'file':
            return AuthenticationFile
        elif style.lower() == 'db':
            return AuthenticationDB
        raise NotImplementedError(f'the style {style} is not supported now.')
