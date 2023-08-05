"""Parsing of W3C-formatted logs (Common Log Format).

See: https://www.w3.org/Daemon/User/Config/Logging.html#common-logfile-format
"""

import re
import typing
from datetime import datetime

LOG_DATETIME_FORMAT = "%d/%b/%Y:%H:%M:%S +0000"

_COMMON_LOGFILE_REGEX = re.compile(
    r"^(?P<host>.*?)"
    r"\s"
    r"(?P<logname>\S+)"
    r"\s"
    r"(?P<user>\S+)"
    r"\s"
    r"\[(?P<time>.*?)\]"
    r"\s"
    r"\"(?P<request>.*?)\""
    r"\s"
    r"(?P<status>\d{3})"
    r"\s"
    r"(?P<size>\S+)"
)

_REQUEST_REGEX = re.compile(
    r"^(?P<method>\w+)\s(?P<path>\S+)\sHTTP/(?P<http_version>[\w\.]+)"
)
_PATH_SECTION_REGEX = re.compile(r"^(?P<section>/\S?[^/]*)")


def _match_or_error(
    pattern: typing.Pattern, value: str, exception=ValueError
) -> dict:
    match = pattern.match(value)
    if match is None:
        raise exception(f"'{value}' did not match pattern '{pattern.pattern}'")
    return match.groupdict()


class Request(typing.NamedTuple):
    method: str
    path: str
    http_version: str
    section: str

    @classmethod
    def parse(cls, value: str) -> "Request":
        kwargs = _match_or_error(_REQUEST_REGEX, value)
        path = kwargs["path"]
        section = _match_or_error(_PATH_SECTION_REGEX, path)["section"]
        kwargs["section"] = section
        return cls(**kwargs)

    def __str__(self):
        return f"{self.method} {self.path} HTTP/{self.http_version}"


class LogLine(typing.NamedTuple):
    host: str
    logname: str
    user: str
    time: datetime
    request: Request
    status: int
    size: int

    @classmethod
    def parse(cls, value: str) -> "LogLine":
        kwargs = _match_or_error(_COMMON_LOGFILE_REGEX, value)

        time = datetime.strptime(kwargs.pop("time"), LOG_DATETIME_FORMAT)

        size = kwargs.pop("size")
        try:
            size = int(size)
        except ValueError:
            if size == "-":
                size = 0
            else:
                raise

        kwargs = dict(
            kwargs,
            request=Request.parse(kwargs.pop("request")),
            status=int(kwargs.pop("status")),
            size=size,
            time=time,
        )

        return cls(**kwargs)

    def __str__(self) -> str:
        time = self.time.strftime(LOG_DATETIME_FORMAT)
        return (
            f"{self.host} {self.logname} {self.user} [{time}] "
            f'"{self.request}" {self.status} {self.size}'
        )
