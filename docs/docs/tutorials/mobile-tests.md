# Mobile Testing Tutorial

Learn how to automate native and hybrid mobile applications using TAFLEX PY and WebdriverIO (Appium).

## 1. Environment Setup

Mobile testing requires the `mobile` strategy. Ensure you have Appium installed and running locally or have access to a cloud lab.

### Capabilities Configuration
Mobile tests require specific capabilities (platform name, device name, app path, etc).

```javascript
// Example mobile config for driver.initialize()
const mobileConfig = {
    capabilities: {
        platformName: 'Android',
        'appium:deviceName': 'Pixel_6',
        'appium:app': './apps/my-app.apk',
        'appium:automationName': 'UiAutomator2'
    }
};
```

## 2. Writing a Mobile Test

Set the `mode: 'mobile'` in your spec to use the WebdriverIO-based strategy.

```javascript
import pytest

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
    assert welcome.is_visible() is True
```

## 3. Best Practices

- **Selectors**: Use `accessibility id` (ID) or `Xpath` carefully. In TAFLEX PY, store these in `src/resources/locators/mobile/`.
- **Platform Branching**: If your app logic differs significantly between iOS and Android, create separate locator files (e.g., `login_ios.json`, `login_android.json`) and load the correct one at runtime.
- **Wait Strategies**: Mobile networks and devices can be slow. Use `await element.waitFor()` before critical actions.

## Execution on Real Devices (Cloud)

While local emulators are great for development, TAFLEX PY allows you to run these tests on **real devices** via BrowserStack and SauceLabs.

See the [Cloud Execution Tutorial](./cloud-execution.md) to learn how to configure your credentials and target real devices.
