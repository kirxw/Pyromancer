import asyncio
import inspect
from typing import Any, Callable

class Event:
    listeners: list[Callable[...,Any]]
    name: str | None
    buffer: list[Any]

    def __init__(self, name: str | None = None):
        self.name = name
        self.listeners = []
        self.buffer = []

    def bind(self, f: Callable[...,Any]):
        assert f not in self.listeners, "Attempt to bind already bound function"
        self.listeners.append(f)

        if len(self.buffer) > 0:
            loop = asyncio.get_running_loop()
            while len(self.buffer) > 0:
                bufferobj = self.buffer.pop(0)
                loop.create_task(self.invoke(*bufferobj["args"],**bufferobj["kwargs"]))

    def unbind(self, f: Callable[...,Any]):
        assert f in self.listeners, "Function was not bound"
        self.listeners.remove(f)

    async def invoke(self, *args: Any, **kwargs: Any):
        if len(self.listeners) == 0:
            bufferobj = {}
            bufferobj["args"] = args
            bufferobj["kwargs"] = kwargs
            self.buffer.append(bufferobj)
            return
        
        for listener in self.listeners:
            if inspect.iscoroutinefunction(listener):
                await listener(*args,**kwargs)
            else:
                listener(*args,**kwargs)