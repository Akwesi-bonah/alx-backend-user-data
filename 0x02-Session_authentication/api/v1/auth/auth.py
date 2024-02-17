#!/usr/bin/env python3
"""a module to manage the API authentication
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''requires auth returns False - path'''
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path[-1] == '/':
            path = path[:-1]

        for p in range(len(excluded_paths)):
            if excluded_paths[p][-1] == '/':
                excluded_paths[p] = excluded_paths[p][:-1]
            if excluded_paths[p][-1] == '*':
                path_len = len(excluded_paths[p][:-1])
                if path[:path_len - 1] in excluded_paths[p][:-1]:
                    return False

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''authorization header returns None - request'''
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user returns None - request'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        if os.getenv('SESSION_NAME') is None:
            return
        return request.cookies.get(os.getenv('SESSION_NAME'))
