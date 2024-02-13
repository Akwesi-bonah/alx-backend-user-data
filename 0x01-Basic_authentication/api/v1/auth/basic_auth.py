#!/usr/bin/env python3
""" Basic auth module
"""
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
import base64, binascii
from models.user import User

class BasicAuth(Auth):
    """ Basic auth class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extract base64 authorization header
        """
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """ Decode base64 authorization header
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            
            decoded_bytes = base64.b64decode(
                base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            
            return decoded_string
        except (binascii.Error, UnicodeDecodeError):
            return None 
    
    def extract_user_credentials(self, 
                                 decoded_base64_authorization_header: str) -> Tuple[str, str]:
            """
            Extract user credentials from the Base64 decoded value.
            """

            if decoded_base64_authorization_header is None \
                    or not isinstance(decoded_base64_authorization_header, str):
                return (None, None)

            if ':' not in decoded_base64_authorization_header:
                return (None, None)

            email, password = decoded_base64_authorization_header.split(':', 1)

            return email, password
    
    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        user object from credentials
        """

        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)