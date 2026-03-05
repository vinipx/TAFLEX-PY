import os
import re
from pathlib import Path

docs_dir = Path("docs")

def replace_in_file(filepath, replacements):
    if not filepath.exists():
        return
    content = filepath.read_text(encoding="utf-8")
    for old, new in replacements.items():
        content = content.replace(old, new)
    filepath.write_text(content, encoding="utf-8")

# 1. docusaurus.config.ts
replace_in_file(docs_dir / "docusaurus.config.ts", {
    "TAFLEX TS": "TAFLEX PY",
    "Enterprise Test Automation Framework in TypeScript": "Enterprise Test Automation Framework in Python",
    "taflex-ts": "taflex-py"
})

# 2. src/pages/index.tsx
replace_in_file(docs_dir / "src/pages/index.tsx", {
    "TAFLEX TS": "TAFLEX PY",
    "Node.js (TypeScript)": "Python",
    "Node.js": "Python",
    "Vitest": "Pytest",
    "taflex-ts": "taflex-py",
    "npm install": "python -m venv .venv\nsource .venv/bin/activate\npip install -e .",
    "npm test": "pytest tests/",
    "npm run test:unit": "pytest tests/unit/"
})

# 3. docs/index.md
idx_md = docs_dir / "docs" / "index.md"
idx_content = """---
sidebar_position: 1
title: Introduction
---

# TAFLEX PY

**Enterprise Test Automation Framework in Python**

---

## 🎯 What is TAFLEX PY?

TAFLEX PY is a **unified, enterprise-grade test automation framework** designed for testing Web, API, and Mobile applications using a single codebase. Migrated from the TypeScript version, it leverages **Python** for superior developer experience, powerful fixtures with Pytest, and modern type validation with Pydantic.

### ✨ Key Highlights

| Feature | Description |
|---------|-------------|
| 🚀 **Python First** | Fully typed API (Mypy) for better IDE support and robustness. |
| 🧩 **Strategy Pattern** | Runtime driver resolution between platforms. |
| 📄 **Hierarchical Locators** | Cascading JSON inheritance model. |
| 🛡️ **Type-Safe Config** | Environment variables validated with **Pydantic**. |

---

## 💻 Code Example (Python)

### Web Test

```python
import pytest
import allure

@allure.feature('Login')
def test_should_login_successfully(web_driver):
    driver = web_driver
    driver.navigate_to('https://the-internet.herokuapp.com/login')
    driver.load_locators('login')

    username = driver.find_element('username_field')
    password = driver.find_element('password_field')
    login_button = driver.find_element('login_button')

    username.fill('tomsmith')
    password.fill('SuperSecretPassword!')
    login_button.click()

    flash_message = driver.find_element('flash_message')
    assert 'You logged into a secure area!' in flash_message.get_text()
```
"""
idx_md.write_text(idx_content, encoding="utf-8")

# 4. docs/architecture/overview.md
arch_md = docs_dir / "docs" / "architecture" / "overview.md"
replace_in_file(arch_md, {
    "TAFLEX JS": "TAFLEX PY",
    "Node.ts (ESM), Zod, Dotenv": "Python 3.10+, Pydantic, Pytest",
    "Vitest": "Pytest",
    "config.manager.ts": "config_manager.py",
    "pg (Postgres), mysql2 (MySQL)": "psycopg2, PyMySQL",
    "tests/fixtures.ts": "conftest.py",
    "playwright-bdd": "pytest-bdd"
})
arch_content = arch_md.read_text(encoding="utf-8")
arch_content = arch_content.replace("""```javascript
import { configManager } from './config/config.manager.ts';

// Type-safe access with Zod validation
const browser = configManager.get('BROWSER');
const timeout = configManager.get('TIMEOUT');
```""", """```python
from src.config.config_manager import config_manager

# Type-safe access with Pydantic validation
browser = config_manager.get('browser')
timeout = config_manager.get('timeout')
```""")
arch_content = arch_content.replace("navigate_to(String)", "navigate_to(str)").replace("findElement(String)", "find_element(str)").replace("loadLocators(String)", "load_locators(str)").replace("get(String)", "get(str)").replace("post(String, Object)", "post(str, dict)")
arch_md.write_text(arch_content, encoding="utf-8")

