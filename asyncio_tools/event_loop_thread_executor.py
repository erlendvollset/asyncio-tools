from __future__ import annotations

import asyncio
import threading
from types import TracebackType
from typing import Awaitable, Optional, Type, TypeVar

T = TypeVar("T")


class EventLoopThreadExecutor(threading.Thread):
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None, daemon: bool = True) -> None:
        super().__init__(name=self.__class__.__name__, daemon=daemon)
        self._event_loop = loop or asyncio.new_event_loop()

    def run(self) -> None:
        asyncio.set_event_loop(self._event_loop)
        self._event_loop.run_forever()

    def stop(self) -> None:
        self._event_loop.call_soon_threadsafe(self._event_loop.stop)
        self.join()

    def __enter__(self) -> EventLoopThreadExecutor:
        self.start()
        return self

    def __exit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        self.stop()

    def __call__(self, coro: Awaitable[T], timeout: Optional[float] = None) -> T:
        return asyncio.run_coroutine_threadsafe(coro, self._event_loop).result(timeout)
