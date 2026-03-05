from typing import Any
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.core.utils.logger import logger

class MobileElement:
    """Appium implementation of the unified element wrapper."""

    def __init__(self, element: WebElement, driver: Any, locator_tuple: tuple[str, str], name: str) -> None:
        self.element = element
        self.driver = driver
        self.locator_tuple = locator_tuple
        self.name = name

    def click(self, **kwargs) -> None:
        logger.info(f"Clicking on: {self.name}")
        self.element.click()

    def fill(self, value: str, **kwargs) -> None:
        logger.info(f"Filling {self.name} with: {value}")
        self.element.clear()
        self.element.send_keys(value)

    def type(self, value: str, **kwargs) -> None:
        logger.info(f"Typing {value} into: {self.name}")
        self.element.send_keys(value)

    def get_text(self) -> str:
        return self.element.text

    def get_value(self) -> str:
        return self.element.get_attribute("value") or ""

    def is_visible(self) -> bool:
        return self.element.is_displayed()

    def is_enabled(self) -> bool:
        return self.element.is_enabled()

    def wait_for(self, timeout: int = 10, **kwargs) -> None:
        logger.info(f"Waiting for element: {self.name}")
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(self.locator_tuple))

    def get_attribute(self, name: str) -> str | None:
        return self.element.get_attribute(name)
