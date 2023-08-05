import typing
from collections import Counter

from .logs import LogLine
from .quantities import Quantity

Number = typing.Union[int, float]
T = typing.TypeVar("T")
V = typing.TypeVar("V")


class Metric(typing.Generic[T, V]):
    unit_suffix = ""

    def __init__(self, quantity: Quantity):
        self._quantity = quantity
        self._times: typing.List[float] = []
        self._values: typing.List[T] = []

    def ingest(self, log_line: LogLine):
        value = self._quantity.extract(log_line)
        self._times.append(log_line.time.timestamp())
        self._values.append(value)

    def get_value(self, times: typing.List[float], values: typing.List[T]) -> V:
        raise NotImplementedError

    @property
    def value(self) -> V:
        return self.get_value(self._times, self._values)

    def reset(self):
        self._times = []
        self._values = []

    @property
    def unit(self) -> str:
        return self._quantity.unit + self.unit_suffix

    @property
    def name(self) -> str:
        return f"{self._quantity.name}.{self.__class__.__name__.lower()}"

    def __str__(self) -> str:
        return self.name


class Total(Metric[Number, Number]):
    def get_value(self, times, values):
        return sum(values)


class Mean(Metric[Number, Number]):
    unit_suffix = "/req"

    def get_value(self, times, values):
        try:
            return sum(values) / len(values)
        except ZeroDivisionError:
            return 0


class Average(Metric[Number, Number]):
    unit_suffix = "/s"

    def get_value(self, times, values):
        timespan = max(times, default=0) - min(times, default=0)
        return sum(values) / timespan if timespan else 0


class Count(Metric[typing.Any, typing.List[dict]]):
    def __init__(self, quantity: Quantity, limit: int = 5):
        super().__init__(quantity)
        self.limit = limit

    def get_value(self, times, values):
        top_items = Counter(values).most_common(self.limit)
        return [{"key": key, "count": count} for key, count in top_items]


def build_report(metrics: typing.List[Metric]) -> dict:
    return {
        metric.name: {"unit": metric.unit, "value": metric.value}
        for metric in metrics
    }
