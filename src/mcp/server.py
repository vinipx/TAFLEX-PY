import json
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from src.config.config_manager import config_manager

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

mcp = FastMCP("taflex-py-mcp-server")

@mcp.resource("taflex://config/current")
def get_current_config() -> str:
    """Returns the currently active configuration (secrets masked)"""
    config_dict = config_manager.config.model_dump()
    secrets = ['cloud_key', 'rp_api_key', 'xray_client_secret', 'pact_broker_token']
    
    for key in secrets:
        if config_dict.get(key):
            config_dict[key] = '****'
            
    return json.dumps(config_dict, indent=2)

@mcp.resource("taflex://reports/latest")
def get_latest_report() -> str:
    """Summary of the most recent test execution (requires pytest-json-report or similar, mocked here)"""
    report_path = ROOT_DIR / 'playwright-report' / 'results.json'
    if report_path.exists():
        return report_path.read_text(encoding="utf-8")
    raise ValueError("Latest report not found.")

@mcp.tool()
def list_specs(type: str = None) -> str:
    """List all available test specification files in the tests/ directory."""
    test_dir = ROOT_DIR / 'tests'
    if type:
        test_dir = test_dir / type
        
    specs = []
    if test_dir.exists():
        for path in test_dir.rglob("*"):
            if path.is_file() and (path.name.endswith(".py") or path.name.endswith(".feature")):
                specs.append(str(path.relative_to(ROOT_DIR)))
                
    return json.dumps(specs, indent=2)

@mcp.tool()
def get_locator(page: str, mode: str = 'web') -> str:
    """Retrieve the content of a specific locator JSON file."""
    locator_path = ROOT_DIR / 'src' / 'resources' / 'locators' / mode / f"{page}.json"
    if locator_path.exists():
        return locator_path.read_text(encoding='utf-8')
    raise ValueError(f"Locator not found for page '{page}' in mode '{mode}'")

@mcp.tool()
def list_locators(mode: str = 'web') -> str:
    """List all available locator files for a given mode."""
    locators_dir = ROOT_DIR / 'src' / 'resources' / 'locators' / mode
    locators = []
    if locators_dir.exists():
        for path in locators_dir.iterdir():
            if path.suffix == '.json':
                locators.append(path.stem)
    return json.dumps(locators, indent=2)

@mcp.tool()
async def run_test(spec_path: str, headed: bool = False) -> str:
    """Execute a specific test file using pytest."""
    import subprocess
    cmd = ['pytest', spec_path]
    if headed:
        cmd.extend(['--headed']) # Requires pytest-playwright or custom fixture support
        
    process = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    return f"Exit Code: {process.returncode}\n\nSTDOUT:\n{stdout.decode()}\n\nSTDERR:\n{stderr.decode()}"

if __name__ == "__main__":
    mcp.run()
