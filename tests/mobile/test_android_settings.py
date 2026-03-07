import pytest
import allure
from src.core.utils.logger import logger

@allure.feature('Mobile App')
@allure.story('Android System Settings')
@pytest.mark.mobile
@pytest.mark.skip(reason="Requires a running Appium server")
def test_android_settings_interaction(mobile_driver):
    """
    Verifies that the framework can interact with a real Android device via USB
    using the Appium mobile strategy.
    """
    driver = mobile_driver
    
    # 1. Load the mobile locators for the settings app
    driver.load_locators('settings')
    
    # 2. Wait for the main settings title to ensure app is loaded
    title_element = driver.find_element('system_settings_title')
    title_element.wait_for(timeout=10)
    assert title_element.is_visible() is True

    # 3. Take a screenshot of the initial state
    driver.capture_screenshot('settings_home_page')
    
    # 4. Interact with the search button (Broad locator already verified to work)
    search_box = driver.find_element('search_box')
    search_box.wait_for()
    search_box.click()
    
    # 5. Final verification - capture search screen
    driver.capture_screenshot('settings_search_page')
    logger.info("Successfully interacted with real Android device settings!")
