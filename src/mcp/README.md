# Taflex MCP Server

This module implements a Model Context Protocol (MCP) server for the Taflex TS framework. It allows AI agents and assistants to interact with your testing framework directly.

## Features

### Tools
- `list_specs`: List all available test specification files.
- `list_locators`: List all available locator files for a specific mode (web/mobile).
- `get_locator`: Retrieve the contents of a specific locator JSON file.
- `run_test`: Execute a specific test file using Playwright.

### Resources
- `taflex://config/current`: Access the current framework configuration (secrets are masked).
- `taflex://reports/latest`: Access the latest test execution report summary.

## Configuration

To use this server with AI agents, you need to point your MCP client to `src/mcp/server.ts`.

### Gemini CLI
Run the following command:

```bash
gemini mcp add taflex node /absolute/path/to/taflex-ts/src/mcp/server.ts
```

### Claude Desktop / VS Code (Cline)
Add the following to your configuration file (e.g., `claude_desktop_config.tson`, `cline_mcp_settings.tson`):

``.tson
{
  "mcpServers": {
    "taflex": {
      "command": "node",
      "args": ["/absolute/path/to/taflex-ts/src/mcp/server.ts"]
    }
  }
}
```

### Cursor
Add a new MCP server in **Settings > Features > MCP**:
- **Name**: `taflex`
- **Type**: `command`
- **Command**: `node /absolute/path/to/taflex-ts/src/mcp/server.ts`

### OpenCode
Add to `opencode.tson`:

``.tson
{
  "mcpServers": {
    "taflex": {
      "type": "local",
      "command": "node",
      "args": ["/absolute/path/to/taflex-ts/src/mcp/server.ts"],
      "enabled": true
    }
  }
}
```

Replace `/absolute/path/to/taflex-ts` with the actual path to your project.

## Development

To start the server manually for testing:

```bash
npm run mcp
```

The server uses standard input/output (stdio) for communication.
