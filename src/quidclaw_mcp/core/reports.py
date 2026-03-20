from beanquery.query import run_query
from quidclaw_mcp.core.ledger import Ledger


class ReportManager:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger

    def query(self, bql: str) -> tuple[list[str], list[tuple]]:
        """Execute a BQL query. Returns (column_names, rows)."""
        entries, errors, options = self.ledger.load()
        columns, rows = run_query(entries, options, bql)
        col_names = [col.name for col in columns]
        result_rows = [tuple(row) for row in rows]
        return col_names, result_rows

    def income_statement(self, period: str | None = None) -> str:
        """Generate a text income statement."""
        if period:
            bql = f"SELECT account, sum(position) WHERE account ~ 'Income|Expenses' AND date >= {period} GROUP BY account ORDER BY account"
        else:
            bql = "SELECT account, sum(position) WHERE account ~ 'Income|Expenses' GROUP BY account ORDER BY account"
        columns, rows = self.query(bql)
        return self._format_table("Income Statement", columns, rows)

    def balance_sheet(self) -> str:
        """Generate a text balance sheet."""
        bql = "SELECT account, sum(position) WHERE account ~ 'Assets|Liabilities|Equity' GROUP BY account ORDER BY account"
        columns, rows = self.query(bql)
        return self._format_table("Balance Sheet", columns, rows)

    def _format_table(self, title: str, columns: list[str], rows: list[tuple]) -> str:
        """Format query results as a readable text table."""
        lines = [title, "=" * len(title)]
        if not rows:
            lines.append("(no data)")
            return "\n".join(lines)
        header = " | ".join(str(c) for c in columns)
        lines.append(header)
        lines.append("-" * len(header))
        for row in rows:
            lines.append(" | ".join(str(v) for v in row))
        return "\n".join(lines)
