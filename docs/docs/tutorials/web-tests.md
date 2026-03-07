# Web Testing Tutorial

Learn how to write robust and maintainable Web tests using TAFLEX PY.

## 1. Page Object Model (POM)

We recommend using the Page Object Model to encapsulate page-specific logic and locators. This makes tests readable and easy to maintain.

### Step 1: Create Locators
Create a JSON file for your page in `src/resources/locators/web/search.json`:

```json
{
  "search_input": "input[name='q']",
  "search_button": "input[type='submit'] >> n=1"
}
```

### Step 2: Create Page Object
Create a class to handle interactions in `tests/web/pages/search_page.py`:

```javascript
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator('input[name="q"]')

    def open(self):
        self.page.goto('https://www.google.com')

    def search_for(self, term):
        self.search_input.fill(term)
        self.page.keyboard.press('Enter')
```

## 2. Writing the Test Spec

Use the `driver` fixture to inject the initialized strategy into your test.

```javascript
import { test, expect } from '../fixtures.ts';
import { SearchPage } from './pages/search.page.ts';

test.describe('Google Search', () => {
    test('should find relevant results', async ({ driver }) => {
        const searchPage = new SearchPage(driver);
        
        await searchPage.open();
        await searchPage.searchFor('TAFLEX PY');
        
        // Assertions using Playwright's expect
        await expect(driver.page).toHaveTitle(/TAFLEX PY/);
    });
});
```

## 3. Best Practices

- **Load Locators Early**: Always call `driver.loadLocators('page_name')` before interacting with elements.
- **Use Logical Names**: Refer to elements by their logical names (e.g., `login_button`) instead of hardcoded CSS/XPath.
- **Leverage Fixtures**: Use the `driver` fixture to handle automatic browser lifecycle (startup/teardown).

## Running on Cloud Grids

You can run these same tests on **BrowserStack** or **SauceLabs** by simply updating your `.env` file. No code changes are required.

Refer to the [Cloud Execution Tutorial](./cloud-execution.md) for detailed configuration steps.
