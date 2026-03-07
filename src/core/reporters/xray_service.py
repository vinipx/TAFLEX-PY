import requests
from datetime import datetime
from src.config.config_manager import AppConfig
from src.core.utils.logger import logger

class XrayService:
    """Service class for interacting with Jira Xray Cloud API."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.base_url = 'https://xray.cloud.getxray.app/api/v2'
        self.token = None

    def authenticate(self) -> str:
        if self.token:
            return self.token

        client_id = self.config.xray_client_id
        client_secret = self.config.xray_client_secret

        try:
            response = requests.post(f"{self.base_url}/authenticate", json={
                "client_id": client_id,
                "client_secret": client_secret
            })
            response.raise_for_status()
            self.token = response.text.strip('"')  # The API returns a string wrapped in quotes
            return self.token
        except Exception as e:
            logger.error(f"Failed to authenticate with Xray: {str(e)}")
            raise e

    def import_execution(self, results: dict):
        if not self.config.xray_enabled:
            return

        token = self.authenticate()

        try:
            response = requests.post(f"{self.base_url}/import/execution", json=results, headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
            response.raise_for_status()
            logger.info(f"Results imported to Xray. Execution Key: {response.json().get('key')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            err_msg = e.response.text if e.response else str(e)
            logger.error(f"Failed to import execution to Xray: {err_msg}")
            raise e

    def format_results(self, test_results: list) -> dict:
        info = {
            "summary": f"Execution of automated tests - {datetime.utcnow().isoformat()}Z",
            "description": "Imported from taflex-py",
        }

        test_plan_key = self.config.xray_test_plan_key
        test_exec_key = self.config.xray_test_exec_key
        project_key = self.config.xray_project_key
        environment = self.config.xray_environment

        if test_plan_key:
            info['testPlanKey'] = test_plan_key
        if test_exec_key:
            info['testExecKey'] = test_exec_key
        if project_key:
            info['project'] = project_key
        if environment:
            info['testEnvironments'] = [environment]

        return {
            "info": info,
            "tests": test_results
        }
