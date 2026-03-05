from typing import Optional
from src.config.config_manager import config_manager
from src.core.drivers.automation_driver import AutomationDriver
from src.core.drivers.strategies.playwright_strategy import PlaywrightDriverStrategy
from src.core.drivers.strategies.playwright_api_strategy import PlaywrightApiStrategy
from src.core.drivers.strategies.httpx_api_strategy import HttpxApiStrategy

class DriverFactory:
    """Factory class for instantiating the correct AutomationDriver strategy."""

    @staticmethod
    def create(overridden_mode: Optional[str] = None) -> AutomationDriver:
        mode = overridden_mode or config_manager.get('execution_mode')

        if mode == 'web':
            return PlaywrightDriverStrategy()
        elif mode == 'api':
            provider = config_manager.get('api_provider')
            if provider == 'axios' or provider == 'httpx':
                return HttpxApiStrategy()
            else:
                return PlaywrightApiStrategy()
        elif mode == 'mobile':
            # Placeholder for WebdriverioMobileStrategy translation
            # Assuming Appium is used for Python
            raise NotImplementedError("Mobile strategy is not fully implemented yet in Python stack.")
        else:
            raise ValueError(f"Unsupported execution mode: {mode}")
