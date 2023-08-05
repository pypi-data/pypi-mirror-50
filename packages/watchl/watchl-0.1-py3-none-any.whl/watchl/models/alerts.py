"""Alerting implementation based on a finite state machine (FSM).

An alert is attached to a metric, and has two main states:
idle ("low") and active ("high").

In-between states (activating, recovering) are used to implement a simple
hysteresis mechanism, with delays for going up (idle -> active) and
down (active -> idle).
"""

import typing
from datetime import datetime, timedelta

from .metrics import Metric


class Context(typing.NamedTuple):
    """Data reused from one state to another."""

    metric: Metric
    threshold: float
    enter_time: datetime
    up: timedelta
    down: timedelta
    on_status_changed: typing.Callable[
        ["State", "State", typing.Optional[str]], None
    ]


class State:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.value: typing.Union[int, float] = 0

    def to(
        self, state_cls: typing.Type["State"], reason: str = None
    ) -> "State":
        new_state = state_cls(ctx=self.ctx._replace(enter_time=datetime.now()))
        self.ctx.on_status_changed(self, new_state, reason)
        return new_state

    def __next__(self) -> "State":
        raise NotImplementedError

    def __str__(self) -> str:
        return type(self).__name__.lower()


class Idle(State):
    def __next__(self) -> State:
        if self.value < self.ctx.threshold:
            return self
        if self.ctx.up.total_seconds():
            return self.to(Activating, reason="above threshold")
        return self.to(Active, reason="above threshold")


class Activating(State):
    def __next__(self) -> State:
        if self.value < self.ctx.threshold:
            return self.to(Idle, reason="below threshold")

        if datetime.now() - self.ctx.enter_time < self.ctx.up:
            return self

        return self.to(
            Active, reason="stayed above threshold for longer than up delay"
        )


class Active(State):
    def __next__(self) -> State:
        if self.value >= self.ctx.threshold:
            return self
        if self.ctx.down.total_seconds():
            return self.to(Recovering, "below threshold")
        return self.to(Idle, reason="below threshold")


class Recovering(State):
    def __next__(self) -> State:
        if self.value >= self.ctx.threshold:
            return self.to(Active)

        if datetime.now() - self.ctx.enter_time < self.ctx.down:
            return self

        return self.to(
            Idle, reason="stayed below threshold for longer than down delay"
        )


class AlertStatusChanged(Exception):
    def __init__(self, change: dict):
        super().__init__()
        self.change = change


class Alert:
    StatusChanged = AlertStatusChanged

    def __init__(
        self, metric: Metric, threshold: float, up: timedelta, down: timedelta
    ):
        self.metric = metric
        ctx = Context(
            metric=metric,
            threshold=threshold,
            enter_time=datetime.now(),
            up=up,
            down=down,
            on_status_changed=self.on_status_changed,
        )
        self.state = Idle(ctx)
        self._change: typing.Optional[dict] = None

    def on_status_changed(
        self, state: State, new_state: State, reason: typing.Optional[str]
    ):
        if not isinstance(new_state, (Idle, Active)):
            return

        self._change = dict(
            status=str(new_state),
            previous_status=str(state),
            value=state.value,
            reason=reason,
        )

    def update(self):
        self._change = None
        self.state.value = self.metric.value
        self.metric.reset()
        self.state = next(self.state)
        if self._change is not None:
            raise AlertStatusChanged(self._change)

    @property
    def identification(self) -> dict:
        return {
            "metric": str(self.metric),
            "threshold": self.threshold,
            "up": str(self.state.ctx.up),
            "down": str(self.state.ctx.down),
        }

    @property
    def status(self) -> dict:
        return {
            **self.identification,
            "value": self.state.value,
            "state": str(self.state),
        }

    @property
    def threshold(self) -> float:
        return self.state.ctx.threshold
