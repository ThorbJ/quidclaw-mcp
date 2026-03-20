import json
from mcp.server.fastmcp import FastMCP, Context


def register_resources(mcp: FastMCP):

    @mcp.resource("quidclaw://accounts")
    async def account_tree(ctx: Context) -> str:
        """Current account structure."""
        from quidclaw_mcp.core.accounts import AccountManager
        app = ctx.request_context.lifespan_context
        mgr = AccountManager(app.ledger)
        accounts = mgr.list_accounts()
        return "\n".join(accounts) if accounts else "(no accounts)"

    @mcp.resource("quidclaw://config")
    async def config_resource(ctx: Context) -> str:
        """Current QuidClaw MCP configuration."""
        app = ctx.request_context.lifespan_context
        return json.dumps({
            "data_dir": str(app.config.data_dir),
            "main_bean": str(app.config.main_bean),
        }, indent=2)
