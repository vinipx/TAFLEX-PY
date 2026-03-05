import pytest
import allure

@allure.feature('Users API')
@pytest.mark.api
def test_fetch_users_list_using_api_strategy(api_driver):
    driver = api_driver
    
    # Depending on the config, api_driver might be httpx or playwright
    # We use httpx api strategy structure
    response = driver.get('https://jsonplaceholder.typicode.com/users')
    
    # Playwright API returns status, httpx returns status_code
    status = getattr(response, "status_code", getattr(response, "status", None))
    if callable(status):
        status = status()
    assert status == 200

    # Httpx json() vs Playwright json()
    if hasattr(response, "json") and callable(response.json):
        users = response.json()
    else:
        users = response.json
        
    assert isinstance(users, list) is True
    assert len(users) > 0
    assert 'username' in users[0]