# 5. docs/api/core-interfaces.md
api_md = docs_dir / "docs" / "api" / "core-interfaces.md"
api_content = """# Core API Reference

This page documents the primary interfaces and classes provided by TAFLEX PY.

## AutomationDriver (Abstract Class)

The base class for all automation strategies.

| Method | Description |
|--------|-------------|
| `initialize(config)` | Initializes the driver session. |
| `terminate()` | Closes the driver session. |
| `navigate_to(url)` | Navigates to the specified URL or endpoint. |
| `find_element(logical_name)` | Resolves a locator and returns a wrapped element. |
| `load_locators(page_name)` | Loads page-specific locators from JSON. |

## Element (Wrappers)

TAFLEX PY wraps native engine elements (Playwright or Appium) to provide a consistent API.

### Common Methods

| Method | Description |
|--------|-------------|
| `click()` | Performs a click action. |
| `fill(value)` | Fills an input field with the specified value. |
| `get_text()` | Returns the inner text of the element. |
| `is_visible()` | Returns `True` if the element is visible. |
| `is_enabled()` | Returns `True` if the element is enabled. |
| `wait_for(**kwargs)` | Waits for the element state (visible, hidden, etc). |

## LocatorManager

The engine behind hierarchical locator resolution.

| Method | Description |
|--------|-------------|
| `load(page_name)` | Loads and merges JSON locator files. |
| `resolve(logical_name)`| Returns the selector associated with the logical name. |
"""
api_md.write_text(api_content, encoding="utf-8")

# 6. docs/getting-started/quickstart.md
qs_md = docs_dir / "docs" / "getting-started" / "quickstart.md"
qs_content = """---
sidebar_position: 1
title: Quick Start
---

# Quick Start Guide

Get up and running with TAFLEX PY in under 5 minutes.

## 1. Installation

TAFLEX PY requires **Python 3.10** or higher. 

```bash
# Clone the repository
git clone https://github.com/vinipx/taflex-py.git
cd taflex-py

# Setup virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Install Playwright browsers
playwright install
```

## 2. Configuration

Create your `.env` file:

```bash
cp .env.example .env
```

Now, edit the `.env` file to match your environment:

```env
EXECUTION_MODE=web
BROWSER=chromium
HEADLESS=true
BASE_URL=https://www.google.com
API_BASE_URL=https://jsonplaceholder.typicode.com

# Reporting configuration
REPORTERS=html,allure
```

## 3. Running Your First Test

### Integration Tests (Web/API)
Execute the Pytest test suite:

```bash
# Run all tests
pytest tests/

# Run a specific spec
pytest tests/web/test_login.py
```

### Unit Tests
Verify the framework core components:

```bash
pytest tests/unit/
```

## 4. Visualizing Results

For enterprise reporting, generate the Allure report:

```bash
allure serve allure-results
```

---

## 🏗️ What's Next?

- [Architecture Overview](../architecture/overview.md)
- [How to manage Locators](../guides/locators.md)
"""
qs_md.write_text(qs_content, encoding="utf-8")

