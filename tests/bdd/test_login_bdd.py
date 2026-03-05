from pytest_bdd import scenarios
from tests.bdd.steps.login_steps import (  # noqa: F401
    navigate_to,
    enter_credentials,
    click_login,
    verify_flash_message,
)

# Load scenarios from feature file
scenarios('features/login.feature')
