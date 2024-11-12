#!/usr/bin/env python3
""" a class to manage the API authentication.
"""
from flask import request
from typing import List


class Auth:
    """ a class to manage the API authentication.
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """a function that returns True if the path is not in the list of
        """
        return False
    
    def authorization_header(self, request=None) -> None:
        """function that handles authorization header
        """
        return None
    
    def current_user(self, request=None) ->None:
        """function that handles current user
        """
        return None
    
if __name__ == "__main__":
    a = Auth()
    print(a.require_auth("/api/v1/status", ["/api/v1/status"]))
    print(a.authorization_header())
    print(a.current_user())