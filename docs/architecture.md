# Architecture

## Layered Design

```
┌─────────────────────────────────────┐
│  AI Client (Claude Desktop / GPT)   │
├─────────────────────────────────────┤
│  MCP Protocol (stdio / HTTP)        │
├─────────────────────────────────────┤
│  mcp_server/    (adapter layer)     │
│  ├── tools.py   (10 MCP Tools)     │
│  ├── prompts.py (3 MCP Prompts)    │
│  └── resources.py (2 Resources)    │
├─────────────────────────────────────┤
│  core/          (business logic)    │
│  ├── ledger.py                      │
│  ├── accounts.py                    │
│  ├── transactions.py                │
│  ├── balance.py                     │
│  ├── reports.py                     │
│  ├── prices.py                      │
│  └── init.py                        │
├─────────────────────────────────────┤
│  Beancount V3   (accounting engine) │
│  beanquery      (query engine)      │
│  beanprice      (price fetching)    │
├─────────────────────────────────────┤
│  ~/.quidclaw/*.bean  (plain text)   │
└─────────────────────────────────────┘
```

## Key Principle

`core/` has zero MCP dependency. Every financial operation is a plain Python function that takes a `Ledger` and returns data. The `mcp_server/` layer is a thin adapter that:

1. Receives MCP tool calls
2. Converts string parameters to Python types
3. Calls the appropriate core function
4. Formats the result as a string for the AI

This makes it easy to add other adapters (OpenClaw, REST API, CLI) without touching business logic.

## Data Flow

```
User: "Lunch was $12, paid with Apple Pay"
  → AI understands: Expenses:Food 12 USD from Assets:ApplePay
  → AI calls MCP tool: add_transaction(...)
  → tools.py: converts params, calls TransactionManager.add_transaction()
  → transactions.py: writes to ~/.quidclaw/2026/2026-03.bean
  → Beancount validates on next load()
```

## File Organization

Transactions are split by month (`YYYY/YYYY-MM.bean`) and auto-included in `main.bean`. This keeps files manageable and makes git diffs readable.

Account definitions live in `accounts.bean`. Prices in `prices.bean`. The `main.bean` file only contains `option` and `include` directives.
