from typing import Sequence, Type

from .client import Client, Headers


def apply(*clients: Type[Client]):
    class _:
        def __init__(self, **headers: Headers):
            for c in clients:
                setattr(self, c.name, c(**headers))

    return _
