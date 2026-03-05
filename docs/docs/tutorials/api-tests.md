# API Testing Tutorial

Learn how to master the **Dual API Strategy** in TAFLEX PY. Choose the right tool for the right job: Playwright for integrated flows or HTTPX for high-performance specialized tests.

---

## 1. Hybrid Approach (Playwright)

**Use case:** Integrated tests where you need to share authentication with a browser or see API calls in a Trace Viewer.

### Creating the Test
Create a standard Playwright spec in `tests/api/`:

```javascript
import pytest

@pytest.mark.api
def test_hybrid_api_strategy(api_driver):
    # Perform request
    response = api_driver.get('/users/1')
    
    # Assert
    assert response.status == 200
    user = response.json()
    assert user['username'] == 'Bret'
```

**How to run:**
```bash
pytest tests/api/
```

---

## 2. Specialized Approach (HTTPX + Pytest)

**Use case:** Standalone API testing, contract validation, and extreme execution speed.

### Creating the Test
Create a file ending in `test_*.py` in `tests/api/`. These tests use **Pytest** as the runner.

```javascript
import { describe, it, expect, beforeAll } from 'vitest';
import { DriverFactory } from '../../src/core/drivers/driver.factory.ts';

describe('Specialized API Strategy (HTTPX + Pytest)', () => {
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
        
        // 3. Standard Pytest assertions
        expect(response.status()).toBe(200);
        const user = await response.json();
        expect(user.id).toBe(1);
    });
});
```

**How to run:**
```bash
# Set provider if not default in .env
API_PROVIDER=httpx pytest tests/api/
```

---

## 3. Which one should I choose?

| Feature | Playwright Strategy | HTTPX Strategy |
|---------|---------------------|----------------|
| **Runner** | Playwright | Pytest |
| **Speed** | Moderate | Fast (Blazing) |
| **Trace Viewer** | Yes | No |
| **Authentication Sharing** | Native with Browser | Manual |
| **Watch Mode** | `npx playwright test --ui` | `npm run test:unit` (Auto-watch) |

---

## 4. Best Practices

- **Shared Locators**: Use `src/resources/locators/api/common.json` to store endpoints for both strategies.
- **Environment URLs**: Always rely on `API_BASE_URL` in your `.env`.
- **Validation**: For both strategies, the `driver` wrapper provides consistent `status()`, .json()`, and `ok()` methods to keep your code portable.
