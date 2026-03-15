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
| **Python 3.10+** | QuidClaw 是一个 Python 包。运行 `python3 --version` 检查版本。 |
| **MCP 客户端** | 任何支持 [Model Context Protocol](https://modelcontextprotocol.io/) 的应用。详见下方配置方式。 |

## 安装

```bash
git clone https://github.com/thorb/quidclaw.git
cd quidclaw

python3 -m venv .venv
source .venv/bin/activate    # macOS / Linux
# .venv\Scripts\activate     # Windows

pip install -e .
```

安装后，记下 Python 可执行文件的完整路径——配置时需要用到：

```bash
which python
# 示例输出: /home/user/quidclaw/.venv/bin/python
```

## 配置

根据你使用的 MCP 客户端选择对应的配置方式。

### 方式 A：Claude Desktop（推荐大多数用户使用）

[Claude Desktop](https://claude.ai/download) 是一个图形界面的 AI 聊天应用，支持 macOS 和 Windows。

**第 1 步.** 打开 Claude Desktop，点击菜单栏中的 **Claude** 菜单（不是聊天窗口内的设置），选择 **Settings**。

**第 2 步.** 在 Settings 窗口中，进入 **Developer** 标签页，点击 **Edit Config**。这会打开配置文件 `claude_desktop_config.json`。

| 系统 | 配置文件位置 |
|------|-------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**第 3 步.** 在 `mcpServers` 中添加 `quidclaw`：

```json
{
  "mcpServers": {
    "quidclaw": {
      "command": "/absolute/path/to/quidclaw/.venv/bin/python",
      "args": ["-m", "quidclaw"]
    }
  }
}
```

> 将 `command` 的值替换为上面 `which python` 输出的实际路径。

**第 4 步.** 完全退出 Claude Desktop 并重新启动。你应该能在聊天输入框底部看到一个 MCP 指示器（锤子图标）。点击它可以确认 QuidClaw 的工具已加载。

### 方式 B：Claude Code（适合开发者）

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是命令行 AI 助手。

```bash
claude mcp add quidclaw -- /absolute/path/to/quidclaw/.venv/bin/python -m quidclaw
```

重启 Claude Code 或开始新会话，QuidClaw 的工具即可使用。

### 方式 C：其他 MCP 客户端

QuidClaw 是标准的 MCP 服务器，使用 stdio 传输。任何兼容 MCP 的客户端都可以通过以下命令启动：

```
/absolute/path/to/quidclaw/.venv/bin/python -m quidclaw
```

具体配置方式请参考你所使用客户端的文档。

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
