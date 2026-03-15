# MCP Tools Reference

## Transaction Tools

### add_transaction

Add a double-entry transaction to the ledger.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| date | string (ISO) | yes | Transaction date, e.g. "2026-03-15" |
| payee | string | yes | Who was paid |
| narration | string | yes | What for |
| postings | list[dict] | yes | Account entries (see below) |

Each posting: `{account: str, amount?: str, currency?: str}`. Omit amount on one posting for auto-balance.

**Example:**
```json
{
  "date": "2026-03-15",
  "payee": "McDonald's",
  "narration": "Lunch",
  "postings": [
    {"account": "Expenses:Food", "amount": "45.00", "currency": "CNY"},
    {"account": "Assets:WeChat"}
  ]
}
```

## Account Tools

### add_account

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Full account name (e.g. "Assets:Bank:BOC") |
| currencies | list[string] | no | Accepted currencies |
| open_date | string (ISO) | no | Account opening date (default: today) |

### close_account

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Account to close |
| close_date | string (ISO) | no | Closing date (default: today) |

### list_accounts

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | no | Filter: Assets, Liabilities, Income, Expenses, Equity |

## Balance Tools

### get_balance

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| account | string | no | Specific account (omit for all) |
| date | string (ISO) | no | Balance as of date |

### balance_check

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| account | string | yes | Account to check |
| expected_amount | string | yes | Expected balance amount |
| currency | string | yes | Currency code |
| date | string (ISO) | no | As of date |

## Query & Report Tools

### query

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| bql | string | yes | BQL query string |

**Example BQL queries:**
- `SELECT account, sum(position) WHERE account ~ 'Expenses' GROUP BY account`
- `SELECT DISTINCT date, payee, narration WHERE year = 2026 AND month = 3`
- `SELECT account, sum(position) WHERE account ~ 'Assets' GROUP BY account`

### report

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | yes | `income_statement` or `balance_sheet` |
| period | string | no | Period filter |

## Other Tools

### init_ledger

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accounts | list[dict] | no | Custom accounts `[{name, currencies?}]`. Omit for defaults. |

### fetch_prices

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| commodities | list[string] | no | Which commodities to fetch prices for |
