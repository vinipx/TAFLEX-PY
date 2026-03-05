# Test Design Best Practices

## Page Object Model (POM)
Even with hierarchical locators, we recommend using the Page Object Model to encapsulate page actions.

```javascript
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.load_locators('login')
        self.driver.find_element('username_field').fill(username)
        self.driver.find_element('password_field').fill(password)
        self.driver.find_element('login_button').click()
```

## Atomic Tests
Keep tests small and focused on a single capability.

## Clean Data Setup
Use the `DatabaseManager` to set up and tear down test data before and after execution.
