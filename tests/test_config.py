import os
from pathlib import Path
from quidclaw_mcp.config import QuidClawConfig


def test_default_data_dir():
    config = QuidClawConfig()
    assert config.data_dir == Path.home() / ".quidclaw"


def test_custom_data_dir(tmp_path):
    config = QuidClawConfig(data_dir=tmp_path / "mydata")
    assert config.data_dir == tmp_path / "mydata"


def test_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("QUIDCLAW_DATA_DIR", str(tmp_path / "envdata"))
    config = QuidClawConfig()
    assert config.data_dir == tmp_path / "envdata"


def test_main_bean_path():
    config = QuidClawConfig()
    assert config.main_bean == config.data_dir / "main.bean"


def test_accounts_bean_path():
    config = QuidClawConfig()
    assert config.accounts_bean == config.data_dir / "accounts.bean"


def test_prices_bean_path():
    config = QuidClawConfig()
    assert config.prices_bean == config.data_dir / "prices.bean"


def test_year_dir():
    config = QuidClawConfig()
    path = config.year_dir(2026)
    assert path == config.data_dir / "2026"


def test_month_bean():
    config = QuidClawConfig()
    path = config.month_bean(2026, 3)
    assert path == config.data_dir / "2026" / "2026-03.bean"
