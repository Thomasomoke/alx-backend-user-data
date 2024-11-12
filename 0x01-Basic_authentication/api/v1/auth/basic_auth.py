#!/usr/bin/env python3
"""A class BasicAuth that inherits from Auth."""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """Basic Authentication class."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts Base64 part from the Authorization header."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 string."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (ValueError, TypeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts user email and password from the decoded Base64 string."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(':', 1)
