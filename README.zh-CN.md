# QuidClaw

AI 驱动的私人 CFO。

*本地优先。隐私至上。你的数据永远不会离开你的电脑。*

QuidClaw 是一个开源的 [MCP](https://modelcontextprotocol.io/) 服务器，让 AI 助手能够使用 [Beancount](https://beancount.github.io/) 复式记账来管理你的个人财务。把它连接到 Claude、ChatGPT 或任何支持 MCP 的客户端——你就有了一个私人 CFO，帮你追踪每一笔钱、生成报表、把账目打理得井井有条。

> **"午饭花了45，微信付的"** → AI 调用 QuidClaw → 正确的复式记账分录写入你的本地账本。

[English / 英文文档](README.md)

## 为什么选择 QuidClaw

- **隐私优先** — 所有数据以纯文本形式存储在本地。没有服务器，没有云端，没有遥测。一切都不会离开你的电脑。
- **数据由你掌控** — 标准的 Beancount `.bean` 文件，你可以直接阅读、编辑、用 Git 管理。没有厂商锁定，没有私有格式。
- **AI 驱动，而非 AI 依赖** — QuidClaw 只是工具。智能来自你的 AI 客户端。随时可以更换 AI 服务商。

## 工作原理

```
你 ──(自然语言)──→ AI 客户端 ──(MCP)──→ QuidClaw ──→ Beancount
                                                         ↓
                                                 ~/.quidclaw/*.bean
```

- **你** 用自然语言和 AI 助手对话
- **AI** 理解你的意图，决定调用哪些工具
- **QuidClaw** 提供 10 个 MCP 工具，负责读写 Beancount 账本文件
- **数据** 以纯文本形式存在本地——完全由你掌控

QuidClaw 不运行任何 AI 模型。它是 AI 客户端和 Beancount 会计引擎之间的桥梁。

## 功能

- 通过自然语言记录交易
- 多币种支持（CNY、USD、EUR 等）
- 余额查询与对账
- 财务报表（利润表、资产负债表）
- 灵活的 BQL（Beancount 查询语言）查询
- 股票、加密货币、外汇的价格追踪
- 交互式账户初始化

## 前置条件

| 条件 | 说明 |
|------|------|
| **Python 3.10 – 3.13** | 运行 `python3 --version` 检查版本。Beancount 暂不支持 Python 3.14+。 |
| **MCP 客户端** | 任何支持 [Model Context Protocol](https://modelcontextprotocol.io/) 的应用。详见下方配置方式。 |

## 安装

一条命令安装 QuidClaw，无需克隆仓库、创建虚拟环境：

```bash
uvx quidclaw
```

> [`uvx`](https://docs.astral.sh/uv/guides/tools/) 可以直接从 [PyPI](https://pypi.org/project/quidclaw/) 运行 Python 包。如果还没有安装，运行 `curl -LsSf https://astral.sh/uv/install.sh | sh`。

### 配置你的 MCP 客户端

选择你使用的客户端，按照说明配置：

<details>
<summary><b>Claude Desktop</b></summary>

在 `claude_desktop_config.json` 中添加（[Settings → Developer → Edit Config](https://modelcontextprotocol.io/quickstart/user)）：

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["quidclaw"]
    }
  }
}
```

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add quidclaw -- uvx quidclaw
```

</details>

<details>
<summary><b>Cursor / Windsurf</b></summary>

在 MCP 配置中添加（Settings → MCP Servers）：

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["quidclaw"]
    }
  }
}
```

</details>

<details>
<summary><b>Codex</b></summary>

在 `~/.codex/config.toml` 中添加（或运行 `codex mcp add`）：

```toml
[mcp_servers.quidclaw]
command = "uvx"
args = ["quidclaw"]
type = "stdio"
```

</details>

<details>
<summary><b>VS Code (Copilot)</b></summary>

在 `.vscode/mcp.json` 中添加：

```json
{
  "servers": {
    "quidclaw": {
      "command": "uvx",
      "args": ["quidclaw"]
    }
  }
}
```

</details>

<details>
<summary><b>其他 MCP 客户端</b></summary>

QuidClaw 是标准的 MCP 服务器，使用 stdio 传输。配置你的客户端运行：

```
uvx quidclaw
```

</details>

### 一键配置多个客户端

如果你同时使用多个 MCP 客户端，可以用 [add-mcp](https://github.com/nicepkg/add-mcp) 一次性配置：

```bash
npx add-mcp --uvx quidclaw -a claude-code -a claude-desktop -a cursor -a codex
```

> 去掉不需要的 `-a <客户端>`，或添加其他客户端如 `-a zed`、`-a vscode`、`-a windsurf`。

### 常见问题

如果 `uvx quidclaw` 报 `beancount` 构建错误，可能是你的默认 Python 版本为 3.14+。指定受支持的版本即可：

```bash
uvx --python 3.13 quidclaw
```

## 从源码安装（开发用）

```bash
git clone https://github.com/thorb/quidclaw.git
cd quidclaw
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

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
