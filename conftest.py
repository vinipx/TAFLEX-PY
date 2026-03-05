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

@pytest.fixture(scope="function")
def mobile_driver():
    # Force mobile mode for locator loading
    import os
    os.environ["EXECUTION_MODE"] = "mobile"
    from src.config.config_manager import AppConfig
    config_manager.config = AppConfig() # Reload config with mobile mode
    
    driver = DriverFactory.create("mobile")
    # Tell appium to open the native settings app on the plugged in Android device
    config_manager.config.os = 'Android'
    driver.initialize(config_manager.config)
    # Appium standard way to start an app if not provided in caps
    driver.driver.execute_script('mobile: startActivity', {
        'component': 'com.android.settings/.Settings',
        'appPackage': 'com.android.settings'
    })
    yield driver
    driver.terminate()
