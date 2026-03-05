import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('features/login.feature')

@given(parsers.parse('I navigate to "{url}"'))
def navigate_to(web_driver, url):
    web_driver.navigate_to(url)

@when(parsers.parse('I enter "{username}" as username and "{password}" as password'))
def enter_credentials(web_driver, username, password):
    web_driver.load_locators('login')
    username_field = web_driver.find_element('username_field')
    password_field = web_driver.find_element('password_field')

    username_field.fill(username)
    password_field.fill(password)

@when('I click on the login button')
def click_login(web_driver):
    login_button = web_driver.find_element('login_button')
    login_button.click()

@then(parsers.parse('I should see "{expected_text}" in the flash message'))
def verify_flash_message(web_driver, expected_text):
    flash_message = web_driver.find_element('flash_message')
    actual_text = flash_message.get_text()
    assert expected_text in actual_text