# 7. docs/guides/api-testing.md
api_guide_md = docs_dir / "docs" / "guides" / "api-testing.md"
api_guide_content = """# API Testing

TAFLEX PY employs a **Dual API Strategy** that allows you to choose the best tool for your specific testing needs.

| Strategy | Engine | Best For... |
|----------|--------|-------------|
| **Hybrid (E2E)** | Playwright | API calls within UI flows (setup/teardown), shared authentication with browser context. |
| **Specialized (Logic)** | HTTPX + Pytest | High-volume contract testing, complex business logic validation, and standalone API suites requiring maximum execution speed. |

---

## 1. Hybrid API Testing (Playwright)

This strategy uses Playwright's `APIRequestContext`.

## Configuration

Ensure `API_BASE_URL` is set in your `.env` file.

## Writing an API Test

Use the `api_driver` fixture (or a generic driver with `EXECUTION_MODE=api`).

```python
import pytest

@pytest.mark.api
def test_get_user_details(api_driver):
    response = api_driver.get('/users/1')
    assert response.status == 200
    
    user = response.json()
    assert user['username'] == 'Bret'
```

## Available Methods

The API driver supports standard HTTP methods:
- `driver.get(url, **kwargs)`
- `driver.post(url, **kwargs)`
- `driver.put(url, **kwargs)`
- `driver.delete(url, **kwargs)`

## 2. Specialized API Testing (HTTPX + Pytest)

For high-performance, pure API tests (without UI dependencies), TAFLEX PY supports a specialized strategy using **HTTPX**.

### Configuration
Set the provider in your `.env`:
```env
API_PROVIDER=httpx
```

### Writing an HTTPX API Test
Create a file `test_users.py` in your `tests/api/` directory:

```python
import pytest

@pytest.mark.api
def test_fetch_data(api_driver):
    response = api_driver.get('/endpoint')
    assert response.status_code == 200
    
    data = response.json()
    assert 'id' in data
```

### Running Specialized Tests
```bash
pytest tests/api/
```
"""
api_guide_md.write_text(api_guide_content, encoding="utf-8")

# 8. docs/guides/bdd-testing.md
bdd_md = docs_dir / "docs" / "guides" / "bdd-testing.md"
bdd_content = """# BDD Testing

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
"""
bdd_md.write_text(bdd_content, encoding="utf-8")

# 9. docs/guides/developers.md
dev_md = docs_dir / "docs" / "guides" / "developers.md"
replace_in_file(dev_md, {
    "TAFLEX JS": "TAFLEX PY",
    "src/core/drivers/strategies/": "src/core/drivers/strategies/",
    "AutomationDriver": "AutomationDriver",
    "import { AutomationDriver } from '../automation.driver.ts';\n\nexport class MyNewStrategy extends AutomationDriver {\n    // Implement abstract methods\n}": "from src.core.drivers.automation_driver import AutomationDriver\n\nclass MyNewStrategy(AutomationDriver):\n    # Implement abstract methods\n    pass",
    "playwright-bdd": "pytest-bdd",
    "JavaScript": "Python",
    "Node.ts": "Python",
    "npx bddgen": "pytest-bdd",
    "npm run test:bdd": "pytest tests/bdd",
    "Vitest": "Pytest",
    "npm run test:unit": "pytest tests/unit",
    "npm test": "pytest tests/",
    "Zod": "Pydantic",
    "src/config/config.manager.ts": "src/config/config_manager.py",
    "ESLint": "Ruff",
    "Prettier": "Mypy",
    "npm run lint:fix": "ruff check --fix .",
    "npm run lint": "ruff check . && mypy src/"
})

# 10. docs/guides/locators.md
loc_md = docs_dir / "docs" / "guides" / "locators.md"
replace_in_file(loc_md, {
    "Taflex JS": "TAFLEX PY",
    """import { test } from '../fixtures.ts';

test('login test', async ({ driver }) => {
    await driver.navigateTo('https://example.com/login');
    
    // Load page-specific locators
    await driver.loadLocators('login');

    const username = await driver.findElement('username_field');
    await username.fill('myuser');
});""": """def test_login(web_driver):
    web_driver.navigate_to('https://example.com/login')
    
    # Load page-specific locators
    web_driver.load_locators('login')

    username = web_driver.find_element('username_field')
    username.fill('myuser')"""
})

# 11. docs/guides/managers.md
man_md = docs_dir / "docs" / "guides" / "managers.md"
replace_in_file(man_md, {
    "TAFLEX JS": "TAFLEX PY",
    "JavaScript/Node.ts": "Python",
    "frontend development stacks": "data engineering, backend, and testing ecosystem",
    "Java to JavaScript": "TypeScript to Python",
    "Node.ts": "Python"
})

# 12. docs/guides/mcp-integration.md
mcp_md = docs_dir / "docs" / "guides" / "mcp-integration.md"
replace_in_file(mcp_md, {
    "TAFLEX JS": "TAFLEX PY",
    "node": "python",
    "src/mcp/server.ts": "src/mcp/server.py",
    ".spec.ts": ".py",
    "npx playwright test": "pytest"
})

