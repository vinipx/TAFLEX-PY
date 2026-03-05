from abc import ABC, abstractmethod
from typing import Any

class AutomationDriver(ABC):
    """Base class for all automation drivers in the TAFLEX framework."""
    
    @abstractmethod
    def initialize(self, config: Any) -> Any:
        """Initializes the driver with the provided configuration."""
        pass

    @abstractmethod
    def terminate(self) -> None:
        """Terminates the driver session and performs cleanup."""
        pass

    @abstractmethod
    def navigate_to(self, url: str) -> None:
        """Navigates to a specific URL or activity."""
        pass

    @abstractmethod
    def find_element(self, logical_name: str) -> Any:
        """Finds an element using its logical name resolved through the LocatorManager."""
        pass

    @abstractmethod
    def load_locators(self, page_name: str) -> None:
        """Loads locators for a specific page or feature."""
        pass

    @abstractmethod
    def get_execution_mode(self) -> str:
        """Gets the current execution mode of the driver."""
        pass

    @abstractmethod
    def capture_screenshot(self, name: str) -> bytes:
        """Captures a screenshot."""
        pass
