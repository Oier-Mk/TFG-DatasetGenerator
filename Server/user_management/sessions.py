from pydantic import BaseModel
from fastapi import HTTPException, Request
from uuid import UUID
from fastapi import Request
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.frontends.session_frontend import ID, FrontendError
from typing import Union
from fastapi_sessions.backends.session_backend import BackendError
from fastapi_sessions.frontends.session_frontend import ID, FrontendError


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=False,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True
    

    # async def __call__(self, request: Request):
    #     try:
    #         session_id: Union[ID, FrontendError] = request.state.session_ids[
    #             self.identifier
    #         ]
    #         session_data = await self.backend.read(session_id)
    #         if not session_data or not self.verify_session(session_data):
    #             if self.auto_error:
    #                 return self.auth_http_exception 
    #             return
    #     except Exception:
    #         session_data = None
    #         print("session_data = None")

    #     return session_data


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=backend,
    auth_http_exception="no user"
)