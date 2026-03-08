---
sidebar_position: 2
title: Framework Execution Flow
---

# Framework Execution Flow

A common question when setting up or extending TAFLEX PY Modular is: **"If we have specific fixtures in `conftest.py` like `web_driver` or `api_driver`, why do we still need the `DriverFactory` and the `EXECUTION_MODE` environment variable?"**

This document explains the "Why" behind the framework's execution flow and the architecture.

## 1. Why do we need `EXECUTION_MODE` in `.env`?

While you might have specific tests that explicitly request a `web_driver` or `api_driver`, the framework also provides a generic, smart `driver` fixture in `conftest.py`. The behavior of this generic fixture defaults to the `EXECUTION_MODE` variable.

### Use Cases:
* **Global Test Runs (BDD):** In Behavior-Driven Development (Cucumber/Gherkin) with tools like `pytest-bdd`, step definitions usually rely on a single, global `driver` fixture. By changing `EXECUTION_MODE=web` or `EXECUTION_MODE=mobile` in your `.env` (or CI/CD pipeline), you can run the exact same scenarios against a web browser or a mobile device without altering a single line of test code.
* **Hybrid Frameworks:** It sets the "default" behavior of the framework. If a standard test doesn't explicitly use `@pytest.mark.api` or request `api_driver`, it inherits the global environment setting.

## 2. Dynamic Fixture Overriding

Instead of forcing you to use specific fixtures everywhere, `conftest.py` dynamically overrides the `EXECUTION_MODE` if it detects a specific marker.

```python
# conftest.py
@pytest.fixture
def driver(request):
    config = AppConfig()
    
    # Override execution_mode if marker is present
    if request.node.get_closest_marker("api"):
        config.execution_mode = "api"
    elif request.node.get_closest_marker("web"):
        config.execution_mode = "web"
    elif request.node.get_closest_marker("mobile"):
        config.execution_mode = "mobile"
    
    driver_instance = DriverFactory.create(config)
    driver_instance.start()
    yield driver_instance
    driver_instance.stop()
```

When you decorate a test with `@pytest.mark.api`, the framework guarantees that `driver` will yield an `HttpxClient`, completely overriding the `.env` value.

## 3. Why do we need the `DriverFactory`?

The Pytest fixtures in `conftest.py` determine *when* a driver is created (e.g., function scope). The Factory pattern determines *how* it is created.

* **Separation of Concerns:** `conftest.py` acts as a lightweight dependency injection layer. It should not contain logic about configuring Playwright context options, connecting to Appium server URLs, or setting up HTTPX timeouts. The `DriverFactory` handles the complexity of instantiating the correct engine.
* **Uniform Interface:** Because of the factory, `conftest.py` can blindly call `driver_instance.start()` and `driver_instance.stop()` on **any** type of driver. The test runner doesn't care if it's shutting down an API session or closing a mobile emulator.
* **Extensibility:** If your team decides to add a new `desktop` execution mode, you simply create a class, register it in the `DriverFactory`, and your `conftest.py` remains completely untouched.

## 4. Testing the Factory and Fixtures

We rigorously unit test the `DriverFactory` and the `conftest.py` overrides (in `tests/framework/`) to verify the **routing logic** in isolation. This ensures that:
- Markers correctly override the `.env` settings.
- The Factory returns the correct `Driver` instance.
- Invalid execution modes fail gracefully with a `ValueError`.

## Summary

* **Specific Fixtures (`web_driver`, `api_driver`)**: Used for explicit setups (e.g., needing an API driver within a Web UI test for data setup).
* **`.env` / `EXECUTION_MODE`**: Drives the global default environment, crucial for CI/CD matrices.
* **Markers (`@pytest.mark.web`)**: Allows elegant, test-level overriding of the default execution mode.
* **Factory Pattern (`DriverFactory`)**: Hides the complex instantiation details of third-party libraries (Playwright/Appium/HTTPX) away from the test layer.
