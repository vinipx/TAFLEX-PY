# Core API Reference

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
