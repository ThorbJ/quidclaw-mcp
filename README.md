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

| Requirement | Description |
|-------------|-------------|
| **Python 3.10+** | QuidClaw is a Python package. Check with `python3 --version`. |
| **An MCP client** | Any app that supports the [Model Context Protocol](https://modelcontextprotocol.io/). See setup options below. |

## Installation

```bash
git clone https://github.com/thorb/quidclaw.git
cd quidclaw

python3 -m venv .venv
source .venv/bin/activate    # macOS / Linux
# .venv\Scripts\activate     # Windows

pip install -e .
```

After installation, note the full path to the Python executable — you'll need it for setup:

```bash
which python
# Example output: /home/user/quidclaw/.venv/bin/python
```

## Setup

Choose the setup that matches your MCP client.

### Option A: Claude Desktop (recommended for most users)

[Claude Desktop](https://claude.ai/download) is a graphical AI chat application for macOS and Windows.

**Step 1.** Open Claude Desktop, click the **Claude** menu in the menu bar (not inside the chat window), then select **Settings**.

**Step 2.** In the Settings window, go to the **Developer** tab and click **Edit Config**. This opens the configuration file `claude_desktop_config.json`.

| OS | Config file location |
|----|---------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Step 3.** Add `quidclaw` to the `mcpServers` section:

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "/absolute/path/to/quidclaw/.venv/bin/python",
      "args": ["-m", "quidclaw"]
    }
  }
}
```

> Replace the `command` value with the actual path from `which python` above.

**Step 4.** Quit Claude Desktop completely and restart it. You should see an MCP indicator (hammer icon) at the bottom of the chat input. Click it to verify QuidClaw's tools are listed.

### Option B: Claude Code (for developers)

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is a command-line AI assistant.

```bash
claude mcp add quidclaw -- /absolute/path/to/quidclaw/.venv/bin/python -m quidclaw
```

Restart Claude Code or start a new session. QuidClaw's tools will be available.

### Option C: Other MCP clients

QuidClaw is a standard MCP server using stdio transport. Any MCP-compatible client can use it by running:

```
/absolute/path/to/quidclaw/.venv/bin/python -m quidclaw
```

Refer to your client's documentation for how to add MCP servers.

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

```bash
git clone https://github.com/thorb/quidclaw.git
cd quidclaw
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

See [Architecture](docs/architecture.md) for design details.

## License

This project is licensed under the [GNU General Public License v2.0](LICENSE), the same license used by [Beancount](https://github.com/beancount/beancount).
