""" A simple bindable event """

import asyncio
import inspect
from collections.abc import Callable
from typing import Any


class Event:
    """ A simple bindable event """

    listeners: list[Callable[..., Any]]
    name: str | None
    buffer: list[Any]

    def __init__(self, name: str | None = None):
        self.name = name
        self.listeners = []
        self.buffer = []

    def bind(self, f: Callable[..., Any]):
        """ Binds a callable to the event, sync and async both work """

        assert f not in self.listeners, "Attempt to bind already bound function"
        self.listeners.append(f)

        if len(self.buffer) > 0:
            while len(self.buffer) > 0:
                bufferobj = self.buffer.pop(0)
                self.invoke(*bufferobj["args"], **bufferobj["kwargs"])

    def unbind(self, f: Callable[..., Any]):
        """ Unbinds a callable from the event """

        assert f in self.listeners, "Function was not bound"
        self.listeners.remove(f)

    def invoke(self, *args: Any, **kwargs: Any):
        """ Asynchronously invokes all bound callables, this method is safe """

        if len(self.listeners) == 0:
            bufferobj = {}
            bufferobj["args"] = args
            bufferobj["kwargs"] = kwargs
            self.buffer.append(bufferobj)
            return

        loop = asyncio.get_running_loop()
        loop.create_task(self.invoke_blocking(*args, **kwargs))

    async def invoke_blocking(self, *args: Any, **kwargs: Any):
        """ Invokes all bound callables in turn, this method is unsafe """

        if len(self.listeners) == 0:
            bufferobj = {}
            bufferobj["args"] = args
            bufferobj["kwargs"] = kwargs
            self.buffer.append(bufferobj)
            return

        for listener in self.listeners:
            if inspect.iscoroutinefunction(listener):
                await listener(*args, **kwargs)
            else:
                listener(*args, **kwargs)
