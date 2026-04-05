# MCP Filesystem 工具使用指南

## 概述

本项目包含一个 Model Context Protocol (MCP) 服务器，提供项目文件系统操作能力。通过 MCP 协议，AI 助手可以安全地读取、管理和操作项目文件。

## 安装

### 前置要求

```bash
# 安装 MCP SDK
pip install mcp
```

### 配置 MCP 客户端

在支持 MCP 的客户端（如 Claude Desktop）配置文件中添加：

```json
{
  "mcpServers": {
    "snake-filesystem": {
      "command": "python3",
      "args": ["/path/to/snake-game/mcp-filesystem-server.py"],
      "description": "Filesystem operations for Snake Game"
    }
  }
}
```

## 可用工具

### 1. read_game_file

读取项目中的文件内容。

**参数：**
- `filename` (string): 文件名，如 "snake.html", "GAME_GUIDE.md"

**示例：**
```python
# 读取游戏主文件
read_game_file(filename="snake.html")
```

**返回：** 文件的完整文本内容

---

### 2. list_project_files

列出项目中的所有文件。

**参数：**
- `pattern` (string, optional): 文件模式，如 "*.md", "*.html"

**示例：**
```python
# 列出所有文件
list_project_files()

# 只列出 Markdown 文件
list_project_files(pattern="*.md")
```

**返回：** 匹配的文件列表

---

### 3. get_game_stats

获取项目文件统计信息。

**参数：** 无

**返回：**
- 总文件数
- 总大小
- 每个文件的详细统计

---

### 4. update_readme

更新 README.md 文件。

**参数：**
- `content` (string): README 的新内容

**示例：**
```python
update_readme(content="# New README content\n...")
```

**返回：** 更新确认消息

---

### 5. create_backup

创建项目文件的备份。

**参数：**
- `backup_name` (string, optional): 备份文件夹名称

**示例：**
```python
# 创建自动命名的备份
create_backup()

# 创建命名备份
create_backup(backup_name="backup-v1.0")
```

**返回：** 备份位置和文件数量

---

## 使用场景

### 场景 1：AI 代码审查

AI 可以读取游戏代码并提供建议：
```python
# AI 读取游戏代码
content = read_game_file("snake.html")
# AI 分析并提供优化建议
```

### 场景 2：自动文档更新

```python
# 获取项目统计
stats = get_game_stats()
# AI 根据统计信息更新 README
update_readme(content=new_readme_content)
```

### 场景 3：版本管理

```python
# 在重大更改前创建备份
create_backup(backup_name="before-refactor")
```

### 场景 4：项目分析

```python
# 列出所有 HTML 文件
html_files = list_project_files(pattern="*.html")
# 读取并分析每个文件
for file in html_files:
    content = read_game_file(file)
    # AI 分析代码
```

## 安全特性

- **项目隔离**: 服务器只能访问项目根目录及其子目录
- **只读操作**: 默认工具主要用于读取，写入操作需要明确意图
- **文件验证**: 所有文件操作都进行路径验证，防止路径遍历攻击
- **错误处理**: 完善的异常捕获和错误消息返回

## 扩展开发

### 添加新工具

1. 在 `mcp-filesystem-server.py` 中添加新的工具定义：

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    # 添加新工具到返回列表
    return [
        # ... 现有工具
        Tool(
            name="your_new_tool",
            description="Tool description",
            inputSchema={...}
        )
    ]
```

2. 在 `call_tool` 函数中添加处理逻辑：

```python
@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "your_new_tool":
        # 实现工具逻辑
        return [TextContent(type="text", text="result")]
```

## 测试

### 本地测试服务器

```bash
# 启动服务器
python3 mcp-filesystem-server.py

# 在另一个终端测试（使用 MCP 客户端）
```

### 集成测试

使用支持 MCP 的 AI 客户端连接服务器，然后调用工具测试。

## 故障排除

### 问题：MCP SDK 未安装

**错误：** `ModuleNotFoundError: No module named 'mcp'`

**解决：**
```bash
pip install mcp
```

### 问题：权限错误

**错误：** `Permission denied when reading file`

**解决：** 确保服务器有权限读取项目文件

### 问题：连接超时

**解决：**
1. 检查服务器是否正在运行
2. 验证客户端配置路径是否正确
3. 查看 MCP 服务器日志

## 配置文件说明

### .mcprc.json

MCP 客户端配置文件，定义可用的 MCP 服务器。

```json
{
  "mcpServers": {
    "snake-filesystem": {
      "command": "python3",
      "args": ["mcp-filesystem-server.py"],
      "description": "Filesystem operations for Snake Game",
      "enabled": true
    }
  }
}
```

## 相关资源

- [MCP 规范](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [项目主文档](./CLAUDE.md)
- [游戏使用指南](./GAME_GUIDE.md)

---

**最后更新：** 2025-04-05
