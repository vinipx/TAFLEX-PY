from appium import webdriver
from appium.options.common.base import AppiumOptions
from typing import Any, Optional
from src.core.drivers.ui_driver import UiDriver
from src.core.locators.locator_manager import LocatorManager
from src.core.utils.logger import logger
from src.core.elements.mobile_element import MobileElement
from appium.webdriver.common.appiumby import AppiumBy

class AppiumMobileStrategy(UiDriver):
    """Mobile automation driver implementation using Appium."""

    def __init__(self) -> None:
        self.driver: Optional[webdriver.Remote] = None
        self.locator_manager = LocatorManager(mode="mobile")

    def initialize(self, config: Any) -> webdriver.Remote:
        # Default local Appium server
        remote_url_config = getattr(config, 'remote_url', None)
        appium_server_url = str(remote_url_config) if remote_url_config else 'http://localhost:4723'
        cloud_platform = getattr(config, 'cloud_platform', 'local')

        options = AppiumOptions()

        if cloud_platform == 'browserstack':
            appium_server_url = f"https://{getattr(config, 'cloud_user')}:{getattr(config, 'cloud_key')}@hub-cloud.browserstack.com/wd/hub"
            options.set_capability('platformName', getattr(config, 'os', 'Android'))
            options.set_capability('appium:deviceName', getattr(config, 'os_version', 'Google Pixel 7'))
        elif cloud_platform == 'saucelabs':
            appium_server_url = f"https://{getattr(config, 'cloud_user')}:{getattr(config, 'cloud_key')}@ondemand.us-west-1.saucelabs.com:443/wd/hub"
            options.set_capability('platformName', getattr(config, 'os', 'Android'))
            options.set_capability('appium:deviceName', getattr(config, 'os_version', 'Google Pixel 7'))
        else:
            options.set_capability('platformName', 'Android')
            options.set_capability('appium:automationName', 'UiAutomator2')

        logger.info(f"Initializing Appium Mobile Strategy via: {appium_server_url}")
        self.driver = webdriver.Remote(appium_server_url, options=options)
        
        self.locator_manager.load()
        return self.driver

    def terminate(self) -> None:
        if self.driver:
            self.driver.quit()

    def navigate_to(self, url: str) -> None:
        # For mobile, this might be deep linking or opening a specific app activity
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Navigating to deep link / activity: {url}")
        self.driver.get(url)

    def find_element(self, logical_name: str) -> Any:
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        selector = self.locator_manager.resolve(logical_name)
        
        if selector.startswith('//'):
            strategy = AppiumBy.XPATH
        elif selector.startswith('id='):
            strategy = AppiumBy.ID
            selector = selector[3:]
        else:
            # Default to accessibility id for mobile
            strategy = AppiumBy.ACCESSIBILITY_ID  # type: ignore[assignment]

        return MobileElement(self.driver, (strategy, selector), logical_name)

    def load_locators(self, page_name: str) -> None:
        self.locator_manager.load(page_name)

    def capture_screenshot(self, name: str) -> bytes:
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        screenshot = self.driver.get_screenshot_as_png()
        logger.screenshot(name, screenshot)
        return screenshot

    def get_execution_mode(self) -> str:
        return "mobile"
