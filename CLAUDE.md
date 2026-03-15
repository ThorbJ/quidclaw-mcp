# QuidClaw

Personal finance AI Agent. MCP Server powered by Beancount V3.

## Architecture

Layered design — two layers:

- `src/quidclaw/core/` — Pure business logic. Depends on Beancount, NOT on MCP. Every financial operation lives here.
- `src/quidclaw/mcp_server/` — Thin MCP adapter. Translates MCP tool calls into core function calls. No business logic here.

This separation exists so we can add other adapters (e.g., OpenClaw) without touching core logic.

## Key Files

| File | Purpose |
|------|---------|
| `src/quidclaw/config.py` | `QuidClawConfig` dataclass — data directory paths |
| `src/quidclaw/core/ledger.py` | `Ledger` — init, load, append to .bean files |
| `src/quidclaw/core/accounts.py` | `AccountManager` — open/close/list accounts |
| `src/quidclaw/core/transactions.py` | `TransactionManager` — add transactions to monthly files |
| `src/quidclaw/core/balance.py` | `BalanceManager` — balance queries and assertions |
| `src/quidclaw/core/reports.py` | `ReportManager` — BQL queries and report generation |
| `src/quidclaw/core/prices.py` | `PriceManager` — write price directives |
| `src/quidclaw/core/init.py` | `LedgerInitializer` — default account templates |
| `src/quidclaw/mcp_server/server.py` | `create_server()` — FastMCP instance with lifespan |
| `src/quidclaw/mcp_server/tools.py` | MCP Tool definitions (10 tools) |
| `src/quidclaw/mcp_server/prompts.py` | MCP Prompts (personality, guides) |
| `src/quidclaw/mcp_server/resources.py` | MCP Resources (account tree, config) |

## Tech Stack

- Python >= 3.10
- `beancount` V3 (3.x) — accounting engine
- `beanquery` — BQL query execution
- `beanprice` — price fetching (optional)
- `mcp` — MCP Python SDK (FastMCP)

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest                            # run all tests
pytest tests/core/                # core logic tests only
pytest tests/mcp_server/          # MCP adapter tests only
pytest tests/test_integration.py  # end-to-end workflow
```

## Data Directory

Default: `~/.quidclaw/`. Override: `QUIDCLAW_DATA_DIR` env var or pass `data_dir` to `QuidClawConfig`.

```
~/.quidclaw/
├── main.bean          # includes all other files
├── accounts.bean      # Open/Close directives
├── prices.bean        # Price directives
└── YYYY/YYYY-MM.bean  # Transactions by month
```

## How to Add a New MCP Tool

1. Add core logic in `src/quidclaw/core/<module>.py` with tests in `tests/core/`
2. Add tool wrapper in `src/quidclaw/mcp_server/tools.py` inside `register_tools()`
3. Pattern:
   ```python
   @mcp.tool()
   async def my_tool(ctx: Context, param: str) -> str:
       app = ctx.request_context.lifespan_context  # → AppContext
       mgr = SomeManager(app.ledger)
       result = mgr.some_method(param)
       return format_result(result)
   ```

## Conventions

- All core classes take a `Ledger` instance in their constructor
- Beancount directives are written as plain text strings appended to .bean files
- Transactions go into monthly files (`YYYY/YYYY-MM.bean`), auto-included in `main.bean`
- Multi-currency open directives use comma-separated currencies: `2026-01-01 open Assets:Bank CNY,USD`
- Tests use `tmp_path` fixture for isolated data directories
- Use `ToolError` (from `mcp.server.fastmcp.exceptions`) for user-facing errors in MCP tools
- FastMCP uses `instructions=` not `description=` in constructor

## Beancount V3 API Notes

```python
from beancount import loader
entries, errors, options = loader.load_file("path.bean")

from beancount.core import data
# data.Open, data.Close, data.Transaction, data.Balance, data.Price

from beancount.core import realization
real_root = realization.realize(entries)
real_account = realization.get(real_root, "Assets:Bank:BOC")
# real_account.balance → Inventory of positions
# realization.iter_children(real_root) → yields RealAccount objects (not tuples)

from beanquery.query import run_query
columns, rows = run_query(entries, options, "SELECT ...")
# columns: tuple of Column objects with .name attribute
# rows: list of tuples
# BQL queries operate at posting level — use DISTINCT to deduplicate
```
