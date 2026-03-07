---
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
    page = web_driver.page
    page.goto('https://the-internet.herokuapp.com/login')

    page.locator('#username').fill('tomsmith')
    page.locator('#password').fill('SuperSecretPassword!')
    page.locator('button[type="submit"]').click()

    from playwright.sync_api import expect
    expect(page.locator('#flash')).to_contain_text('You logged into a secure area!')
```