# 13. docs/guides/pact-testing.md
pact_md = docs_dir / "docs" / "guides" / "pact-testing.md"
replace_in_file(pact_md, {
    "tests/contract/consumer/user.spec.ts": "tests/contract/consumer/test_user.py",
    """import { pactManager } from '../../../src/core/contracts/pact.manager.ts';
import axios from 'axios';

describe('User API Contract', () => {
  const pact = pactManager.setup();

  it('should return user details', async () => {
    // 1. Define Interaction
    await pactManager.addInteraction({
      state: 'user with ID 1 exists',
      uponReceiving: 'a request for user 1',
      withRequest: {
        method: 'GET',
        path: '/users/1',
      },
      willRespondWith: {
        status: 200,
        body: {
          id: 1,
          name: 'John Doe',
        },
      },
    });

    // 2. Execute Test against the Mock Server
    await pactManager.executeTest(async (mockServer) => {
      const response = await axios.get(`${mockServer.url}/users/1`);
      expect(response.status).toBe(200);
      expect(response.data.name).toBe('John Doe');
    });
  });
});""": """import requests
from src.core.contracts.pact_manager import pact_manager

def test_user_api_contract():
    pact = pact_manager.setup()
    
    (pact_manager
     .given('user with ID 1 exists')
     .upon_receiving('a request for user 1')
     .with_request('GET', '/users/1')
     .will_respond_with(200, body={"id": 1, "name": "John Doe"}))
     
    def run_test(mock_url):
        response = requests.get(f"{mock_url}/users/1")
        assert response.status_code == 200
        assert response.json()['name'] == 'John Doe'
        
    pact_manager.execute_test(run_test)""",
    "pact-verify.ts": "pact_verify.py",
    """import { Verifier } from '@pact-foundation/pact';

const opts = {
  provider: 'my-api-service',
  providerBaseUrl: 'http://localhost:3000',
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  pactBrokerToken: process.env.PACT_BROKER_TOKEN,
  publishVerificationResult: true,
  providerVersion: '1.0.0',
};

new Verifier(opts).verifyProvider();""": """from pact import Verifier
import os

verifier = Verifier(
    provider='my-api-service',
    provider_base_url='http://localhost:3000'
)

verifier.verify_with_broker(
    broker_url=os.getenv('PACT_BROKER_URL'),
    broker_token=os.getenv('PACT_BROKER_TOKEN'),
    publish_version='1.0.0',
    publish_verification_results=True
)""",
    "npm run test:contract": "pytest tests/contract/consumer",
    "npm run pact:publish": "# Custom script using pact-cli",
    "npm run pact:verify": "python pact_verify.py"
})

# 14. docs/guides/qa-engineers.md
qa_md = docs_dir / "docs" / "guides" / "qa-engineers.md"
replace_in_file(qa_md, {
    "TAFLEX JS": "TAFLEX PY",
    """test('should verify account balance', async ({ driver }) => {
    await driver.navigateTo('/accounts');
    await driver.loadLocators('accounts');
    
    const balance = await driver.findElement('total_balance');
    expect(await balance.getText()).toBe('$1,000.00');
});""": """def test_verify_account_balance(web_driver):
    web_driver.navigate_to('/accounts')
    web_driver.load_locators('accounts')
    
    balance = web_driver.find_element('total_balance')
    assert balance.get_text() == '$1,000.00'""",
    "npx playwright show-trace": "playwright show-trace"
})

# 15. docs/guides/reporting.md
rep_md = docs_dir / "docs" / "guides" / "reporting.md"
replace_in_file(rep_md, {
    "TAFLEX JS": "TAFLEX PY",
    "`test('should login @PROJ-123', ...)`": "`@pytest.mark.PROJ_123` or naming `test_PROJ_123_login`",
    "taflex-ts-automation": "taflex-py-automation"
})

