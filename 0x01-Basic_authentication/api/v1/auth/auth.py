#!/usr/bin/env python3

"""
module for authentification
"""
from typing import List, TypeVar, Any


class Auth:
    """
    class for authentification
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require authentification
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> Any | None:
        """
        authorization header
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
