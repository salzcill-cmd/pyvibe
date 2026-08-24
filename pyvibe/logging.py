"""
PyVibe Logging — comprehensive logging with levels, formatters, and handlers.

Usage:
    from pyvibe.logging import get_logger, setup_logging

    # Quick setup
    setup_logging(level="DEBUG", file="app.log")

    # Get logger
    logger = get_logger("my-module")
    logger.info("Server started")
    logger.error("Something went wrong")
"""

from __future__ import annotations
import os
import time
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ==================== Log Levels ====================

class LogLevel:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    NAMES = {
        10: "DEBUG",
        20: "INFO",
        30: "WARNING",
        40: "ERROR",
        50: "CRITICAL",
    }

    COLORS = {
        10: "\033[90m",    # Gray
        20: "\033[92m",    # Green
        30: "\033[93m",    # Yellow
        40: "\033[91m",    # Red
        50: "\033[95m",    # Magenta
    }

    RESET = "\033[0m"


# ==================== Log Record ====================

@dataclass
class LogRecord:
    """Single log record."""
    level: int
    message: str
    module: str = ""
    timestamp: float = field(default_factory=time.time)
    data: Optional[Dict] = None
    exc_info: Optional[str] = None

    @property
    def level_name(self) -> str:
        return LogLevel.NAMES.get(self.level, "UNKNOWN")

    @property
    def formatted_time(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level_name,
            "message": self.message,
            "module": self.module,
            "timestamp": self.formatted_time,
            "data": self.data,
        }


# ==================== Formatters ====================

class Formatter:
    """Log formatter."""

    def format(self, record: LogRecord) -> str:
        raise NotImplementedError


class TextFormatter(Formatter):
    """Plain text formatter."""

    def __init__(self, format_str: str = "%(asctime)s [%(levelname)s] %(module)s: %(message)s"):
        self.format_str = format_str

    def format(self, record: LogRecord) -> str:
        return self.format_str % {
            "asctime": record.formatted_time,
            "levelname": record.level_name,
            "module": record.module or "-",
            "message": record.message,
        }


class ColoredFormatter(Formatter):
    """Colored console formatter."""

    def format(self, record: LogRecord) -> str:
        color = LogLevel.COLORS.get(record.level, "")
        reset = LogLevel.RESET
        return f"{color}{record.formatted_time} [{record.level_name}]{reset} {record.module or '-'}: {record.message}"


class JsonFormatter(Formatter):
    """JSON formatter."""

    def format(self, record: LogRecord) -> str:
        return json.dumps(record.to_dict())


# ==================== Handlers ====================

class Handler:
    """Base log handler."""

    def __init__(self, formatter: Optional[Formatter] = None, level: int = LogLevel.DEBUG):
        self.formatter = formatter or TextFormatter()
        self.level = level

    def emit(self, record: LogRecord) -> None:
        raise NotImplementedError


class ConsoleHandler(Handler):
    """Console output handler."""

    def __init__(self, colored: bool = True, **kwargs):
        formatter = ColoredFormatter() if colored else TextFormatter()
        super().__init__(formatter=formatter, **kwargs)

    def emit(self, record: LogRecord) -> None:
        if record.level >= self.level:
            print(self.formatter.format(record))


class FileHandler(Handler):
    """File output handler."""

    def __init__(self, filepath: str, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)

    def emit(self, record: LogRecord) -> None:
        if record.level >= self.level:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(self.formatter.format(record) + "\n")


class JsonFileHandler(Handler):
    """JSON file output handler."""

    def __init__(self, filepath: str, **kwargs):
        super().__init__(formatter=JsonFormatter(), **kwargs)
        self.filepath = filepath

    def emit(self, record: LogRecord) -> None:
        if record.level >= self.level:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(self.formatter.format(record) + "\n")


# ==================== Logger ====================

class Logger:
    """
    Logger instance.
    
    Usage:
        logger = Logger("my-module")
        logger.info("Server started")
        logger.error("Error occurred", data={"code": 500})
    """

    def __init__(self, name: str = "", level: int = LogLevel.DEBUG):
        self.name = name
        self.level = level
        self.handlers: List[Handler] = []
        self._history: List[LogRecord] = []

    def add_handler(self, handler: Handler) -> Logger:
        """Add a handler."""
        self.handlers.append(handler)
        return self

    def remove_handler(self, handler: Handler) -> Logger:
        """Remove a handler."""
        if handler in self.handlers:
            self.handlers.remove(handler)
        return self

    def set_level(self, level: int) -> Logger:
        """Set log level."""
        self.level = level
        return self

    def _log(self, level: int, message: str, data: Optional[Dict] = None, exc_info: Optional[str] = None) -> None:
        if level < self.level:
            return

        record = LogRecord(
            level=level,
            message=message,
            module=self.name,
            data=data,
            exc_info=exc_info,
        )

        self._history.append(record)
        if len(self._history) > 1000:
            self._history.pop(0)

        for handler in self.handlers:
            try:
                handler.emit(record)
            except Exception:
                pass

    def debug(self, message: str, data: Optional[Dict] = None) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, data)

    def info(self, message: str, data: Optional[Dict] = None) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, data)

    def warning(self, message: str, data: Optional[Dict] = None) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, data)

    def error(self, message: str, data: Optional[Dict] = None, exc_info: Optional[str] = None) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, data, exc_info)

    def critical(self, message: str, data: Optional[Dict] = None) -> None:
        """Log critical message."""
        self._log(LogLevel.CRITICAL, message, data)

    def exception(self, message: str, exc: Exception) -> None:
        """Log exception."""
        self._log(LogLevel.ERROR, message, exc_info=str(exc))

    def get_history(self, level: Optional[int] = None) -> List[LogRecord]:
        """Get log history."""
        if level:
            return [r for r in self._history if r.level >= level]
        return list(self._history)

    def clear_history(self) -> None:
        """Clear log history."""
        self._history.clear()


# ==================== Global Logger ====================

_global_handlers: List[Handler] = [ConsoleHandler(colored=True)]
_global_level: int = LogLevel.DEBUG
_loggers: Dict[str, Logger] = {}


def setup_logging(
    level: str = "DEBUG",
    file: Optional[str] = None,
    json_file: Optional[str] = None,
    colored: bool = True,
) -> None:
    """
    Setup global logging.
    
    Usage:
        setup_logging(level="DEBUG", file="app.log")
    """
    global _global_handlers, _global_level

    level_num = getattr(LogLevel, level.upper(), LogLevel.DEBUG)
    _global_level = level_num

    _global_handlers = [ConsoleHandler(colored=colored, level=level_num)]

    if file:
        _global_handlers.append(FileHandler(file, level=level_num))

    if json_file:
        _global_handlers.append(JsonFileHandler(json_file, level=level_num))


def get_logger(name: str = "", level: Optional[int] = None) -> Logger:
    """
    Get or create logger.
    
    Usage:
        logger = get_logger("my-module")
        logger.info("Hello")
    """
    if name not in _loggers:
        logger = Logger(name, level=level or _global_level)
        for handler in _global_handlers:
            logger.add_handler(handler)
        _loggers[name] = logger

    return _loggers[name]
