import pytest
from unittest.mock import Mock, patch
from selenium.webdriver.common.by import By
from src.core.drivers.strategies.appium_mobile_strategy import AppiumMobileStrategy

@pytest.fixture
def mobile_strategy():
    return AppiumMobileStrategy()

@patch('src.core.drivers.strategies.appium_mobile_strategy.webdriver.Remote')
@patch('src.core.drivers.strategies.appium_mobile_strategy.locator_manager')
def test_initialize_local_appium(mock_locator_manager, mock_remote, mobile_strategy):
    mock_config = Mock()
    mock_config.remote_url = 'http://localhost:4723'
    mock_config.cloud_platform = 'local'

    driver = mobile_strategy.initialize(mock_config)

    mock_remote.assert_called_once()
    args, kwargs = mock_remote.call_args
    assert args[0] == 'http://localhost:4723'
    options = kwargs['options']
    assert options.get_capability('platformName') == 'Android'
    assert options.get_capability('appium:automationName') == 'UiAutomator2'
    
    mock_locator_manager.load.assert_called_once()
    assert driver == mock_remote.return_value
    assert mobile_strategy.get_execution_mode() == "mobile"

@patch('src.core.drivers.strategies.appium_mobile_strategy.webdriver.Remote')
def test_initialize_browserstack(mock_remote, mobile_strategy):
    mock_config = Mock()
    mock_config.cloud_platform = 'browserstack'
    mock_config.cloud_user = 'testuser'
    mock_config.cloud_key = 'testkey'
    mock_config.os = 'iOS'
    mock_config.os_version = 'iPhone 14'

    mobile_strategy.initialize(mock_config)

    mock_remote.assert_called_once()
    args, kwargs = mock_remote.call_args
    assert args[0] == 'https://testuser:testkey@hub-cloud.browserstack.com/wd/hub'
    options = kwargs['options']
    assert options.get_capability('platformName') == 'iOS'
    assert options.get_capability('appium:deviceName') == 'iPhone 14'

@patch('src.core.drivers.strategies.appium_mobile_strategy.webdriver.Remote')
def test_navigate_to(mock_remote, mobile_strategy):
    mock_config = Mock()
    mock_config.cloud_platform = 'local'
    mobile_strategy.initialize(mock_config)
    
    mobile_strategy.navigate_to('myapp://home')
    mock_remote.return_value.get.assert_called_once_with('myapp://home')

def test_navigate_to_without_initialization_raises_error(mobile_strategy):
    with pytest.raises(RuntimeError, match="Driver not initialized"):
        mobile_strategy.navigate_to('myapp://home')

@patch('src.core.drivers.strategies.appium_mobile_strategy.webdriver.Remote')
@patch('src.core.drivers.strategies.appium_mobile_strategy.locator_manager')
def test_find_element(mock_locator_manager, mock_remote, mobile_strategy):
    mock_config = Mock()
    mock_config.cloud_platform = 'local'
    mobile_strategy.initialize(mock_config)

    mock_locator_manager.resolve.return_value = '//android.widget.Button[@text="Submit"]'
    
    element = mobile_strategy.find_element('submit_button')
    
    assert element.element == mock_remote.return_value.find_element.return_value
    assert element.name == 'submit_button'
    assert element.locator_tuple == (By.XPATH, '//android.widget.Button[@text="Submit"]')
    mock_locator_manager.resolve.assert_called_once_with('submit_button')
    mock_remote.return_value.find_element.assert_called_once_with(By.XPATH, '//android.widget.Button[@text="Submit"]')

@patch('src.core.drivers.strategies.appium_mobile_strategy.webdriver.Remote')
def test_terminate(mock_remote, mobile_strategy):
    mock_config = Mock()
    mock_config.cloud_platform = 'local'
    mobile_strategy.initialize(mock_config)
    
    mobile_strategy.terminate()
    mock_remote.return_value.quit.assert_called_once()