# 16. docs/guides/unit-testing.md
unit_md = docs_dir / "docs" / "guides" / "unit-testing.md"
replace_in_file(unit_md, {
    "Taflex JS": "TAFLEX PY",
    "Vitest": "Pytest",
    "npm run test:unit": "pytest tests/unit",
    "*.spec.ts": "test_*.py",
    "Zod": "Pydantic",
    "vi.mock()": "monkeypatch / unittest.mock"
})

# 17. docs/tutorials/api-tests.md
api_tut_md = docs_dir / "docs" / "tutorials" / "api-tests.md"
replace_in_file(api_tut_md, {
    "TAFLEX JS": "TAFLEX PY",
    "Axios": "HTTPX",
    "Vitest": "Pytest",
    ".axios.spec.ts": "test_*.py",
    "npx playwright test tests/api/": "pytest tests/api/",
    """import { test, expect } from '../fixtures.ts';

test.describe('Hybrid API Strategy (Playwright)', () => {
    // 1. Configure mode
    test.use({ mode: 'api' });

    test('should validate user profile integration', async ({ driver }) => {
        // 2. Perform request
        const response = await driver.get('/users/1');
        
        // 3. Assert using Playwright matchers
        expect(response.status()).toBe(200);
        const user = await response.json();
        expect(user.username).toBe('Bret');
    });
});""": """import pytest

@pytest.mark.api
def test_hybrid_api_strategy(api_driver):
    # Perform request
    response = api_driver.get('/users/1')
    
    # Assert
    assert response.status == 200
    user = response.json()
    assert user['username'] == 'Bret'""",
    """import { describe, it, expect, beforeAll } from 'vitest';
import { DriverFactory } from '../../src/core/drivers/driver.factory.ts';

describe('Specialized API Strategy (Axios + Vitest)', () => {
    let driver;

    beforeAll(async () => {
        // 1. Initialize driver with api mode
        // Ensure API_PROVIDER=axios is set in .env
        driver = DriverFactory.create('api'); 
        await driver.initialize({
            apiBaseUrl: 'https:/.jsonplaceholder.typicode.com'
        });
    });

    it('should validate user contract with high performance', async () => {
        // 2. Perform request
        const response = await driver.get('/users/1');
        
        // 3. Standard Vitest assertions
        expect(response.status()).toBe(200);
        const user = await response.json();
        expect(user.id).toBe(1);
    });
});""": """import pytest
from src.core.drivers.driver_factory import DriverFactory

@pytest.fixture(scope="module")
def httpx_driver():
    # Ensure API_PROVIDER=httpx in config
    driver = DriverFactory.create('api')
    driver.initialize({"api_base_url": "https://jsonplaceholder.typicode.com"})
    yield driver
    driver.terminate()

def test_specialized_api_strategy(httpx_driver):
    response = httpx_driver.get('/users/1')
    
    assert response.status_code == 200
    user = response.json()
    assert user['id'] == 1""",
    "API_PROVIDER=axios npm run test:unit": "API_PROVIDER=httpx pytest tests/api/"
})

# 18. docs/tutorials/bdd-tests.md
bdd_tut_md = docs_dir / "docs" / "tutorials" / "bdd-tests.md"
replace_in_file(bdd_tut_md, {
    "TAFLEX JS": "TAFLEX PY",
    "tests/bdd/steps/google.steps.ts": "tests/bdd/test_google.py",
    "npm run test:bdd": "pytest tests/bdd",
    """import { createBdd } from 'playwright-bdd';
import { test, expect } from '../../fixtures.ts';

const { Given, When, Then } = createBdd(test);

Given('I navigate to {string}', async ({ driver }, url) => {
    await driver.navigateTo(url);
});

When('I search for {string}', async ({ driver }, term) => {
    await driver.loadLocators('global'); // Using global locators
    const searchInput = await driver.findElement('search_input');
    await searchInput.fill(term);
    await searchInput.press('Enter');
});

Then('I should see results related to {string}', async ({ driver }, expected) => {
    // Assertions using TAFLEX JS unified element API
    const body = await driver.page.textContent('body');
    expect(body).toContain(expected);
});""": """from pytest_bdd import scenarios, given, when, then, parsers

scenarios('features/google_search.feature')

@given(parsers.parse('I navigate to "{url}"'))
def navigate_to(web_driver, url):
    web_driver.navigate_to(url)

@when(parsers.parse('I search for "{term}"'))
def search(web_driver, term):
    web_driver.load_locators('global')
    search_input = web_driver.find_element('search_input')
    search_input.fill(term)
    search_input.type('\\n') # Enter

@then(parsers.parse('I should see results related to "{expected}"'))
def verify_results(web_driver, expected):
    body_text = web_driver.find_element('body').get_text()
    assert expected in body_text"""
})

