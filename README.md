<h1 align="center">🚀 TAFLEX PY</h1>

<div align="center">

**The Enterprise-Grade, Multi-Platform Automation Engine in Python.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

</div>

<div align="center">
  <h3>
    <a href="https://vinipx.github.io/TAFLEX-PY">📖 See Documentation</a>
  </h3>
</div>

---

## 💎 Why TAFLEX PY?

**TAFLEX PY** is a modern, enterprise-grade test automation framework rewritten in Python. It unifies Web, API, and Mobile testing into a single Strategy-based architecture, leveraging powerful Python native tools like Pytest and Pydantic for maximum developer productivity and robustness.

### ✨ Key Capabilities

*   🌐 **Unified Multi-Platform**: Playwright (Web/Hybrid API), HTTPX (Specialized API), and Appium (Mobile).
*   🛡️ **Type-Safe Configuration**: Catch configuration errors instantly with Pydantic validation.
*   🤖 **AI-Agent Ready**: Native **MCP (Model Context Protocol)** server integration for autonomous AI debugging.
*   📂 **Smart Locators**: Hierarchical, JSON-based locator management without hardcoded selectors in tests.
*   🥒 **BDD Support**: Native Gherkin feature execution via `pytest-bdd`.
*   🤝 **Contract Testing**: First-class support for Consumer-Driven Contracts via `pact-python`.
*   🗄️ **Database Integration**: Native support for PostgreSQL and MySQL via SQLAlchemy for seamless test data management.
*   📊 **Enterprise Reporting**: Built-in hooks for Allure, EPAM ReportPortal, and Jira Xray.

---

## 🚀 Quick Start

### 1. Setup
```bash
# Clone the repository
git clone https://github.com/vinipx/taflex-py.git
cd taflex-py

# Run the automated setup script
# (Creates virtual environment, installs dependencies & Playwright browsers, generates .env template)
./setup.sh

# Activate virtual environment
source .venv/bin/activate
```

### 2. Configuration
The `./setup.sh` script automatically creates a `.env` template. Here are the core settings you can adjust:

```env
EXECUTION_MODE=web            # web, api, mobile
BROWSER=chromium              # chromium, firefox, webkit
HEADLESS=true                 # true, false
BASE_URL=https://example.com
API_BASE_URL=https://api.example.com
REPORTERS=html,allure         # html, allure, reportportal, xray
```
*For advanced configuration (Cloud Execution, Xray, Pact), check the generated `.env` file.*

### 3. Run Tests
| Command | Purpose |
| :--- | :--- |
| `pytest tests/` | Run all test suites |
| `pytest tests/web/` | Run Web integration tests |
| `pytest tests/api/` | Run Specialized API tests |
| `pytest tests/mobile/` | Run Mobile Appium tests |
| `pytest tests/bdd/` | Run BDD specifications |
| `pytest tests/unit/` | Run internal framework logic validation |
| `fastmcp run src/mcp/server.py` | Start the **AI-Agent** server |

---

<div align="center">
Built with ❤️ by <a href="https://github.com/vinipx">vinipx</a>
</div>
