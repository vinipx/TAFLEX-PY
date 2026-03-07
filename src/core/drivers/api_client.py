from abc import ABC, abstractmethod
from typing import Any

class ApiClient(ABC):
    """Base protocol for API automation clients."""

    @abstractmethod
    def initialize(self, config: Any) -> Any:
        pass

    @abstractmethod
    def terminate(self) -> None:
        pass

    @abstractmethod
    def get(self, endpoint: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def post(self, endpoint: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def put(self, endpoint: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def delete(self, endpoint: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_execution_mode(self) -> str:
        pass
