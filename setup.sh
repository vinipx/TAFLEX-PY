#!/bin/bash

# Taflex PY Setup Script
# This script ensures the environment is ready for development.

echo "🚀 Starting Taflex PY setup..."

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
echo "✅ Found Python v$PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment (.venv)..."
    $PYTHON_CMD -m venv .venv
else
    echo "✅ Virtual environment already exists."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies using pip (pip automatically checks and only installs missing packages)
echo "📦 Installing/verifying dependencies from pyproject.toml..."
pip install -e .

# Check if playwright is installed and install browsers
if command -v playwright &> /dev/null; then
    echo "🎭 Installing/verifying Playwright browsers..."
    playwright install --with-deps
else
    echo "❌ Playwright not found in virtual environment. Dependency installation might have failed."
    exit 1
fi

# Create .env from .env.example if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📄 Creating .env file from .env.example..."
        cp .env.example .env
        echo "⚠️  Please update .env with your specific credentials."
    else
        echo "⚠️  .env.example not found. Creating a comprehensive .env file..."
        cat <<EOF > .env
# ==============================================================================
# TAFLEX PY - Environment Configuration
# ==============================================================================

# ------------------------------------------------------------------------------
# Core Execution Settings
# ------------------------------------------------------------------------------
# The primary mode of execution. 
# Supported values: web, api, mobile
EXECUTION_MODE=web

# Global timeout for requests, element waiting, etc. (in milliseconds)
# Default: 30000
TIMEOUT=30000

# ------------------------------------------------------------------------------
# Web Automation Settings (Playwright)
# ------------------------------------------------------------------------------
# The browser engine to use.
# Supported values: chromium, firefox, webkit
BROWSER=chromium

# Whether to run the browser in headless mode (no UI).
# Supported values: true, false
HEADLESS=true

# The base URL for web navigation.
BASE_URL=https://the-internet.herokuapp.com

# ------------------------------------------------------------------------------
# API Automation Settings
# ------------------------------------------------------------------------------
# The base URL for API requests.
API_BASE_URL=https://jsonplaceholder.typicode.com

# The underlying HTTP client to use for API testing.
# Supported values: playwright (hybrid flows), httpx (high-speed specialized)
API_PROVIDER=httpx

# ------------------------------------------------------------------------------
# Cloud Grid Settings (BrowserStack / SauceLabs)
# ------------------------------------------------------------------------------
# Target execution platform.
# Supported values: local, browserstack, saucelabs
CLOUD_PLATFORM=local

# Cloud provider credentials. (Uncomment and populate if using cloud grid)
# CLOUD_USER=your_username
# CLOUD_KEY=your_access_key

# Specific environment requirements for cloud execution.
# BROWSER_VERSION=latest
# OS=Windows
# OS_VERSION=11

# ------------------------------------------------------------------------------
# Reporting & Integration Settings
# ------------------------------------------------------------------------------
# Comma-separated list of active reporters.
# Example: html, allure, reportportal, xray
REPORTERS=html,allure

# Directory to output Allure results.
ALLURE_RESULTS_DIR=allure-results

# --- EPAM ReportPortal Integration ---
# RP_ENDPOINT=https://rp.yourcompany.com/api/v1
# RP_API_KEY=your_secret_api_key
# RP_PROJECT=taflex-automation
# RP_LAUNCH=nightly_build
# RP_DESCRIPTION=Regression Suite
# RP_ATTRIBUTES=env:dev;team:qa

# --- Jira Xray Integration ---
XRAY_ENABLED=false
# XRAY_CLIENT_ID=your_xray_client_id
# XRAY_CLIENT_SECRET=your_xray_client_secret
# XRAY_PROJECT_KEY=PROJ
# XRAY_TEST_PLAN_KEY=PROJ-100
# XRAY_TEST_EXEC_KEY=PROJ-101
# XRAY_ENVIRONMENT=staging

# ------------------------------------------------------------------------------
# Pact Contract Testing Settings
# ------------------------------------------------------------------------------
PACT_ENABLED=false
PACT_CONSUMER=taflex-consumer
PACT_PROVIDER=taflex-provider
# PACT_BROKER_URL=https://your-pact-broker.com
# PACT_BROKER_TOKEN=your_broker_token
# PACT_LOG_LEVEL=info # debug, info, warn, error
EOF
    fi
else
    echo "✅ .env file already exists."
fi

# Set permissions for utility scripts
echo "🔐 Setting execution permissions for utility scripts..."
chmod +x *.sh
echo "✅ Permissions updated."

echo "✨ Setup complete! You can now activate the environment with 'source .venv/bin/activate' and run 'pytest tests/' to verify the installation."
