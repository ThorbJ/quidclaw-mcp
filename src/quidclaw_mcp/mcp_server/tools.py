import datetime
from decimal import Decimal
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.exceptions import ToolError


def register_tools(mcp: FastMCP):

    @mcp.tool()
    async def init_ledger(ctx: Context, accounts: list[dict] | None = None) -> str:
        """Initialize ledger with account template. Pass accounts from AI conversation or omit for defaults."""
        from quidclaw_mcp.core.init import LedgerInitializer
        app = ctx.request_context.lifespan_context
        initializer = LedgerInitializer(app.ledger)
        created = initializer.init_with_template(accounts=accounts)
        if not created:
            return "Ledger already initialized, no new accounts created."
        return f"Created {len(created)} accounts:\n" + "\n".join(f"  - {a}" for a in created)

    @mcp.tool()
    async def add_account(
        ctx: Context, name: str, currencies: list[str] | None = None, open_date: str | None = None
    ) -> str:
        """Open a new account. Example: name='Assets:Bank:BOC', currencies=['CNY']"""
        from quidclaw_mcp.core.accounts import AccountManager
        app = ctx.request_context.lifespan_context
        mgr = AccountManager(app.ledger)
        date = datetime.date.fromisoformat(open_date) if open_date else None
        mgr.add_account(name, currencies=currencies, open_date=date)
        return f"Account opened: {name}"

    @mcp.tool()
    async def close_account(ctx: Context, name: str, close_date: str | None = None) -> str:
        """Close an account."""
        from quidclaw_mcp.core.accounts import AccountManager
        app = ctx.request_context.lifespan_context
        mgr = AccountManager(app.ledger)
        date = datetime.date.fromisoformat(close_date) if close_date else None
        mgr.close_account(name, close_date=date)
        return f"Account closed: {name}"

    @mcp.tool()
    async def list_accounts(ctx: Context, type: str | None = None) -> str:
        """List all accounts, optionally filtered by type (Assets, Liabilities, Income, Expenses, Equity)."""
        from quidclaw_mcp.core.accounts import AccountManager
        app = ctx.request_context.lifespan_context
        mgr = AccountManager(app.ledger)
        accounts = mgr.list_accounts(account_type=type)
        if not accounts:
            return "No accounts found."
        return "\n".join(accounts)

    @mcp.tool()
    async def add_transaction(
        ctx: Context,
        date: str,
        payee: str,
        narration: str,
        postings: list[dict],
    ) -> str:
        """Add a transaction. Each posting: {account, amount (optional), currency (optional)}.
        Omit amount on one posting for auto-balance."""
        from quidclaw_mcp.core.transactions import TransactionManager
        app = ctx.request_context.lifespan_context
        mgr = TransactionManager(app.ledger)
        txn_date = datetime.date.fromisoformat(date)
        mgr.add_transaction(date=txn_date, payee=payee, narration=narration, postings=postings)
        return f"Transaction recorded: {date} {payee} - {narration}"

    @mcp.tool()
    async def get_balance(ctx: Context, account: str | None = None, date: str | None = None) -> str:
        """Get account balance. Omit account for all balances."""
        from quidclaw_mcp.core.balance import BalanceManager
        app = ctx.request_context.lifespan_context
        mgr = BalanceManager(app.ledger)
        if account:
            bal = mgr.get_balance(account)
            if not bal:
                return f"{account}: no balance"
            parts = [f"{amount} {curr}" for curr, amount in bal.items()]
            return f"{account}: {', '.join(parts)}"
        else:
            all_bal = mgr.get_all_balances()
            if not all_bal:
                return "No balances found."
            lines = []
            for acct, currencies in sorted(all_bal.items()):
                parts = [f"{amount} {curr}" for curr, amount in currencies.items()]
                lines.append(f"{acct}: {', '.join(parts)}")
            return "\n".join(lines)

    @mcp.tool()
    async def balance_check(
        ctx: Context, account: str, expected_amount: str, currency: str, date: str | None = None
    ) -> str:
        """Check if account balance matches expected amount (for reconciliation)."""
        from quidclaw_mcp.core.balance import BalanceManager
        app = ctx.request_context.lifespan_context
        mgr = BalanceManager(app.ledger)
        ok, msg = mgr.balance_check(account, Decimal(expected_amount), currency)
        return msg

    @mcp.tool()
    async def query(ctx: Context, bql: str) -> str:
        """Execute a BQL (Beancount Query Language) query. Returns tabular results."""
        from quidclaw_mcp.core.reports import ReportManager
        app = ctx.request_context.lifespan_context
        mgr = ReportManager(app.ledger)
        try:
            columns, rows = mgr.query(bql)
        except Exception as e:
            raise ToolError(f"BQL query error: {e}")
        if not rows:
            return "No results."
        lines = [" | ".join(str(c) for c in columns)]
        lines.append("-" * len(lines[0]))
        for row in rows:
            lines.append(" | ".join(str(v) for v in row))
        return "\n".join(lines)

    @mcp.tool()
    async def report(ctx: Context, type: str, period: str | None = None) -> str:
        """Generate a financial report. Types: income_statement, balance_sheet."""
        from quidclaw_mcp.core.reports import ReportManager
        app = ctx.request_context.lifespan_context
        mgr = ReportManager(app.ledger)
        if type == "income_statement":
            return mgr.income_statement(period=period)
        elif type == "balance_sheet":
            return mgr.balance_sheet()
        else:
            raise ToolError(f"Unknown report type: {type}. Use: income_statement, balance_sheet")

    @mcp.tool()
    async def fetch_prices(ctx: Context, commodities: list[str] | None = None) -> str:
        """Fetch latest prices for commodities and write to ledger."""
        from quidclaw_mcp.core.prices import PriceManager
        app = ctx.request_context.lifespan_context
        mgr = PriceManager(app.ledger)
        try:
            results = mgr.fetch_prices(commodities)
            return "\n".join(f"{r['commodity']}: {r['price']} {r['currency']}" for r in results)
        except NotImplementedError as e:
            raise ToolError(str(e))
