import typing

from .logs import LogLine


class Quantity(typing.NamedTuple):
    name: str
    extract: typing.Callable[[LogLine], typing.Any]
    unit: str


# Built-in quantities.
requests = Quantity("requests", extract=lambda log: 1, unit="req")
transfer = Quantity("transfer", extract=lambda log: log.size, unit="bytes")
sections = Quantity(
    "sections", extract=lambda log: log.request.section, unit="hits"
)
