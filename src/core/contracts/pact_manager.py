import os
from pathlib import Path
from typing import Optional, Callable, Any, Union, Dict
from pact import Pact, Verifier
from src.config.config_manager import config_manager

class PactManager:
    """Manages Pact contract testing lifecycle and interactions using Pact-Python v3+ API."""

    def __init__(self) -> None:
        self.pact: Optional[Pact] = None
        self.interaction: Any = None

    @property
    def enabled(self) -> bool:
        return config_manager.get('pact_enabled')

    def setup(self, consumer: Optional[str] = None, provider: Optional[str] = None):
        """Sets up a new Pact instance for a consumer-provider pair."""
        if not self.enabled:
            return None

        consumer_name = consumer or config_manager.get('pact_consumer')
        provider_name = provider or config_manager.get('pact_provider')
        
        self.pact = Pact(consumer_name, provider_name)
        self.interaction = None
        return self.pact

    def given(self, provider_state: str, **kwargs):
        if not self.enabled or not self.pact:
            return self
        if self.interaction:
            self.interaction.given(provider_state, **kwargs)
        return self

    def upon_receiving(self, description: str):
        if not self.enabled or not self.pact:
            return self
        self.interaction = self.pact.upon_receiving(description)
        return self

    def with_request(self, method: str, path: str, **kwargs):
        if not self.enabled or not self.interaction:
            return self
        self.interaction.with_request(method, path)
        if 'headers' in kwargs:
            self.interaction.set_headers(kwargs['headers'])
        if 'body' in kwargs:
            self.interaction.with_body(kwargs['body'])
        if 'query' in kwargs:
            self.interaction.with_query_parameters(kwargs['query'])
        return self

    def will_respond_with(self, status: int, **kwargs):
        if not self.enabled or not self.interaction:
            return self
        self.interaction.will_respond_with(status)
        if 'body' in kwargs:
            self.interaction.with_body(kwargs['body'])
        if 'headers' in kwargs:
            self.interaction.set_headers(kwargs['headers'])
        return self

    def execute_test(self, test_fn: Callable[[str], Any]) -> Any:
        if not self.enabled or not self.pact:
            if not self.enabled:
                print("Pact is disabled. Skipping contract test execution.")
                return None
            raise ValueError("Pact not setup. Call setup() before execute_test().")
            
        with self.pact.serve() as mock_server:
            result = test_fn(mock_server.url)
            
        pact_dir = Path(os.getcwd()) / 'pacts'
        pact_dir.mkdir(exist_ok=True)
        self.pact.write_file(str(pact_dir))
        return result

    def verify_provider(self, provider: str, pact_source: str, provider_url: str, 
                        state_handler: Optional[Callable] = None):
        """Verifies a provider against a pact source."""
        if not self.enabled:
            print("Pact is disabled. Skipping provider verification.")
            return None

        verifier = Verifier(provider)
        verifier.add_source(pact_source)
        verifier.add_transport(url=provider_url)
        
        # In v3, state_handler can be a function
        return verifier.verify(state_handler=state_handler)

pact_manager = PactManager()
