#!/usr/bin/env python3
"""basic auth"""
import base64
import binascii
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa
        """extract base64 from header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # noqa
        """decode base64 from header"""
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')  # noqa
        except binascii.Error:
            return None
