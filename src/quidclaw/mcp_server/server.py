from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from quidclaw.config import QuidClawConfig
from quidclaw.core.ledger import Ledger


class AppContext:
    def __init__(self, config: QuidClawConfig, ledger: Ledger):
        self.config = config
        self.ledger = ledger


@asynccontextmanager
async def app_lifespan(server: FastMCP):
    config = QuidClawConfig()
    ledger = Ledger(config)
    ledger.init()
    yield AppContext(config=config, ledger=ledger)


def create_server() -> FastMCP:
    mcp = FastMCP(
        "QuidClaw",
        instructions="Personal finance AI Agent powered by Beancount",
        lifespan=app_lifespan,
    )

    from quidclaw.mcp_server.tools import register_tools
    from quidclaw.mcp_server.prompts import register_prompts
    from quidclaw.mcp_server.resources import register_resources

    register_tools(mcp)
    register_prompts(mcp)
    register_resources(mcp)

    return mcp
