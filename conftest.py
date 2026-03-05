import pytest
from src.config.config_manager import config_manager
from src.core.drivers.driver_factory import DriverFactory
from src.core.reporters.xray_reporter import XrayReporter

def pytest_configure(config):
    config.pluginmanager.register(XrayReporter(), "xray_reporter")

@pytest.fixture(scope="function")
def web_driver():
    driver = DriverFactory.create("web")
    driver.initialize(config_manager.config)
    yield driver
    driver.terminate()

@pytest.fixture(scope="function")
def api_driver():
    driver = DriverFactory.create("api")
    driver.initialize(config_manager.config)
    yield driver
    driver.terminate()

# A generic driver fixture that uses the EXECUTION_MODE from config
@pytest.fixture(scope="function")
def driver():
    driver = DriverFactory.create()
    driver.initialize(config_manager.config)
    yield driver
    driver.terminate()
