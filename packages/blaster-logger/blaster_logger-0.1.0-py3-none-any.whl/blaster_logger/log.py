import logging
import time

import attr
from decorator import decorator
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info, ansi=True)
        logger_opt.log(
            record.levelname, f"[{record.name}] {record.getMessage()} [{record.module}]"
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)


@attr.s(auto_attribs=True)
class Log:
    DEBUG = "DEBUG"
    INFO = "INFO"
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @staticmethod
    @decorator
    def this(func, *args, **kwargs):
        logger.log("DEBUG", f"Entering: {func.__name__} [{func.__module__}]")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        if execution_time > 3:
            if execution_time < 10:
                logger.warning(
                    f"Long execution time: {execution_time} [{func.__module__}.{func.__name__}]"
                )
            else:
                logger.critical(
                    f"Extra long execution time: {execution_time} [{func.__module__}.{func.__name__}]"
                )
        else:
            logger.log(
                "DEBUG",
                f"Execution time: {execution_time} [{func.__module__}.{func.__name__}]",
            )
        logger.log("DEBUG", f"Result: {result} [{func.__module__}.{func.__name__}]")
        logger.log("DEBUG", f"Exiting: {func.__name__} [{func.__module__}]")
        return result

    def __call__(self, message: str, level: str = "DEBUG"):
        return logger.log(level.upper(), message)

    def info(self, message):
        return self(message, self.INFO)

    def debug(self, message):
        return self(message, self.DEBUG)

    def critical(self, message):
        return self(message, self.CRITICAL)

    def warning(self, message):
        return self(message, self.WARNING)

    def error(self, message):
        return self(message, self.ERROR)

    @staticmethod
    def trace(e):
        return logger.trace(e)


log = Log()
