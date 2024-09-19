#!/usr/bin/env python3
"""basic auth"""
from werkzeug.datastructures import auth
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
