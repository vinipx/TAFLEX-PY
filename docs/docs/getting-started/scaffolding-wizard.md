---
sidebar_position: 1.5
title: Scaffolding Wizard
---

# Scaffolding Wizard

The **TAFLEX PY Modular** framework includes an interactive, CLI-based Scaffolding Wizard (`scaffold.sh`) that dynamically generates a bespoke test automation project based on your specific requirements.

Instead of cloning a monolithic repository full of tools you don't need, the wizard asks you a series of questions and builds a lightweight, clean project tailored to your team's stack.

## How to Run It

To generate a new project, simply execute the script from the root of the TAFLEX repository:

```bash
./scaffold.sh
```

## Step-by-Step Options

### 1. Testing Modules Selection

The wizard first asks which domains you intend to test. By selecting only what you need, you reduce dependency bloat.

*   **Web Testing (Playwright)?**: Includes `taflex.web` and installs `playwright` dependencies. Select this for browser automation.
*   **API Testing (HTTPX)?**: Includes `taflex.api` and installs `httpx`. Select this for high-speed, direct backend API tests.
*   **Mobile Testing (Appium)?**: Includes `taflex.mobile` and installs `Appium-Python-Client`. Select this for iOS/Android native app automation.
*   **Contract Testing (Pact)?**: Includes `taflex.contract` and installs `pact-python`. Select this for consumer-driven contract testing.

*Note: If no modules are selected, the wizard defaults to Web Testing.*

### 2. Reporting Tools Selection

Next, the wizard configures your reporting stack:

*   **HTML Report (pytest-html)?**: Generates a lightweight, single-file HTML report directly from pytest.
*   **Allure Report?**: Sets up `allure-pytest` integration for rich, interactive, historical reporting. Generates a helper `allure.sh` script to serve results locally.
*   **ReportPortal?**: Sets up `pytest-reportportal` and populates the `.env` file with necessary EPAM ReportPortal configurations (endpoint, token, project name).
*   **Jira Xray?**: Sets up `pytest-jira-xray` to sync automated test results directly back to Jira Test Executions.

### 3. CI/CD Configuration

The wizard can automatically generate CI/CD pipeline files for your target infrastructure:

*   **GitHub Actions**: Copies the pre-configured `.github/workflows/ci.yml` template into your project.
*   **GitLab CI**: Generates a `.gitlab-ci.yml` file with optimized caching, linting, and Pytest steps.
*   **None**: Skips CI generation.

### 4. Target Directory

Finally, you define where the new project should be created:

```text
Enter the project directory path (default: ./my-test-project):
```

## What Gets Generated?

The wizard seamlessly creates a ready-to-run environment in your target directory containing:

1.  **Source Code (`src/taflex/`)**: Copies the `core` module and any domain modules (e.g., `web`, `api`) you selected.
2.  **`pyproject.toml`**: The modern Python build file. It dynamically populates the `dependencies` list and `pytest` markers based on your selections.
3.  **`.env`**: The central framework configuration file. It sets `EXECUTION_MODE` to your primary selection and uncomments the relevant sections (e.g., `APPIUM_SERVER_URL` if mobile was selected).
4.  **`tests/` directory**: Generates sample Page Objects, tests, and a local `conftest.py` that inherits from the core framework fixtures to get you started immediately.
5.  **`docs/` directory**: Copies/generates the local documentation tailored to the modules you selected, acting as a quick-reference guide for your team.
6.  **`config.sh`**: A helper script to quickly initialize a virtual environment, install the generated `pyproject.toml` dependencies, and download Playwright browsers (if applicable).

## Next Steps

After the wizard completes:

```bash
cd my-test-project
source ./config.sh
pytest
```
