from dataclasses import dataclass
from typing import (
    Type,
    Dict,
    NewType,
    Optional,
    Any,
    Union,
    Tuple,
    Callable,
    cast,
    Sequence,
    ValuesView,
)
from collections import namedtuple

import requests
from requests.models import Response
from mypy_extensions import KwArg

from .method import Method


Url = NewType("Url", str)
HeaderName = NewType("HeaderName", str)
HeaderVar = NewType("HeaderVar", str)
HeaderMap = Dict[HeaderName, HeaderVar]
ParamName = NewType("ParamName", str)
Param = Dict[ParamName, Any]
PathParamName = NewType("PathParamName", str)
DataParamName = NewType("DataParamName", str)
PathParam = Dict[PathParamName, Param]
Payload = Dict[DataParamName, Param]
Headers = Dict[HeaderVar, Any]
HeaderDetail = Dict[HeaderName, Headers]
Cookies = Dict[str, Any]


class UnknownHeaderError(Exception):
    pass


class HandlerBase:
    def __init__(
        self,
        api_base_url: Url,
        header_map: HeaderMap,
        headers: Headers,
        cookies: Cookies,
    ):
        self.api_base_url = api_base_url
        self.header_map = header_map
        self.cookies = cookies
        for var, val in headers.items():
            if not self._inverted_header_map.get(cast(HeaderVar, var)):
                raise UnknownHeaderError(var)
            setattr(self, var, val)

    def _header_name_from_var(self, var: HeaderVar) -> HeaderName:
        return self._inverted_header_map[var]

    @property
    def _inverted_header_map(self) -> Dict[HeaderVar, HeaderName]:
        return {v: k for k, v in self.header_map.items()}

    @property
    def _header_vars(self) -> ValuesView[HeaderVar]:
        return self.header_map.values()

    @property
    def headers(self) -> HeaderDetail:
        return {
            self._header_name_from_var(v): getattr(self, v) for v in self._header_vars
        }

    def _build_param(self, method: Method, params: Param) -> Payload:
        return {
            DataParamName(
                "params" if method in (Method.Get, Method.Delete) else "data"
            ): params
            or {}
        }

    def _build_url(self, endpoint: str) -> Url:
        return Url(f"{self.api_base_url}/{endpoint}")

    def _apply_path_params(self, endpoint: str, **path_params: PathParam) -> str:
        # SO UGLY
        for k, v in path_params.items():
            endpoint = endpoint.replace(f":{k}", cast(str, v))
        return endpoint

    def _request(
        self, url: Url, method: Method, cookies: Cookies, **payload
    ) -> Type[Response]:
        raise NotImplementedError

    def method(
        self, meth: Method, endpoint: str
    ) -> Callable[[KwArg(Param)], Type[Response]]:
        class Requestor:
            def __init__(self, handler):
                self.handler = handler
                self._extra_cookies = {}

            def set_cookies(self, **cookies: Cookies) -> "Requestor":
                self._extra_cookies = cookies
                return self

            def reset_cookies(self) -> "Requestor":
                self._extra_cookies = {}
                return self

            def add_cookies(self, **cookies: Cookies) -> "Requestor":
                self._extra_cookies.update(cookies)
                return self

            def __call__(self, **params: Param) -> Type[Response]:
                return self.handler._request(  # type: ignore
                    self.handler._build_url(endpoint),
                    meth,
                    {**self.handler.cookies, **self._extra_cookies},
                    **self.handler._build_param(meth, cast(Param, params)),
                )

        return Requestor(self)

    def method_with_path_params(
        self, meth: Method, endpoint: str
    ) -> Callable[[KwArg(PathParam)], Callable[[KwArg(Param)], Type[Response]]]:
        def _req(**path_params: PathParam) -> Callable[[KwArg(Param)], Type[Response]]:
            return self.method(meth, self._apply_path_params(endpoint, **path_params))

        return _req


class SyncHandler(HandlerBase):
    def _build_request(self, method: Method) -> Callable[..., Type[Response]]:
        return getattr(requests, method.value)

    def _request(
        self, url: Url, method: Method, cookies: Cookies, **payload
    ) -> Type[Response]:
        return self._build_request(method)(
            url, headers=self.headers, cookies=cookies, **payload
        )


MetaMap = namedtuple("MetaMap", "method url")


class MethodMap(dict):
    def __init__(self, *tuples: Tuple[str, Method, Url]):
        for name, method, url in tuples:
            self[name] = MetaMap(method, url)

    @property
    def method_names(self):
        return self.keys()


def detect_method_name(url: Url) -> str:
    return "method_with_path_params" if ":" in url else "method"


class Client:
    name: str
    _method_map: MethodMap
    api_base_url: Url
    header_map: Optional[HeaderMap] = None

    def __init__(self, headers: Headers, cookies: Cookies):
        if not hasattr(self, "_method_map"):
            raise NotImplementedError("_method_map")
        if not isinstance(self._method_map, MethodMap):
            raise TypeError("_method_map must be a MethodMap instance")
        sync_handler = SyncHandler(
            self.api_base_url, self.header_map or {}, headers, cookies
        )

        for name, meta in self._method_map.items():
            client_method = detect_method_name(meta.url)
            setattr(
                self, name, getattr(sync_handler, client_method)(meta.method, meta.url)
            )

    @property
    def method_names(self):
        return self.methods.method_names

    @property
    def methods(self):
        return self._method_map
