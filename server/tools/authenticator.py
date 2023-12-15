from functools import lru_cache
from secrets import compare_digest

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from genie_common.tools import logger
from starlette.status import HTTP_401_UNAUTHORIZED


class Authenticator:
    def __init__(self, username: str, password: str):
        self._username = self._to_bytes(username)
        self._password = self._to_bytes(password)

    def authenticate(self, credentials: HTTPBasicCredentials):
        logger.info("Authenticating request credentials")
        is_correct_username = self._authenticate_single_pair(credentials.username, self._username)
        is_correct_password = self._authenticate_single_pair(credentials.password, self._password)

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    def _authenticate_single_pair(self, actual: str, expected: bytes) -> bool:
        actual_bytes = self._to_bytes(actual)
        return compare_digest(actual_bytes, expected)

    @staticmethod
    @lru_cache
    def _to_bytes(s: str) -> bytes:
        return s.encode("utf8")
