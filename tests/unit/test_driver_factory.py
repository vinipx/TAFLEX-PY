from src.core.drivers.driver_factory import DriverFactory
from src.core.drivers.strategies.playwright_strategy import PlaywrightDriverStrategy
from src.core.drivers.strategies.playwright_api_strategy import PlaywrightApiStrategy
from src.core.drivers.strategies.httpx_api_strategy import HttpxApiStrategy

def test_driver_factory_web(monkeypatch):
    import src.core.drivers.driver_factory as df
    
    class MockConfigManager:
        def get(self, key):
            if key == "execution_mode": return "web"
            return None

    monkeypatch.setattr(df, "config_manager", MockConfigManager())
    
    driver = DriverFactory.create()
    assert isinstance(driver, PlaywrightDriverStrategy)

def test_driver_factory_api_playwright(monkeypatch):
    import src.core.drivers.driver_factory as df

    class MockConfigManager:
        def get(self, key):
            if key == "execution_mode": return "api"
            if key == "api_provider": return "playwright"
            return None

    monkeypatch.setattr(df, "config_manager", MockConfigManager())

    driver = DriverFactory.create()
    assert isinstance(driver, PlaywrightApiStrategy)

def test_driver_factory_api_httpx(monkeypatch):
    import src.core.drivers.driver_factory as df

    class MockConfigManager:
        def get(self, key):
            if key == "execution_mode": return "api"
            if key == "api_provider": return "axios" # Tests legacy config
            return None

    monkeypatch.setattr(df, "config_manager", MockConfigManager())

    driver = DriverFactory.create()
    assert isinstance(driver, HttpxApiStrategy)
