# QuidClaw

Your AI-powered Personal CFO.

*Local-first. Privacy by design. Your data never leaves your machine.*

QuidClaw is an open-source [MCP](https://modelcontextprotocol.io/) server that gives AI assistants the ability to manage your personal finances using [Beancount](https://beancount.github.io/) double-entry accounting. Connect it to Claude, ChatGPT, or any MCP-compatible client — and you have a Personal CFO that tracks every dollar, generates reports, and keeps your books clean.

> **"Lunch was $12, paid with Apple Pay"** → AI calls QuidClaw → proper double-entry transaction recorded in your local ledger.

[Chinese / 中文文档](README.zh-CN.md)

## Why QuidClaw

- **Privacy first** — All data stored locally as plain text. No servers, no cloud, no telemetry. Nothing ever leaves your machine.
- **You own your data** — Standard Beancount `.bean` files you can read, edit, and version control. No vendor lock-in, no proprietary formats.
- **AI-powered, not AI-dependent** — QuidClaw is just tools. The intelligence comes from your AI client. Switch AI providers anytime.

## How It Works

```
You ──(natural language)──→ AI Client ──(MCP)──→ QuidClaw ──→ Beancount
                                                                  ↓
                                                          ~/.quidclaw/*.bean
```

- **You** talk naturally to your AI assistant
- **AI** understands your intent and decides which tools to call
- **QuidClaw** provides 10 MCP tools that read/write Beancount ledger files
- **Data** is stored locally as plain text — you own it completely

QuidClaw doesn't run any AI model. It's a bridge between your AI client and the Beancount accounting engine.

## Features

- Record transactions via natural language
- Multi-currency support (USD, EUR, CNY, etc.)
- Balance queries and reconciliation
- Financial reports (income statement, balance sheet)
- Flexible BQL (Beancount Query Language) queries
- Price tracking for stocks, crypto, and forex
- Interactive account setup for new users

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)** — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **An MCP client** — Claude Desktop, Claude Code, Cursor, Codex, VS Code, or any [MCP-compatible](https://modelcontextprotocol.io/) app.

## Getting Started

Add QuidClaw to your MCP client's config. Pick your client below:

<details open>
<summary><b>Claude Desktop</b></summary>

Add to your `claude_desktop_config.json` ([Settings → Developer → Edit Config](https://modelcontextprotocol.io/quickstart/user)):

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["--python", "3.13", "quidclaw"]
    }
  }
}
```

Restart Claude Desktop.

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add quidclaw -- uvx --python 3.13 quidclaw
```

</details>

<details>
<summary><b>Cursor / Windsurf</b></summary>

Add to your MCP config (Settings → MCP Servers):

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["--python", "3.13", "quidclaw"]
    }
  }
}
```

</details>

<details>
<summary><b>VS Code (Copilot)</b></summary>

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["--python", "3.13", "quidclaw"]
    }
  }
}
```

</details>

<details>
<summary><b>Codex</b></summary>

Codex runs MCP servers in a sandbox, so `uvx` won't work directly. Install first, then configure:

```bash
uv tool install --python 3.13 quidclaw
```

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.quidclaw]
command = "quidclaw"
args = []
type = "stdio"
```

</details>

<details>
<summary><b>Other MCP clients</b></summary>

QuidClaw is a standard MCP server using stdio transport. Configure your client to run:

```
uvx --python 3.13 quidclaw
```

</details>

That's it. Your client will automatically download and run QuidClaw on first launch.

### Upgrade

QuidClaw is downloaded fresh by `uvx` each time your client starts, so you'll always get the latest version automatically.

### Install from source

For contributors or users who prefer not to use [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/thorb/quidclaw.git
cd quidclaw
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Then use the full Python path in your client config:

```json
{
  "command": "/absolute/path/to/quidclaw/.venv/bin/python",
  "args": ["-m", "quidclaw"]
}
```

> Replace the path with the output of `which python` (run inside the activated venv).

## Usage

Once connected, just talk to your AI naturally:

> **You:** Help me set up my ledger
>
> **AI:** *(calls init_ledger)* Created 20 default accounts. What bank accounts do you have?
>
> **You:** Chase checking and Amex credit card
>
> **AI:** *(calls add_account twice)* Done. Want to set initial balances?
>
> **You:** Chase has $5,200
>
> **AI:** *(calls add_transaction)* Recorded opening balance.
>
> **You:** Lunch was $12, paid with Apple Pay
>
> **AI:** *(calls add_transaction)* Recorded: Expenses:Food $12.00 from Assets:ApplePay

## Data Storage

All data is stored locally as plain text Beancount `.bean` files:

```
~/.quidclaw/
├── main.bean          # includes all other files
├── accounts.bean      # account definitions
├── prices.bean        # price directives
└── 2026/
    ├── 2026-01.bean   # January transactions
    ├── 2026-02.bean   # February transactions
    └── ...
```

Default directory: `~/.quidclaw/`. To customize:

```bash
export QUIDCLAW_DATA_DIR="/path/to/your/ledger"
```

## MCP Tools

QuidClaw exposes 10 tools to AI clients:

| Tool | Description |
|------|-------------|
| `init_ledger` | Initialize ledger with default or custom accounts |
| `add_account` | Open a new account |
| `close_account` | Close an account |
| `list_accounts` | List accounts, optionally filtered by type |
| `add_transaction` | Record a transaction |
| `get_balance` | Query account balances |
| `balance_check` | Verify balance for reconciliation |
| `query` | Execute arbitrary BQL queries |
| `report` | Generate income statement or balance sheet |
| `fetch_prices` | Fetch commodity prices |

See [MCP Tools Reference](docs/mcp-tools.md) for full parameter details.

## Development

See [Install from source](#install-from-source) above, then:

```bash
pytest
```

See [Architecture](docs/architecture.md) for design details.

## License

This project is licensed under the [GNU General Public License v2.0](LICENSE), the same license used by [Beancount](https://github.com/beancount/beancount).
