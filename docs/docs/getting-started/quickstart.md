---
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
