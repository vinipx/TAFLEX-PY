import pytest
import requests
from src.core.contracts.pact_manager import pact_manager
from src.config.config_manager import config_manager

@pytest.fixture(scope='module')
def pact_setup():
    # Force pact enabled for this test
    config_manager.config.pact_enabled = True
    pact = pact_manager.setup(consumer='UserConsumer', provider='UserService')
    return pact

def test_get_user_contract(pact_setup):
    """Verifies the contract for getting a user by ID."""
    
    expected_response = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }

    # In v3, start with upon_receiving
    (pact_manager
     .upon_receiving('a request for user 1')
     .given('User with ID 1 exists')
     .with_request('GET', '/users/1')
     .will_respond_with(200, body=expected_response))

    def run_test(uri):
        # This is the actual call to the mock service
        response = requests.get(f"{uri}/users/1")
        assert response.status_code == 200
        assert response.json() == expected_response
        return response

    # execute_test handles the pact lifecycle (start/stop mock server)
    pact_manager.execute_test(run_test)
