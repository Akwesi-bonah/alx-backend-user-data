#!/usr/bin/env python3
"""a module to manage the API authentication
"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a User ID based on a Session ID'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value'''
        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''deletes the user session / logout'''
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_by_session_id.get(session_id, None) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
