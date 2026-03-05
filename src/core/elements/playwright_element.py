from playwright.sync_api import Locator
from src.core.utils.logger import logger

class PlaywrightElement:
    """Playwright implementation of the unified element wrapper."""

    def __init__(self, locator: Locator, name: str) -> None:
        self.locator = locator
        self.name = name

    def click(self, **kwargs) -> None:
        logger.info(f"Clicking on: {self.name}")
        self.locator.click(**kwargs)

    def fill(self, value: str, **kwargs) -> None:
        logger.info(f"Filling {self.name} with: {value}")
        self.locator.fill(value, **kwargs)

    def type(self, value: str, **kwargs) -> None:
        logger.info(f"Typing {value} into: {self.name}")
        self.locator.type(value, **kwargs)

    def get_text(self) -> str:
        return self.locator.inner_text()

    def get_value(self) -> str:
        return self.locator.input_value()

    def is_visible(self) -> bool:
        return self.locator.is_visible()

    def is_enabled(self) -> bool:
        return self.locator.is_enabled()

    def wait_for(self, **kwargs) -> None:
        logger.info(f"Waiting for element: {self.name}")
        self.locator.wait_for(**kwargs)

    def get_attribute(self, name: str) -> str | None:
        return self.locator.get_attribute(name)
