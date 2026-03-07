import pytest
from src.config.config_manager import AppConfig
from src.core.drivers.driver_factory import DriverFactory
from src.core.reporters.xray_reporter import XrayReporter

@pytest.fixture(scope="session")
def app_config():
    return AppConfig()

def pytest_configure(config):
    # Retrieve config inside plugin register if needed, or register plugin when testing session starts
    # XrayReporter needs config. We can pass app_config to XrayReporter if possible, but XrayReporter is registered here.
    # We might need to initialize it with AppConfig().
    app_config = AppConfig()
    config.pluginmanager.register(XrayReporter(app_config), "xray_reporter")

@pytest.fixture(scope="function")
def web_driver(app_config):
    # Override config for web
    config = app_config.model_copy(update={'execution_mode': 'web'})
    driver = DriverFactory.create(config)
    driver.initialize(config)
    yield driver
    driver.terminate()

@pytest.fixture(scope="function")
def api_driver(app_config):
    # Override config for api
    config = app_config.model_copy(update={'execution_mode': 'api'})
    driver = DriverFactory.create(config)
    driver.initialize(config)
    yield driver
    driver.terminate()

# A generic driver fixture that uses the EXECUTION_MODE from config
@pytest.fixture(scope="function")
def driver(app_config):
    driver = DriverFactory.create(app_config)
    driver.initialize(app_config)
    yield driver
    driver.terminate()

@pytest.fixture(scope="function")
def mobile_driver(app_config):
    config = app_config.model_copy(update={'execution_mode': 'mobile', 'os': 'Android'})
    
    driver = DriverFactory.create(config)
    driver.initialize(config)
    # Appium standard way to start an app if not provided in caps
    driver.driver.execute_script('mobile: startActivity', {
        'component': 'com.android.settings/.Settings',
        'appPackage': 'com.android.settings'
    })
    yield driver
    driver.terminate()
