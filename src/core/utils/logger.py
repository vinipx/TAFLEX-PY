import logging
import allure
import sys

_logger = logging.getLogger("TAFLEX")
_logger.setLevel(logging.INFO)

# Add a default console handler only if not running inside pytest
# Pytest's log_cli handles console output for tests to prevent duplication.
if "pytest" not in sys.modules:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    _logger.addHandler(console_handler)

class Logger:
    @staticmethod
    def info(message: str, *args, **kwargs) -> None:
        _logger.info(message, *args, **kwargs)
        try:
            with allure.step(message):
                pass
        except Exception:
            pass

    @staticmethod
    def debug(message: str, *args, **kwargs) -> None:
        _logger.debug(message, *args, **kwargs)

    @staticmethod
    def warn(message: str, *args, **kwargs) -> None:
        _logger.warning(message, *args, **kwargs)

    @staticmethod
    def error(message: str, *args, **kwargs) -> None:
        _logger.error(message, *args, **kwargs)

    @staticmethod
    def screenshot(name: str, buffer: bytes) -> None:
        try:
            allure.attach(buffer, name=name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

logger = Logger()
