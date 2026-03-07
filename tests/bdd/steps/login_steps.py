from pytest_bdd import given, when, then, parsers
from playwright.sync_api import expect
from tests.pages.login_page import LoginPage

@given(parsers.parse('I navigate to "{url}"'))
def navigate_to(web_driver, url):
    web_driver.page.goto(url)

@when(parsers.parse('I enter "{username}" as username and "{password}" as password'))
def enter_credentials(web_driver, username, password):
    login_page = LoginPage(web_driver.page)
    login_page.username_input.fill(username)
    login_page.password_input.fill(password)

@when('I click on the login button')
def click_login(web_driver):
    login_page = LoginPage(web_driver.page)
    login_page.login_button.click()

@then(parsers.parse('I should see "{expected_text}" in the flash message'))
def verify_flash_message(web_driver, expected_text):
    login_page = LoginPage(web_driver.page)
    expect(login_page.flash_message).to_contain_text(expected_text)
