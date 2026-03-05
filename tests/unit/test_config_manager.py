import os
import pytest
from pydantic import ValidationError
from src.config.config_manager import AppConfig, ConfigManager

def test_default_config(monkeypatch):
    # Remove any env vars that might interfere
    monkeypatch.delenv("EXECUTION_MODE", raising=False)
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("REPORTERS", raising=False)
    
    config = AppConfig(_env_file=None) # ignore .env explicitly
    
    assert config.execution_mode == "web"
    assert config.browser == "chromium"
    assert config.headless is True
    assert config.timeout == 30000
    assert config.reporters == ["html"]
    assert config.base_url is None

def test_override_config_via_env(monkeypatch):
    monkeypatch.setenv("EXECUTION_MODE", "api")
    monkeypatch.setenv("TIMEOUT", "5000")
    monkeypatch.setenv("HEADLESS", "false")
    monkeypatch.setenv("BASE_URL", "https://example.com")
    monkeypatch.setenv("REPORTERS", "html, allure")
    monkeypatch.setenv("RP_ATTRIBUTES", "key1:value1;key2:value2")

    config = AppConfig()
    assert config.execution_mode == "api"
    assert config.timeout == 5000
    assert config.headless is False
    assert str(config.base_url) == "https://example.com/"
    assert config.reporters == ["html", "allure"]
    assert config.rp_attributes == [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]

def test_invalid_enum_raises_error(monkeypatch):
    monkeypatch.setenv("EXECUTION_MODE", "invalid_mode")
    with pytest.raises(ValidationError) as exc_info:
        AppConfig()
    assert "Input should be 'web', 'api' or 'mobile'" in str(exc_info.value)

def test_empty_base_url_becomes_none(monkeypatch):
    monkeypatch.setenv("BASE_URL", "")
    config = AppConfig()
    assert config.base_url is None

    monkeypatch.setenv("BASE_URL", "/")
    config2 = AppConfig()
    assert config2.base_url is None
