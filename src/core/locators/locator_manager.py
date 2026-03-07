import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LocatorManager:
    """Manages hierarchical locators using a cascading inheritance model."""

    def __init__(self, mode: str) -> None:
        self.locators: Dict[str, str] = {}
        # Assuming run from project root, fallback logic can be added if needed
        self.base_path = Path("src/resources/locators").resolve()
        self.current_page: Optional[str] = None
        self.mode = mode

    def load(self, page_name: Optional[str] = None) -> None:
        """Loads and merges locators for the current execution mode and an optional specific page."""
        self.current_page = page_name

        global_locators = self._read_json("global.json")
        mode_locators = self._read_json(f"{self.mode}/common.json")

        page_locators = {}
        if page_name:
            page_locators = self._read_json(f"{self.mode}/{page_name}.json")

        self.locators = {**global_locators, **mode_locators, **page_locators}
        logger.info(f"Loaded {len(self.locators)} locators for mode '{self.mode}' and page '{page_name}'")
        if len(self.locators) == 0:
            logger.warning(f"⚠️ No locators found for {self.mode}/{page_name}. Check file paths in {self.base_path}")

    def resolve(self, logical_name: str) -> str:
        """Resolves a logical name to its underlying selector string."""
        return self.locators.get(logical_name, logical_name)

    def _read_json(self, relative_path: str) -> Dict[str, str]:
        file_path = self.base_path / relative_path
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"⚠️ Failed to parse locator file: {file_path}. Error: {e}")
        return {}