# 19. docs/tutorials/cloud-execution.md
cloud_tut_md = docs_dir / "docs" / "tutorials" / "cloud-execution.md"
replace_in_file(cloud_tut_md, {
    "Taflex JS": "TAFLEX PY",
    "npm run test:web": "pytest tests/web",
    "npm run test:bdd": "pytest tests/bdd",
    "OS=\"OS X\" OS_VERSION=\"Ventura\" CLOUD_PLATFORM=\"browserstack\" npm run test:web": "OS=\"OS X\" OS_VERSION=\"Ventura\" CLOUD_PLATFORM=\"browserstack\" pytest tests/web"
})

# 20. docs/tutorials/contract-testing.md
contract_tut_md = docs_dir / "docs" / "tutorials" / "contract-testing.md"
replace_in_file(contract_tut_md, {
    "taflex-ts": "taflex-py",
    "tests/contract/consumer/profile.spec.ts": "tests/contract/consumer/test_profile.py",
    "npm run test:contract": "pytest tests/contract/consumer",
    "npm run pact:verify": "python pact_verify.py",
    """import { describe, it, expect } from 'vitest';
import { pactManager } from '../../../src/core/contracts/pact.manager.ts';
import axios from 'axios';

describe('User Profile Contract', () => {
  // Initialize the Pact Mock Server
  const pact = pactManager.setup('user-web-app', 'profile-service');

  it('validates the response for a valid user', async () => {
    // 1. Define the expectation (The Interaction)
    await pactManager.addInteraction({
      state: 'user exists',
      uponReceiving: 'a request for user profile',
      withRequest: {
        method: 'GET',
        path: '/profile',
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application.json' },
        body: {
          username: 'johndoe',
          role: 'editor'
        },
      },
    });

    // 2. Execute the test against the mock server
    await pactManager.executeTest(async (mockServer) => {
      const response = await axios.get(`${mockServer.url}/profile`);
      
      // Verify that the consumer code (axios in this case) 
      // can handle the expected response
      expect(response.status).toBe(200);
      expect(response.data.username).toBe('johndoe');
    });
  });
});""": """import requests
from src.core.contracts.pact_manager import pact_manager

def test_user_profile_contract():
    pact_manager.setup('user-web-app', 'profile-service')
    
    (pact_manager
     .given('user exists')
     .upon_receiving('a request for user profile')
     .with_request('GET', '/profile')
     .will_respond_with(200, headers={'Content-Type': 'application/json'}, body={
         "username": "johndoe",
         "role": "editor"
     }))
     
    def run_test(mock_url):
        response = requests.get(f"{mock_url}/profile")
        assert response.status_code == 200
        assert response.json()['username'] == 'johndoe'
        
    pact_manager.execute_test(run_test)"""
})

# 21. docs/tutorials/mobile-tests.md
mobile_tut_md = docs_dir / "docs" / "tutorials" / "mobile-tests.md"
replace_in_file(mobile_tut_md, {
    "TAFLEX JS": "TAFLEX PY",
    """import { test, expect } from '../fixtures.ts';

test.describe('Mobile App Login', () => {
    test.use({ mode: 'mobile' });

    test('should login on Android', async ({ driver }) => {
        // Load mobile-specific locators
        await driver.loadLocators('login');

        const userField = await driver.findElement('username_input');
        const passField = await driver.findElement('password_input');
        const loginBtn = await driver.findElement('submit_button');

        await userField.fill('mobile_user');
        await passField.fill('secret_pass');
        await loginBtn.click();

        const welcome = await driver.findElement('welcome_text');
        expect(await welcome.isVisible()).toBeTruthy();
    });
});""": """import pytest

@pytest.mark.mobile
def test_should_login_on_android(mobile_driver):
    mobile_driver.load_locators('login')

    user_field = mobile_driver.find_element('username_input')
    pass_field = mobile_driver.find_element('password_input')
    login_btn = mobile_driver.find_element('submit_button')

    user_field.fill('mobile_user')
    pass_field.fill('secret_pass')
    login_btn.click()

    welcome = mobile_driver.find_element('welcome_text')
    assert welcome.is_visible() is True"""
})

