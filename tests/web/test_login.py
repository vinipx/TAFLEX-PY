import pytest
import allure

@allure.feature('Login')
@allure.story('Valid Credentials')
@pytest.mark.web
def test_should_login_successfully_with_valid_credentials(web_driver):
    driver = web_driver
    
    driver.navigate_to('https://the-internet.herokuapp.com/login')
    driver.capture_screenshot('login_page_loaded')
    driver.load_locators('login')

    username = driver.find_element('username_field')
    password = driver.find_element('password_field')
    login_button = driver.find_element('login_button')

    # Since we are using generic locators, we can mock them if they don't exist
    # but the framework provides fallback to raw selector if logical name not found
    # Let's provide fallback for testing purpose if global locators are empty
    # In standard flow, locator manager would resolve this.
    
    # Using raw selectors as fallback if locators are not populated
    username.fill('tomsmith')
    password.fill('SuperSecretPassword!')
    login_button.click()

    flash_message = driver.find_element('flash_message')
    text = flash_message.get_text()
    
    assert 'You logged into a secure area!' in text
