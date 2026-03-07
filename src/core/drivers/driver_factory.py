from typing import Optional, Union
from src.config.config_manager import AppConfig
from src.core.drivers.ui_driver import UiDriver
from src.core.drivers.api_client import ApiClient
from src.core.drivers.strategies.playwright_strategy import PlaywrightDriverStrategy
from src.core.drivers.strategies.playwright_api_strategy import PlaywrightApiStrategy
from src.core.drivers.strategies.httpx_api_strategy import HttpxApiStrategy

class DriverFactory:
    """Factory class for instantiating the correct driver strategy."""

    @staticmethod
    def create(config: AppConfig) -> Union[UiDriver, ApiClient]:
        mode = config.execution_mode

        if mode == 'web':
            return PlaywrightDriverStrategy()
        elif mode == 'api':
            provider = config.api_provider
            if provider == 'httpx':
                return HttpxApiStrategy()
            else:
                return PlaywrightApiStrategy()
        elif mode == 'mobile':
            from src.core.drivers.strategies.appium_mobile_strategy import AppiumMobileStrategy
            return AppiumMobileStrategy()
        else:
            raise ValueError(f"Unsupported execution mode: {mode}")
