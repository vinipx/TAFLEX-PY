from typing import Any, Optional
from playwright.sync_api import sync_playwright, APIRequestContext
from src.core.drivers.api_client import ApiClient
from src.core.utils.logger import logger

class PlaywrightApiStrategy(ApiClient):
    """API automation driver implementation using Playwright's APIRequestContext."""

    def __init__(self) -> None:
        self.playwright = None
        self.request_context: Optional[APIRequestContext] = None

    def initialize(self, config: Any) -> APIRequestContext:
        api_base_url = getattr(config, 'api_base_url', None)
        logger.info(f"Initializing Playwright API Strategy with base URL: {api_base_url}")
        
        self.playwright = sync_playwright().start()
        self.request_context = self.playwright.request.new_context(
            base_url=str(api_base_url) if api_base_url else None,
            extra_http_headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return self.request_context

    def terminate(self) -> None:
        if self.request_context:
            self.request_context.dispose()
        if self.playwright:
            self.playwright.stop()

    def get(self, endpoint: str, **kwargs) -> Any:
        if not self.request_context:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Playwright GET: {endpoint}")
        return self.request_context.get(endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Any:
        if not self.request_context:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Playwright POST: {endpoint}")
        return self.request_context.post(endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Any:
        if not self.request_context:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Playwright PUT: {endpoint}")
        return self.request_context.put(endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        if not self.request_context:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Playwright DELETE: {endpoint}")
        return self.request_context.delete(endpoint, **kwargs)

    def get_execution_mode(self) -> str:
        return "api"
