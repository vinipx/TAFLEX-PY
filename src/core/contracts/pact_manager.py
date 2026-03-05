import os
from pathlib import Path
from typing import Optional, Callable, Any
from pact import Consumer, Provider
from src.config.config_manager import config_manager

class PactManager:
    """Manages Pact contract testing lifecycle and interactions."""

    def __init__(self) -> None:
        self.enabled: bool = config_manager.get('pact_enabled')
        self.pact = None

    def setup(self, consumer: Optional[str] = None, provider: Optional[str] = None):
        """Sets up a new Pact instance for a consumer-provider pair."""
        if not self.enabled:
            return None

        consumer_name = consumer or config_manager.get('pact_consumer')
        provider_name = provider or config_manager.get('pact_provider')
        pact_dir = str(Path(os.getcwd()) / 'pacts')
        log_level = config_manager.get('pact_log_level')

        self.pact = Consumer(consumer_name).has_pact_with(
            Provider(provider_name),
            pact_dir=pact_dir,
            log_level=log_level
        )
        return self.pact

    def given(self, provider_state: str):
        if not self.enabled or not self.pact:
            return self
        self.pact.given(provider_state)
        return self

    def upon_receiving(self, description: str):
        if not self.enabled or not self.pact:
            return self
        self.pact.upon_receiving(description)
        return self

    def with_request(self, method: str, path: str, **kwargs):
        if not self.enabled or not self.pact:
            return self
        self.pact.with_request(method=method, path=path, **kwargs)
        return self

    def will_respond_with(self, status: int, **kwargs):
        if not self.enabled or not self.pact:
            return self
        self.pact.will_respond_with(status=status, **kwargs)
        return self

    def execute_test(self, test_fn: Callable) -> Any:
        if not self.enabled or not self.pact:
            return test_fn()
            
        with self.pact:
            return test_fn(self.pact.uri)

pact_manager = PactManager()
