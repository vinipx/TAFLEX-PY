from abc import ABC, abstractmethod
from typing import Any

class UiDriver(ABC):
    """Base protocol for UI automation drivers (Web, Mobile)."""

    @abstractmethod
    def initialize(self, config: Any) -> Any:
        pass

    @abstractmethod
    def terminate(self) -> None:
        pass

    @abstractmethod
    def navigate_to(self, url: str) -> None:
        pass

    @abstractmethod
    def find_element(self, logical_name: str) -> Any:
        pass

    @abstractmethod
    def load_locators(self, page_name: str) -> None:
        pass

    @abstractmethod
    def get_execution_mode(self) -> str:
        pass

    @abstractmethod
    def capture_screenshot(self, name: str) -> bytes:
        pass
