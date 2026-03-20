# QuidClaw MCP

AI 驱动的私人 CFO。

*本地优先。隐私至上。你的数据永远不会离开你的电脑。*

QuidClaw MCP 是一个开源的 [MCP](https://modelcontextprotocol.io/) 服务器，让 AI 助手能够使用 [Beancount](https://beancount.github.io/) 复式记账来管理你的个人财务。把它连接到 Claude、ChatGPT 或任何支持 MCP 的客户端——你就有了一个私人 CFO，帮你追踪每一笔钱、生成报表、把账目打理得井井有条。

> **"午饭花了45，微信付的"** → AI 调用 QuidClaw MCP → 正确的复式记账分录写入你的本地账本。

[English / 英文文档](README.md)

## 为什么选择 QuidClaw MCP

- **隐私优先** — 所有数据以纯文本形式存储在本地。没有服务器，没有云端，没有遥测。一切都不会离开你的电脑。
- **数据由你掌控** — 标准的 Beancount `.bean` 文件，你可以直接阅读、编辑、用 Git 管理。没有厂商锁定，没有私有格式。
- **AI 驱动，而非 AI 依赖** — QuidClaw MCP 只是工具。智能来自你的 AI 客户端。随时可以更换 AI 服务商。

## 工作原理

```
你 ──(自然语言)──→ AI 客户端 ──(MCP)──→ QuidClaw MCP ──→ Beancount
                                                         ↓
                                                 ~/.quidclaw/*.bean
```

- **你** 用自然语言和 AI 助手对话
- **AI** 理解你的意图，决定调用哪些工具
- **QuidClaw MCP** 提供 10 个 MCP 工具，负责读写 Beancount 账本文件
- **数据** 以纯文本形式存在本地——完全由你掌控

QuidClaw MCP 不运行任何 AI 模型。它是 AI 客户端和 Beancount 会计引擎之间的桥梁。

## 功能

- 通过自然语言记录交易
- 多币种支持（CNY、USD、EUR 等）
- 余额查询与对账
- 财务报表（利润表、资产负债表）
- 灵活的 BQL（Beancount 查询语言）查询
- 股票、加密货币、外汇的价格追踪
- 交互式账户初始化

## 前置条件

- **[uv](https://docs.astral.sh/uv/)** — 安装命令：`curl -LsSf https://astral.sh/uv/install.sh | sh`
- **MCP 客户端** — Claude Desktop、Claude Code、Codex 或其他支持 [MCP](https://modelcontextprotocol.io/) 的应用。

## 开始使用

在你的 MCP 客户端配置中添加 QuidClaw MCP。选择你使用的客户端：

<details open>
<summary><b>Claude Desktop</b></summary>

在 `claude_desktop_config.json` 中添加（[Settings → Developer → Edit Config](https://modelcontextprotocol.io/quickstart/user)）：

```json
{
  "mcpServers": {
    "quidclaw-mcp": {
      "command": "uvx",
      "args": ["--python", "3.13", "quidclaw-mcp"]
    }
  }
}
```

重启 Claude Desktop。

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add quidclaw-mcp -- uvx --python 3.13 quidclaw-mcp
```

</details>

<details>
<summary><b>Codex</b></summary>

Codex 在沙箱中运行 MCP 服务器，`uvx` 无法直接使用。需要先安装，再配置：

```bash
uv tool install --python 3.13 quidclaw-mcp
```

在 `~/.codex/config.toml` 中添加：

```toml
[mcp_servers.quidclaw-mcp]
command = "quidclaw-mcp"
args = []
type = "stdio"
```

</details>

<details>
<summary><b>其他 MCP 客户端</b></summary>

QuidClaw MCP 是标准的 MCP 服务器，使用 stdio 传输。配置你的客户端运行：

```
uvx --python 3.13 quidclaw-mcp
```

</details>

配置完成后，客户端会在首次启动时自动下载并运行 QuidClaw MCP。

### 升级

`uvx` 会在客户端每次启动时自动获取最新版本，无需手动升级。

### 从源码安装

适合贡献者或不想使用 [uv](https://docs.astral.sh/uv/) 的用户：

```bash
git clone https://github.com/thorb/quidclaw-mcp.git
cd quidclaw-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

然后在客户端配置中使用完整的 Python 路径：

```json
{
  "command": "/absolute/path/to/quidclaw-mcp/.venv/bin/python",
  "args": ["-m", "quidclaw_mcp"]
}
```

> 将路径替换为在激活的虚拟环境中运行 `which python` 的输出。

## 使用示例

连接后，直接用自然语言和 AI 对话：

> **你：** 帮我初始化账本
>
> **AI：** *（调用 init_ledger）* 已创建 20 个默认账户。你有哪些银行卡？
>
> **你：** 中国银行储蓄卡，招商信用卡
>
> **AI：** *（调用 add_account）* 好了。要设一下初始余额吗？
>
> **你：** 中行卡里有 32000
>
> **AI：** *（调用 add_transaction）* 已记录初始余额。
>
> **你：** 午饭花了45，微信付的
>
> **AI：** *（调用 add_transaction）* 已记录：Expenses:Food 45.00 CNY，来源 Assets:WeChat

## 数据存储

所有数据以纯文本 Beancount `.bean` 文件形式存储在本地：

```
~/.quidclaw/
├── main.bean          # 引用所有其他文件
├── accounts.bean      # 账户定义
├── prices.bean        # 价格信息
└── 2026/
    ├── 2026-01.bean   # 一月交易
    ├── 2026-02.bean   # 二月交易
    └── ...
```

默认目录：`~/.quidclaw/`。自定义目录：

```bash
export QUIDCLAW_DATA_DIR="/path/to/your/ledger"
```

## 许可证

本项目使用 [GNU 通用公共许可证 v2.0](LICENSE)，与 [Beancount](https://github.com/beancount/beancount) 使用相同的许可证。
