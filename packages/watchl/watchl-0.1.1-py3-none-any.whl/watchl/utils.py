import asyncio
import concurrent.futures
import time
import typing


async def _async_follow(
    stream: typing.IO[str]
) -> typing.AsyncGenerator[str, None]:
    loop = asyncio.get_event_loop()
    num_threads = 1  # Only need one thread to delegate blocking file I/O to.

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=num_threads
    ) as executor:
        while True:
            line = await loop.run_in_executor(executor, stream.readline)
            line = line.strip("\x00")  # Encountered in Docker.
            if not line:
                time.sleep(0.5)
                continue
            assert line.endswith("\n"), repr(line)
            yield line


async def async_tail(filename: str) -> typing.AsyncGenerator[str, None]:
    with open(filename, "r", encoding="utf-8") as f:
        _end = 2
        f.seek(0, _end)
        async for line in _async_follow(f):
            yield line.strip()


async def timer(interval: float):
    while True:
        await asyncio.sleep(interval)
        yield


class Background:
    __slots__ = ("tasks", "funcs")

    def __init__(self):
        self.tasks = set()
        self.funcs = set()

    def task(self, func: typing.Callable[[], typing.Awaitable[None]]):
        self.funcs.add(func)
        return func

    async def check_for_exceptions(self):
        if not self.tasks:
            return
        done, self.tasks = await asyncio.wait(self.tasks, timeout=0)
        for task in done:
            task.result()

    async def __aenter__(self) -> "Background":
        loop = asyncio.get_event_loop()
        for func in self.funcs:
            self.tasks.add(loop.create_task(func()))
        return self

    async def __aexit__(self, *args):
        await self.check_for_exceptions()
        for task in self.tasks:
            task.cancel()
