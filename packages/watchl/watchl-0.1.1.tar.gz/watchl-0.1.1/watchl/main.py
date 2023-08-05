import asyncio
import logging
import os
import signal
import typing
from datetime import timedelta

import click

from . import defaults
from .config import LOG_LEVELS, Config
from .models.alerts import Alert
from .models.logs import LogLine
from .models.metrics import Average, Count, Mean, Metric, Total, build_report
from .models.quantities import requests, sections, transfer
from .utils import Background, async_tail, timer

HANDLED_SIGNALS = (
    signal.SIGINT,  # Sent by Ctrl+C
    signal.SIGTERM,  # Sent by `kill <pid>`
)


@click.command()
@click.option(
    "-f",
    "path",
    type=click.Path(exists=True),
    default=defaults.LOG_PATH,
    help="Path to an actively written-to log file.",
    show_default=True,
)
@click.option(
    "--report-every",
    type=float,
    default=defaults.REPORT_TICK,
    show_default=True,
    help="Number of seconds between stats reports.",
)
@click.option(
    "--sections-top",
    type=int,
    default=defaults.REPORT_SECTIONS_TOP,
    show_default=True,
    help="Number of most hit website sections to display in the report.",
)
@click.option(
    "--traffic-threshold",
    type=float,
    default=defaults.ALERT_TRAFFIC_THRESHOLD,
    show_default=True,
)
@click.option(
    "--traffic-up",
    type=float,
    default=defaults.ALERT_TRAFFIC_UP,
    show_default=True,
    help=(
        "Number of seconds to trigger an alert "
        "after traffic exceeded the threshold."
    ),
)
@click.option(
    "--traffic-down",
    type=float,
    default=defaults.ALERT_TRAFFIC_DOWN,
    show_default=True,
    help=(
        "Number of seconds to stop an alert "
        "after traffic dropped below the threshold."
    ),
)
@click.option(
    "--alert-tick",
    type=float,
    default=defaults.ALERT_TICK,
    show_default=True,
    help=(
        "Number of seconds between evaluation of stats for alerting purposes."
    ),
)
@click.option(
    "--tick",
    type=float,
    default=defaults.MONITOR_TICK,
    show_default=True,
    help=(
        "Number of seconds between system event checks. "
        "Note: lower values increase CPU usage."
    ),
)
@click.option(
    "--log-level",
    type=click.Choice(LOG_LEVELS.keys()),
    default=defaults.MONITOR_LOG_LEVEL,
    show_default=True,
    help="Level for internal log messages",
)
@click.option(
    "--limit-max-log-lines",
    type=int,
    default=defaults.MONITOR_LIMIT_MAX_LOG_LINES,
    help=(
        "Limit the number of log lines to ingest "
        "before terminating the process."
    ),
)
def main(
    path: str,
    sections_top: int,
    report_every: float,
    traffic_threshold: float,
    traffic_up: float,
    traffic_down: float,
    alert_tick: float,
    tick: float,
    log_level: str,
    limit_max_log_lines: typing.Optional[int],
):
    config = Config(
        path=path,
        report_tick=report_every,
        alert_tick=alert_tick,
        tick=tick,
        log_level=log_level,
        limit_max_log_lines=limit_max_log_lines,
    )

    monitor = Monitor(
        config=config,
        metrics=[
            Count(sections, limit=sections_top),
            Total(requests),
            Average(requests),
            Average(transfer),
            Mean(transfer),
        ],
        alerts=[
            Alert(
                metric=Average(requests),
                threshold=traffic_threshold,
                up=timedelta(seconds=traffic_up),
                down=timedelta(seconds=traffic_down),
            )
        ],
    )

    monitor.run()


class Monitor:
    def __init__(
        self,
        config: Config,
        metrics: typing.List[Metric] = None,
        alerts: typing.List[Alert] = None,
    ):
        self._config = config
        self._metrics = metrics or []
        self._alerts = alerts or []
        self._total_log_lines = 0
        self._should_exit = False

    @property
    def logger(self) -> logging.Logger:
        return self._config.logger

    def install_signal_handlers(self):
        loop = asyncio.get_event_loop()
        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, self._handle_exit, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self._handle_exit)

    def _handle_exit(self, *_):
        self._should_exit = True

    def _background_tasks(self) -> Background:
        background = Background()

        @background.task
        async def process_logs():
            self.logger.info("watching logs", extra={"path": self._config.path})

            async for line in async_tail(self._config.path):
                try:
                    log_line = LogLine.parse(line)
                except ValueError as exc:
                    self.logger.error(
                        "parsing failed",
                        extra={"raw": line, "exception": str(exc)},
                    )
                else:
                    for metric in self._metrics:
                        metric.push(log_line)
                    for alert in self._alerts:
                        alert.metric.push(log_line)
                finally:
                    self._total_log_lines += 1

        @background.task
        async def update_alerts():
            tick = self._config.alert_tick

            self.logger.debug(
                "alerting task started",
                extra={
                    "tick": tick,
                    "alerts": [
                        {
                            "metric": str(alert.metric),
                            "threshold": alert.threshold,
                        }
                        for alert in self._alerts
                    ],
                },
            )

            async for _ in timer(tick):
                for alert in self._alerts:
                    try:
                        alert.update()
                    except Alert.StatusChanged as exc:
                        self.logger.warning(
                            "alert status changed",
                            extra={**exc.change, **alert.identification},
                        )
                self.logger.debug(
                    "alerts updated",
                    extra={"alerts": alert.status for alert in self._alerts},
                )

        @background.task
        async def report():
            tick = self._config.report_tick

            self.logger.debug(
                "reporting task started",
                extra={
                    "tick": tick,
                    "metrics": [str(metric) for metric in self._metrics],
                },
            )

            async for _ in timer(tick):
                report = build_report(self._metrics)
                self.logger.info(
                    f"activity in the past {tick} seconds", extra=dict(report)
                )
                self.logger.debug(
                    "activity detail",
                    extra={"total_log_lines": self._total_log_lines},
                )
                for metric in self._metrics:
                    metric.reset()

        return background

    async def main(self):
        self.logger.info("process started", extra={"pid": os.getpid()})

        self.install_signal_handlers()

        async with self._background_tasks() as background:
            async for _ in timer(self._config.tick):
                await background.check_for_exceptions()
                if self._should_exit:
                    break
                if self._config.limit_max_log_lines is None:
                    continue
                if self._total_log_lines >= self._config.limit_max_log_lines:
                    break

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
