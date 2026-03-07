#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

RESULTS_DIR="allure-results"

# Check if allure is installed
if ! command -v allure &> /dev/null; then
    echo "Allure is not installed. Attempting to install..."
    
    if command -v brew &> /dev/null; then
        echo "Found Homebrew. Installing allure via brew..."
        brew install allure
    elif command -v npm &> /dev/null; then
        echo "Found npm. Installing allure-commandline via npm..."
        npm install -g allure-commandline
    else
        echo "Error: Neither Homebrew nor npm is installed on this system."
        echo "Please install Allure manually: https://allurereport.org/docs/install/"
        exit 1
    fi
else
    echo "Allure is already installed."
fi

# Check if the results directory exists
if [ ! -d "$RESULTS_DIR" ] || [ -z "$(ls -A "$RESULTS_DIR" 2>/dev/null)" ]; then
    echo "Error: Allure results directory '$RESULTS_DIR' does not exist or is empty."
    echo "Please run your tests first with Allure enabled to generate the results."
    echo "Example: REPORTERS=allure .venv/bin/pytest tests/"
    exit 1
fi

echo "Generating and serving Allure report from '$RESULTS_DIR'..."
allure serve "$RESULTS_DIR"