# 22. docs/tutorials/web-tests.md
web_tut_md = docs_dir / "docs" / "tutorials" / "web-tests.md"
replace_in_file(web_tut_md, {
    "TAFLEX JS": "TAFLEX PY",
    "tests/web/pages/search.page.ts": "tests/web/pages/search_page.py",
    "Taflex JS": "TAFLEX PY",
    """export class SearchPage {
    constructor(driver) {
        this.driver = driver;
    }

    async open() {
        await this.driver.navigateTo('https://www.google.com');
        // Load the page-specific locators
        await this.driver.loadLocators('search');
    }

    async searchFor(term) {
        const input = await this.driver.findElement('search_input');
        await input.fill(term);
        await this.driver.page.keyboard.press('Enter');
    }
}""": """class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.navigate_to('https://www.google.com')
        self.driver.load_locators('search')

    def search_for(self, term):
        input_element = self.driver.find_element('search_input')
        input_element.fill(term)
        self.driver.page.keyboard.press('Enter')""",
    """import { test, expect } from '../fixtures.ts';
import { SearchPage } from './pages/search.page.ts';

test.describe('Google Search', () => {
    test('should find relevant results', async ({ driver }) => {
        const searchPage = new SearchPage(driver);
        
        await searchPage.open();
        await searchPage.searchFor('Taflex JS');
        
        // Assertions using Playwright's expect
        await expect(driver.page).toHaveTitle(/Taflex JS/);
    });
});""": """from tests.web.pages.search_page import SearchPage

def test_google_search(web_driver):
    search_page = SearchPage(web_driver)
    
    search_page.open()
    search_page.search_for('TAFLEX PY')
    
    # Assertions
    assert "TAFLEX PY" in web_driver.page.title()"""
})

# 23. docs/best-practices/test-design.md
best_md = docs_dir / "docs" / "best-practices" / "test-design.md"
replace_in_file(best_md, {
    """class LoginPage {
    constructor(driver) {
        this.driver = driver;
    }

    async login(username, password) {
        await this.driver.loadLocators('login');
        await (await this.driver.findElement('username_field')).fill(username);
        await (await this.driver.findElement('password_field')).fill(password);
        await (await this.driver.findElement('login_button')).click();
    }
}""": """class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.load_locators('login')
        self.driver.find_element('username_field').fill(username)
        self.driver.find_element('password_field').fill(password)
        self.driver.find_element('login_button').click()"""
})

# 24. docs/troubleshooting/common-issues.md
trouble_md = docs_dir / "docs" / "troubleshooting" / "common-issues.md"
replace_in_file(trouble_md, {
    "npx playwright install": "playwright install"
})

# 25. docs/contributing/guidelines.md
cont_md = docs_dir / "docs" / "contributing" / "guidelines.md"
replace_in_file(cont_md, {
    "Taflex JS": "TAFLEX PY",
    "npm test && npm run test:unit": "pytest tests/",
    "Use ESM (import/export).": "Use Python 3.10+ typing standards."
})

# 26. docs/changelog.md
cl_md = docs_dir / "docs" / "changelog.md"
cl_content = """# Changelog

## [1.0.0] - 2026-03-05
### Added
- Initial release of TAFLEX PY (migrated from TypeScript).
- Unified `AutomationDriver` with Playwright Python and HTTPX strategies.
- Hierarchical JSON Locator Manager.
- Type-safe configuration with Pydantic.
- Integrated Pytest for standard and BDD tests.
- Docusaurus enterprise documentation updated to Python stack.
"""
cl_md.write_text(cl_content, encoding="utf-8")

print("Docs successfully updated for Python stack!")
