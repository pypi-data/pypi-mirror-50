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
Cookie = Dict[str, Any]


class UndefinedHeaderVarError(Exception):
    pass


class ClientBase:
    def __init__(
        self,
        api_base_url: Url,
        header_map: Optional[HeaderMap] = None,
        **headers: Headers,
    ):
        self.api_base_url = api_base_url
        self.header_map = header_map
        for var, val in headers.items():
            if not self._inverted_header_map.get(cast(HeaderVar, var)):
                raise UndefinedHeaderVarError(var)
            setattr(self, var, val)

    @property
    def _h(self) -> HeaderMap:
        return self.header_map or {}

    def _header_name_from_var(self, var: HeaderVar) -> HeaderName:
        return self._inverted_header_map[var]

    @property
    def _inverted_header_map(self) -> Dict[HeaderVar, HeaderName]:
        return {v: k for k, v in self._h.items()}

    @property
    def _header_vars(self) -> ValuesView[HeaderVar]:
        return self._h.values()

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

    def _request(self, url: Url, method: Method, **payload) -> Type[Response]:
        raise NotImplementedError

    def method(
        self, meth: Method, endpoint: str
    ) -> Callable[[KwArg(Param)], Type[Response]]:
        def _req(**params) -> Type[Response]:
            return self._request(  # type: ignore
                self._build_url(endpoint),
                meth,
                **self._build_param(meth, cast(Param, params)),
            )

        return _req

    def method_with_path_params(
        self, meth: Method, endpoint: str
    ) -> Callable[[KwArg(PathParam)], Callable[[KwArg(Param)], Type[Response]]]:
        def _req(**path_params: PathParam) -> Callable[[KwArg(Param)], Type[Response]]:
            def __req(**params: Param) -> Type[Response]:
                return self.method(
                    meth, self._apply_path_params(endpoint, **path_params)
                )(**params)

            return __req

        return _req


class SyncClient(ClientBase):
    _cookies: Cookie

    def __init__(
        self,
        api_base_url: Url,
        header_map: Optional[HeaderMap] = None,
        **headers: Headers,
    ):
        super().__init__(api_base_url, header_map, **headers)
        self._cookies = {}

    def set_cookies(self, **cookies) -> "SyncClient":
        self._cookies = cookies
        return self

    def reset_cookies(self) -> "SyncClient":
        self._cookies = {}
        return self

    def add_cookies(self, **cookies) -> "SyncClient":
        self._cookies.update(cookies)
        return self

    def _build_request(self, method: Method) -> Callable[..., Type[Response]]:
        return getattr(requests, method.value)

    def _request(self, url: Url, method: Method, **payload) -> Type[Response]:
        return self._build_request(method)(
            url, headers=self.headers, **payload, cookies=self._cookies
        )


class AsyncClient(ClientBase):
    def __init__(self):
        raise NotImplementedError


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

    def __init__(self, **headers: Headers):
        if not hasattr(self, "_method_map"):
            raise NotImplementedError("_method_map")
        if not isinstance(self._method_map, MethodMap):
            raise TypeError("_method_map must be a MethodMap instance")
        sync_client = SyncClient(self.api_base_url, self.header_map, **headers)

        # TODO:
        # async_client = AsyncClient(**kwargs)

        for name, meta in self._method_map.items():
            client_method = detect_method_name(meta.url)
            setattr(
                self, name, getattr(sync_client, client_method)(meta.method, meta.url)
            )

    @property
    def method_names(self):
        return self.methods.method_names

    @property
    def methods(self):
        return self._method_map
