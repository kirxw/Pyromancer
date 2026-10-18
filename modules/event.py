import inspect
from typing import Any, Callable

class Event:
    listeners: list[Callable[...,Any]]
    name: str | None

    def __init__(self, name: str | None = None):
        self.name = name
        self.listeners = []


    def bind(self, f: Callable[...,Any]):
        assert f not in self.listeners, "Attempt to bind already bound function"
        self.listeners.append(f)

    def unbind(self, f: Callable[...,Any]):
        assert f in self.listeners, "Function was not bound"
        self.listeners.remove(f)

    async def invoke(self, *args: Any, **kwargs: Any):
        for listener in self.listeners:
            if inspect.iscoroutinefunction(listener):
                await listener(*args,**kwargs)
            else:
                listener(*args,**kwargs)