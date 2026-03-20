import pytest
import asyncio
import os
from quidclaw_mcp.mcp_server.server import create_server


@pytest.fixture
def server(tmp_path):
    """Create a server with a temporary data directory."""
    os.environ["QUIDCLAW_DATA_DIR"] = str(tmp_path / "testdata")
    srv = create_server()
    yield srv
    del os.environ["QUIDCLAW_DATA_DIR"]


def test_server_has_tools(server):
    """Verify all expected tools are registered."""
    tools = asyncio.run(server.list_tools())
    tool_names = [t.name for t in tools]
    assert "add_transaction" in tool_names
    assert "get_balance" in tool_names
    assert "list_accounts" in tool_names
    assert "add_account" in tool_names
    assert "close_account" in tool_names
    assert "balance_check" in tool_names
    assert "query" in tool_names
    assert "report" in tool_names
    assert "init_ledger" in tool_names
    assert "fetch_prices" in tool_names
    assert len(tool_names) == 10


def test_server_has_prompts(server):
    """Verify prompts are registered."""
    prompts = asyncio.run(server.list_prompts())
    prompt_names = [p.name for p in prompts]
    assert "quidclaw_system" in prompt_names
    assert "init_guide" in prompt_names
    assert "reconcile_guide" in prompt_names
    assert len(prompt_names) == 3
