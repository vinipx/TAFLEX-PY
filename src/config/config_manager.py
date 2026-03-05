from typing import List, Literal, Optional, Dict
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    execution_mode: Literal['web', 'api', 'mobile'] = Field(default='web', alias='EXECUTION_MODE')
    browser: Literal['chromium', 'firefox', 'webkit'] = Field(default='chromium', alias='BROWSER')
    headless: bool = Field(default=True, alias='HEADLESS')
    cloud_platform: Literal['local', 'browserstack', 'saucelabs'] = Field(default='local', alias='CLOUD_PLATFORM')
    cloud_user: Optional[str] = Field(default=None, alias='CLOUD_USER')
    cloud_key: Optional[str] = Field(default=None, alias='CLOUD_KEY')
    browser_version: str = Field(default='latest', alias='BROWSER_VERSION')
    os: Optional[str] = Field(default=None, alias='OS')
    os_version: Optional[str] = Field(default=None, alias='OS_VERSION')
    remote_url: Optional[HttpUrl] = Field(default=None, alias='REMOTE_URL')
    
    base_url: Optional[HttpUrl] = Field(default=None, alias='BASE_URL')
    api_base_url: Optional[HttpUrl] = Field(default=None, alias='API_BASE_URL')
    api_provider: Literal['playwright', 'axios'] = Field(default='playwright', alias='API_PROVIDER')
    timeout: int = Field(default=30000, alias='TIMEOUT')
    
    reporters_raw: str = Field(default='html', alias='REPORTERS')
    allure_results_dir: str = Field(default='allure-results', alias='ALLURE_RESULTS_DIR')
    
    rp_endpoint: Optional[HttpUrl] = Field(default=None, alias='RP_ENDPOINT')
    rp_api_key: Optional[str] = Field(default=None, alias='RP_API_KEY')
    rp_project: Optional[str] = Field(default=None, alias='RP_PROJECT')
    rp_launch: Optional[str] = Field(default=None, alias='RP_LAUNCH')
    rp_attributes_raw: Optional[str] = Field(default=None, alias='RP_ATTRIBUTES')
    rp_description: Optional[str] = Field(default=None, alias='RP_DESCRIPTION')

    xray_enabled: bool = Field(default=False, alias='XRAY_ENABLED')
    xray_client_id: Optional[str] = Field(default=None, alias='XRAY_CLIENT_ID')
    xray_client_secret: Optional[str] = Field(default=None, alias='XRAY_CLIENT_SECRET')
    xray_project_key: Optional[str] = Field(default=None, alias='XRAY_PROJECT_KEY')
    xray_test_plan_key: Optional[str] = Field(default=None, alias='XRAY_TEST_PLAN_KEY')
    xray_test_exec_key: Optional[str] = Field(default=None, alias='XRAY_TEST_EXEC_KEY')
    xray_environment: Optional[str] = Field(default=None, alias='XRAY_ENVIRONMENT')

    pact_enabled: bool = Field(default=False, alias='PACT_ENABLED')
    pact_broker_url: Optional[HttpUrl] = Field(default=None, alias='PACT_BROKER_URL')
    pact_broker_token: Optional[str] = Field(default=None, alias='PACT_BROKER_TOKEN')
    pact_consumer: str = Field(default='taflex-consumer', alias='PACT_CONSUMER')
    pact_provider: str = Field(default='taflex-provider', alias='PACT_PROVIDER')
    pact_log_level: Literal['debug', 'info', 'warn', 'error'] = Field(default='info', alias='PACT_LOG_LEVEL')

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

    @field_validator('base_url', 'api_base_url', mode='before')
    def empty_str_to_none(cls, v: str | None) -> str | None:
        if v == '' or v == '/':
            return None
        return v

    @property
    def reporters(self) -> List[str]:
        return [s.strip() for s in self.reporters_raw.split(',')]

    @property
    def rp_attributes(self) -> List[Dict[str, str]]:
        if not self.rp_attributes_raw:
            return []
        attrs = []
        for attr in self.rp_attributes_raw.split(';'):
            if ':' in attr:
                key, value = attr.split(':', 1)
                attrs.append({'key': key, 'value': value})
        return attrs

class ConfigManager:
    def __init__(self) -> None:
        self.config = AppConfig()

    def get(self, key: str) -> any:
        if key in ('reporters', 'rp_attributes'):
            return getattr(self.config, key)
        return getattr(self.config, f"{key}_raw", getattr(self.config, key))

config_manager = ConfigManager()
