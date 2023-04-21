import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional


class RotatingLog:
    def __init__(self, log_file_path: str,
                 log_name: str,
                 log_level: Optional[str] = logging.INFO) -> None:
        self.logger: logging.Logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        # create a file manipulator with daily routativity
        self.handler = TimedRotatingFileHandler(
            log_file_path,
            when='D',
            backupCount=3
        )

        # format the output
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
