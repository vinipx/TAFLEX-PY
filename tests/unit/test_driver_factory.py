from src.core.drivers.driver_factory import DriverFactory
from src.core.drivers.strategies.playwright_strategy import PlaywrightDriverStrategy
from src.core.drivers.strategies.playwright_api_strategy import PlaywrightApiStrategy
from src.core.drivers.strategies.httpx_api_strategy import HttpxApiStrategy
from src.config.config_manager import AppConfig

def test_driver_factory_web():
    config = AppConfig(EXECUTION_MODE="web")
    driver = DriverFactory.create(config)
    assert isinstance(driver, PlaywrightDriverStrategy)

def test_driver_factory_api_playwright():
    config = AppConfig(EXECUTION_MODE="api", API_PROVIDER="playwright")
    driver = DriverFactory.create(config)
    assert isinstance(driver, PlaywrightApiStrategy)

def test_driver_factory_api_httpx():
    config = AppConfig(EXECUTION_MODE="api", API_PROVIDER="httpx")
    driver = DriverFactory.create(config)
    assert isinstance(driver, HttpxApiStrategy)
