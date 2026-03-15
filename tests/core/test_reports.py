import datetime
from quidclaw.config import QuidClawConfig
from quidclaw.core.ledger import Ledger
from quidclaw.core.accounts import AccountManager
from quidclaw.core.transactions import TransactionManager
from quidclaw.core.reports import ReportManager


def make_ledger_with_data(tmp_path):
    config = QuidClawConfig(data_dir=tmp_path / "testdata")
    ledger = Ledger(config)
    ledger.init()
    acct = AccountManager(ledger)
    acct.add_account("Assets:Bank:BOC", currencies=["CNY"], open_date=datetime.date(2026, 1, 1))
    acct.add_account("Expenses:Food", open_date=datetime.date(2026, 1, 1))
    acct.add_account("Income:Salary", open_date=datetime.date(2026, 1, 1))
    txn = TransactionManager(ledger)
    txn.add_transaction(
        date=datetime.date(2026, 1, 15), payee="Company", narration="Salary",
        postings=[
            {"account": "Assets:Bank:BOC", "amount": "10000.00", "currency": "CNY"},
            {"account": "Income:Salary", "amount": "-10000.00", "currency": "CNY"},
        ],
    )
    txn.add_transaction(
        date=datetime.date(2026, 1, 20), payee="Restaurant", narration="Dinner",
        postings=[
            {"account": "Expenses:Food", "amount": "200.00", "currency": "CNY"},
            {"account": "Assets:Bank:BOC", "amount": "-200.00", "currency": "CNY"},
        ],
    )
    return ledger


def test_query_bql(tmp_path):
    ledger = make_ledger_with_data(tmp_path)
    reports = ReportManager(ledger)
    columns, rows = reports.query("SELECT account, sum(position) WHERE account ~ 'Expenses' GROUP BY account")
    assert len(rows) >= 1


def test_income_statement(tmp_path):
    ledger = make_ledger_with_data(tmp_path)
    reports = ReportManager(ledger)
    result = reports.income_statement()
    assert "Income" in result or "Expenses" in result


def test_balance_sheet(tmp_path):
    ledger = make_ledger_with_data(tmp_path)
    reports = ReportManager(ledger)
    result = reports.balance_sheet()
    assert "Assets" in result
