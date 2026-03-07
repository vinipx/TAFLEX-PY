import json
from urllib.parse import quote
from typing import Any, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Locator, Playwright
from src.core.drivers.ui_driver import UiDriver
from src.core.locators.locator_manager import LocatorManager
from src.core.utils.logger import logger

class PlaywrightDriverStrategy(UiDriver):
    """Web automation driver implementation using Playwright."""

    def __init__(self) -> None:
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.locator_manager = LocatorManager(mode="web")

    def initialize(self, config: Any) -> Page:
        browser_name = getattr(config, 'browser', 'chromium')
        headless = getattr(config, 'headless', True)
        cloud_platform = getattr(config, 'cloud_platform', 'local')

        self.playwright = sync_playwright().start()
        engine = getattr(self.playwright, browser_name)

        if cloud_platform == 'local':
            self.browser = engine.launch(headless=headless)
        else:
            # Simplified cloud integration for Python mock-up
            caps = {
                'browser': browser_name,
                'browser_version': getattr(config, 'browser_version', 'latest'),
                'os': getattr(config, 'os', 'Windows'),
                'os_version': getattr(config, 'os_version', '10')
            }
            ws_endpoint = ""
            if cloud_platform == 'browserstack':
                ws_endpoint = f"wss://cdp.browserstack.com/playwright?caps={quote(json.dumps(caps))}"
            elif cloud_platform == 'saucelabs':
                ws_endpoint = f"wss://ondemand.us-west-1.saucelabs.com/playwright/test?caps={quote(json.dumps(caps))}"
            
            if ws_endpoint:
                self.browser = engine.connect(ws_endpoint)
            else:
                raise ValueError("Unsupported cloud platform or missing configuration.")

        if not self.browser:
            raise RuntimeError("Failed to initialize browser")

        self.context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        self.page = self.context.new_page()

        self.locator_manager.load()

        return self.page

    def navigate_to(self, url: str) -> None:
        if not self.page:
            raise RuntimeError("Driver not initialized")
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def find_element(self, logical_name: str) -> Locator:
        if not self.page:
            raise RuntimeError("Driver not initialized")
        selector = self.locator_manager.resolve(logical_name)
        locator = self.page.locator(selector)
        return locator

    def load_locators(self, page_name: str) -> None:
        self.locator_manager.load(page_name)

    def terminate(self) -> None:
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def capture_screenshot(self, name: str) -> bytes:
        if not self.page:
            raise RuntimeError("Driver not initialized")
        screenshot = self.page.screenshot(full_page=True)
        logger.screenshot(name, screenshot)
        return screenshot

    def get_execution_mode(self) -> str:
        return "web"
