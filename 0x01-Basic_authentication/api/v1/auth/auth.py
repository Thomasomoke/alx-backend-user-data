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
        if path and not path.endswith("/"):
            path += "/"
        if not path or path not in excluded_paths:
            return True
        if not path:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        if path is excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> None:
        """function that handles authorization header
        """
        key = 'Authorization'

        if request is None or key not in request.headers:
            return
        return request.headers.get(key)

    def current_user(self, request=None) -> None:
        """function that handles current user
        """
        return None


if __name__ == "__main__":
    a = Auth()

    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(a.require_auth
          ("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))
