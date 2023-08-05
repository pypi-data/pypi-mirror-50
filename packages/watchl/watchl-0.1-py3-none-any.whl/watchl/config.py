import logging
import typing
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger

from . import defaults

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARN,
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
}


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self, log_record: dict, record: logging.LogRecord, message_dict: dict
    ):
        super().add_fields(log_record, record, message_dict)
        created = datetime.utcfromtimestamp(record.created)
        log_record["timestamp"] = created.isoformat()


def get_logger(log_level: typing.Union[int, str]) -> logging.Logger:
    if isinstance(log_level, str):
        log_level = LOG_LEVELS[log_level]

    logger = logging.getLogger("watchl")

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter("(levelname) (message) (timestamp)"))
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


class Config:
    def __init__(
        self,
        path: str = defaults.LOG_PATH,
        report_tick: float = defaults.REPORT_TICK,
        alert_tick: float = defaults.ALERT_TICK,
        tick: float = defaults.MONITOR_TICK,
        log_level: str = defaults.MONITOR_LOG_LEVEL,
        limit_max_log_lines: typing.Optional[
            int
        ] = defaults.MONITOR_LIMIT_MAX_LOG_LINES,
    ):
        self.path = path
        self.report_tick = report_tick
        self.alert_tick = alert_tick
        self.tick = tick
        self.limit_max_log_lines = limit_max_log_lines
        self.log_level = log_level
        self.logger = get_logger(self.log_level)
