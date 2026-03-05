import json
from src.core.locators.locator_manager import LocatorManager

def test_locator_manager_loads_hierarchically(tmp_path, monkeypatch):
    # Mock config_manager using monkeypatch
    import src.core.locators.locator_manager as lm
    
    # Create mock locator files
    base_dir = tmp_path / "src" / "resources" / "locators"
    base_dir.mkdir(parents=True)
    
    global_json = base_dir / "global.json"
    global_json.write_text(json.dumps({"login_btn": "#global-login", "header": "#header"}))
    
    mode_dir = base_dir / "web"
    mode_dir.mkdir()
    common_json = mode_dir / "common.json"
    common_json.write_text(json.dumps({"login_btn": "#web-login", "footer": "#footer"}))
    
    page_json = mode_dir / "login.json"
    page_json.write_text(json.dumps({"login_btn": "#page-login", "username": "#user"}))

    class MockConfigManager:
        def get(self, key):
            if key == "execution_mode":
                return "web"
            return None

    monkeypatch.setattr(lm, "config_manager", MockConfigManager())
    
    manager = LocatorManager()
    manager.base_path = base_dir

    manager.load("login")

    # verify inheritance: page > mode > global
    assert manager.resolve("login_btn") == "#page-login"
    assert manager.resolve("header") == "#header"
    assert manager.resolve("footer") == "#footer"
    assert manager.resolve("username") == "#user"
    assert manager.resolve("unknown") == "unknown"
