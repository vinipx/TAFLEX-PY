import pytest
import allure
from tests.pages.login_page import LoginPage

@allure.feature('Hybrid Testing')
@pytest.mark.web
@pytest.mark.api
def test_hybrid_api_and_ui(web_driver, api_driver):
    """
    Demonstrates that both web_driver and api_driver fixtures can be requested
    in the same test without global state conflicts.
    """
    # 1. Use API driver to fetch some data (mock scenario)
    response = api_driver.get("https://jsonplaceholder.typicode.com/users/1")
    
    status = getattr(response, "status_code", getattr(response, "status", None))
    if callable(status):
        status = status()
    assert status == 200
    
    # 2. Use Web driver to interact with the UI
    page = web_driver.page
    login_page = LoginPage(page)
    
    login_page.navigate()
    
    # Just asserting the page loads successfully using the UI driver
    assert page.title() == "The Internet"
