from typing import Sequence, Type, Optional

from .client import Client, Headers, MethodMap, Method, Cookies


def apply(*clients: Type[Client]):
    class _:
        def __init__(
            self, headers: Optional[Headers] = None, cookies: Optional[Cookies] = None
        ):
            for c in clients:
                setattr(self, c.name, c(headers=headers or {}, cookies=cookies or {}))

    return _
