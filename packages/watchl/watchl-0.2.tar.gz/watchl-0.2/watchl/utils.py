import typing

import trio


async def async_tail(filename: str) -> typing.AsyncGenerator[str, None]:
    async with await trio.open_file(filename, encoding="utf-8") as f:
        _end = 2
        await f.seek(0, _end)
        while True:
            line = await f.readline()
            line = line.strip("\x00")  # Encountered in Docker.
            if not line:
                await trio.sleep(0.5)
                continue
            assert line.endswith("\n"), repr(line)
            yield line


async def timer(interval: float):
    while True:
        await trio.sleep(interval)
        yield
