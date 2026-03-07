import pytest
import allure
from playwright.sync_api import expect
from tests.pages.login_page import LoginPage

@allure.feature('Login')
@allure.story('Valid Credentials')
@pytest.mark.web
def test_should_login_successfully_with_valid_credentials(web_driver):
    # Using Playwright Page object from the driver
    page = web_driver.page
    login_page = LoginPage(page)
    
    login_page.navigate()
    web_driver.capture_screenshot('login_page_loaded')

    login_page.login('tomsmith', 'SuperSecretPassword!')

    expect(login_page.flash_message).to_contain_text('You logged into a secure area!')
