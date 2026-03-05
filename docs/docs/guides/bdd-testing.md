# BDD Testing

TAFLEX PY supports Behavior-Driven Development (BDD) using Gherkin syntax through the `pytest-bdd` integration.

## Project Structure

BDD tests are located in the `tests/bdd/` directory:
- `features/`: Contains your `.feature` files (Gherkin).
- `test_*.py`: Contains your Python step definitions and scenario bindings.

## Writing a Feature File

Create a file `tests/bdd/features/login.feature`:

```gherkin
Feature: User Login

  Scenario: Successful login
    Given I navigate to "https://example.com/login"
    When I enter "myuser" as username and "mypass" as password
    And I click on the login button
    Then I should see "Welcome" in the header
```

## Writing Step Definitions

Create a Python file `tests/bdd/test_login_bdd.py`. Use the decorators from `pytest-bdd` and the TAFLEX PY `web_driver` fixture:

```python
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('features/login.feature')

@given(parsers.parse('I navigate to "{url}"'))
def navigate_to(web_driver, url):
    web_driver.navigate_to(url)

@when(parsers.parse('I enter "{username}" as username and "{password}" as password'))
def enter_credentials(web_driver, username, password):
    web_driver.load_locators('login')
    username_field = web_driver.find_element('username')
    password_field = web_driver.find_element('password')

    username_field.fill(username)
    password_field.fill(password)

@when('I click on the login button')
def click_login(web_driver):
    web_driver.find_element('login_btn').click()

@then(parsers.parse('I should see "{expected}" in the header'))
def verify_header(web_driver, expected):
    header = web_driver.find_element('header')
    assert expected in header.get_text()
```

## Running BDD Tests

You can run BDD tests specifically using:

```bash
pytest tests/bdd/
```
