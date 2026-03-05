import httpx
from typing import Any, Optional
from src.core.drivers.automation_driver import AutomationDriver
from src.core.locators.locator_manager import locator_manager
from src.core.utils.logger import logger

class HttpxApiStrategy(AutomationDriver):
    """API automation driver implementation using Httpx (replacing Axios)."""

    def __init__(self) -> None:
        self.client: Optional[httpx.Client] = None

    def initialize(self, config: Any) -> httpx.Client:
        api_base_url = getattr(config, 'api_base_url', None)
        timeout = getattr(config, 'timeout', 30000) / 1000.0  # httpx takes seconds
        
        logger.info(f"Initializing HTTPX API Strategy with base URL: {api_base_url}")

        self.client = httpx.Client(
            base_url=str(api_base_url) if api_base_url else "",
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return self.client

    def terminate(self) -> None:
        if self.client:
            self.client.close()
            self.client = None

    def navigate_to(self, url: str) -> None:
        pass

    def find_element(self, logical_name: str) -> Any:
        raise NotImplementedError("find_element() is not applicable for API strategy")

    def load_locators(self, page_name: str) -> None:
        locator_manager.load(page_name)

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        if not self.client:
            raise RuntimeError("Driver not initialized")
        logger.info(f"HTTPX GET: {endpoint}")
        return self.client.get(endpoint, **kwargs)

    def post(self, endpoint: str, json: Any = None, data: Any = None, **kwargs) -> httpx.Response:
        if not self.client:
            raise RuntimeError("Driver not initialized")
        logger.info(f"HTTPX POST: {endpoint}")
        return self.client.post(endpoint, json=json, data=data, **kwargs)

    def put(self, endpoint: str, json: Any = None, data: Any = None, **kwargs) -> httpx.Response:
        if not self.client:
            raise RuntimeError("Driver not initialized")
        logger.info(f"HTTPX PUT: {endpoint}")
        return self.client.put(endpoint, json=json, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        if not self.client:
            raise RuntimeError("Driver not initialized")
        logger.info(f"HTTPX DELETE: {endpoint}")
        return self.client.delete(endpoint, **kwargs)

    def get_execution_mode(self) -> str:
        return "api"

    def capture_screenshot(self, name: str) -> bytes:
        raise NotImplementedError("capture_screenshot() is not applicable for API strategy")
