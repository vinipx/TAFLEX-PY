#!/bin/bash

# TAFLEX TS - Allure Report Utility
# This script ensures allure-commandline is installed, generates the report, and opens it.

# Colors for better visibility
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   TAFLEX TS - Allure Reporter        ${NC}"
echo -e "${BLUE}=======================================${NC}"

# 1. Check if allure-commandline is installed
if ! npx allure --version &> /dev/null; then
    echo -e "${YELLOW}[!] Allure commandline not found. Installing...${NC}"
    npm install --save-dev allure-commandline
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[✓] Allure installed successfully.${NC}"
    else
        echo -e "${RED}[✗] Failed to install Allure. Please check your internet connection and permissions.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[✓] Allure is already installed.${NC}"
fi

# 2. Check if allure-results directory exists and is not empty
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results 2>/dev/null)" ]; then
    echo -e "${RED}[✗] Error: 'allure-results/' directory is missing or empty.${NC}"
    echo -e "${YELLOW}Please run your tests first with REPORTERS=allure enabled.${NC}"
    exit 1
fi

# 3. Generate the report
echo -e "${BLUE}[i] Generating report from allure-results...${NC}"
npx allure generate allure-results --clean -o allure-report

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] Report generated in 'allure-report/'${NC}"
else
    echo -e "${RED}[✗] Failed to generate Allure report.${NC}"
    exit 1
fi

# 4. Open the report
echo -e "${BLUE}[i] Opening Allure report in your browser...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server.${NC}"
npx allure open allure-report
