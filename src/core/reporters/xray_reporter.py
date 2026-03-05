import pytest
import re
from datetime import datetime, timezone
from src.core.reporters.xray_service import xray_service
from src.config.config_manager import config_manager
from src.core.utils.logger import logger

class XrayReporter:
    """Pytest plugin to export test results to Jira Xray."""

    def __init__(self):
        self.enabled = config_manager.get('xray_enabled')
        self.results = []
        self.test_start_times = {}

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        if not self.enabled:
            return
        self.test_start_times[item.nodeid] = datetime.now(timezone.utc)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if not self.enabled:
            return

        if report.when == "call":
            xray_key = self._extract_xray_key(item)
            if not xray_key:
                return

            start_time = self.test_start_times.get(item.nodeid)
            finish_time = datetime.now(timezone.utc)
            
            status = self._map_status(report.outcome)

            self.results.append({
                "testKey": xray_key,
                "start": start_time.isoformat() if start_time else None,
                "finish": finish_time.isoformat(),
                "status": status,
                "comment": report.longreprtext if report.outcome == 'failed' else ""
            })
        elif report.when == "setup" and report.outcome == "skipped":
            # Handle skipped tests
            xray_key = self._extract_xray_key(item)
            if xray_key:
                self.results.append({
                    "testKey": xray_key,
                    "status": "TODO",
                    "comment": report.longreprtext
                })

    def pytest_sessionfinish(self, session, exitstatus):
        if not self.enabled or not self.results:
            if self.enabled:
                logger.info("Xray: No tests with Xray keys found. Skipping upload.")
            return

        formatted_results = xray_service.format_results(self.results)
        try:
            xray_service.import_execution(formatted_results)
        except Exception as e:
            logger.error(f"Xray: Failed to upload results: {str(e)}")

    def _extract_xray_key(self, item) -> str:
        # Check markers first (e.g. @pytest.mark.PROJ_123)
        for mark in item.iter_markers():
            match = re.match(r'^([A-Z]+-\d+)$', mark.name.replace("_", "-"))
            if match:
                return match.group(1)
            
        # Check node name
        match = re.search(r'([A-Z]+-\d+)', item.name)
        if match:
            return match.group(1)
            
        return None

    def _map_status(self, pytest_status: str) -> str:
        if pytest_status == 'passed':
            return 'PASSED'
        elif pytest_status == 'failed':
            return 'FAILED'
        elif pytest_status == 'skipped':
            return 'TODO'
        return 'FAILED'
