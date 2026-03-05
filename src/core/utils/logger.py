import logging
import allure

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
_logger = logging.getLogger("TAFLEX")

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
