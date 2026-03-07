import pytest
from src.config.config_manager import AppConfig
from src.core.drivers.driver_factory import DriverFactory
from src.core.reporters.xray_reporter import XrayReporter

@pytest.fixture(scope="session")
def app_config():
    return AppConfig()

def pytest_configure(config):
    app_config = AppConfig()
    config.pluginmanager.register(XrayReporter(app_config), "xray_reporter")
    
    if 'reportportal' in app_config.reporters:
        # Dynamically enable reportportal
        setattr(config.option, "rp_enabled", True)
        if app_config.rp_endpoint:
            setattr(config.option, "rp_endpoint", str(app_config.rp_endpoint))
        if app_config.rp_api_key:
            setattr(config.option, "rp_api_key", app_config.rp_api_key)
        if app_config.rp_project:
            setattr(config.option, "rp_project", app_config.rp_project)
        if app_config.rp_launch:
            setattr(config.option, "rp_launch", app_config.rp_launch)

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
