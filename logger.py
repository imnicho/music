r"""Structured logging with rotation to %APPDATA%\OctaveLights\logs\app.log."""

import logging
import logging.handlers
import os
from pathlib import Path


class Logger:
    def __init__(self):
        """Initialize logger with rotation."""
        self.app_data = Path(os.getenv("APPDATA")) / "OctaveLights" / "logs"
        self.app_data.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("OctaveLights")
        self.logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            self.app_data / "app.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
