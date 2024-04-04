from base64 import b64decode
from functools import lru_cache
from secrets import compare_digest
from typing import Optional

from fastapi.security import HTTPBasicCredentials
from genie_common.tools import logger
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
from starlette.requests import HTTPConnection

AUTHORIZATION_HEADER = "Authorization"


class BasicAuthBackend(AuthenticationBackend):
    def __init__(self, username: str, password: str):
        self._username = self._to_bytes(username)
        self._password = self._to_bytes(password)

    async def authenticate(self, conn: HTTPConnection):
        logger.info("Authenticating request credentials")
        credentials = self._extract_credentials(conn)

        if credentials is not None:
            self._validate_authentication_details(credentials)
            return AuthCredentials(["authenticated"]), SimpleUser(credentials.username)

    @staticmethod
    def _extract_credentials(conn: HTTPConnection) -> Optional[HTTPBasicCredentials]:
        if AUTHORIZATION_HEADER not in conn.headers:
            return

        auth = conn.headers[AUTHORIZATION_HEADER]
        scheme, credentials = auth.split()

        if scheme.lower() == 'basic':
            decoded = b64decode(credentials).decode("ascii")
            username, _, password = decoded.partition(":")

            return HTTPBasicCredentials(username=username, password=password)

    def _validate_authentication_details(self, credentials: HTTPBasicCredentials) -> None:
        is_correct_username = self._authenticate_single_pair(credentials.username, self._username)
        is_correct_password = self._authenticate_single_pair(credentials.password, self._password)

        if not (is_correct_username and is_correct_password):
            raise AuthenticationError('Invalid basic auth credentials')

    def _authenticate_single_pair(self, actual: str, expected: bytes) -> bool:
        actual_bytes = self._to_bytes(actual)
        return compare_digest(actual_bytes, expected)

    @staticmethod
    @lru_cache
    def _to_bytes(s: str) -> bytes:
        return s.encode("utf8")
