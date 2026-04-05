#!/usr/bin/env python3
"""
MCP Filesystem Server for Snake Game
A Model Context Protocol server providing filesystem operations
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP SDK not installed. Install with: pip install mcp")
    print("This server provides filesystem operations for the Snake Game project.")
    sys.exit(1)

# Create MCP server instance
server = Server("snake-game-filesystem")

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available filesystem tools"""
    return [
        Tool(
            name="read_game_file",
            description="Read a file from the snake game project",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to read (e.g., 'snake.html', 'GAME_GUIDE.md')"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="list_project_files",
            description="List all files in the snake game project",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Optional file pattern (e.g., '*.md', '*.html')"
                    }
                }
            }
        ),
        Tool(
            name="get_game_stats",
            description="Get statistics about the game files",
            inputSchema={}
        ),
        Tool(
            name="update_readme",
            description="Update the README.md with new content",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "New content for README.md"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="create_backup",
            description="Create a backup of game files",
            inputSchema={
                "type": "object",
                "properties": {
                    "backup_name": {
                        "type": "string",
                        "description": "Name for the backup folder"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "read_game_file":
            filename = arguments.get("filename")
            file_path = PROJECT_ROOT / filename

            if not file_path.exists():
                return [TextContent(
                    type="text",
                    text=f"Error: File '{filename}' not found in project"
                )]

            if not file_path.is_file():
                return [TextContent(
                    type="text",
                    text=f"Error: '{filename}' is not a file"
                )]

            content = file_path.read_text(encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"Content of {filename}:\n\n{content}"
            )]

        elif name == "list_project_files":
            pattern = arguments.get("pattern", "*")
            files = list(PROJECT_ROOT.glob(pattern))

            # Filter out directories and hidden files
            file_list = [
                f.name for f in files
                if f.is_file() and not f.name.startswith('.')
            ]

            return [TextContent(
                type="text",
                text=f"Project files matching '{pattern}':\n" +
                     "\n".join(f"  - {f}" for f in sorted(file_list))
            )]

        elif name == "get_game_stats":
            files = list(PROJECT_ROOT.glob("*"))
            file_stats = []

            for f in files:
                if f.is_file() and not f.name.startswith('.'):
                    stat = f.stat()
                    file_stats.append({
                        "name": f.name,
                        "size": f"{stat.st_size} bytes",
                        "modified": stat.st_mtime
                    })

            total_size = sum(f.stat().st_size for f in files if f.is_file())

            stats_text = f"""Snake Game Project Statistics
{'=' * 40}

Total Files: {len(file_stats)}
Total Size: {total_size} bytes

Files:
"""
            for fs in sorted(file_stats, key=lambda x: x["name"]):
                stats_text += f"  • {fs['name']}: {fs['size']}\n"

            return [TextContent(type="text", text=stats_text)]

        elif name == "update_readme":
            content = arguments.get("content")
            readme_path = PROJECT_ROOT / "README.md"

            readme_path.write_text(content, encoding='utf-8')

            return [TextContent(
                type="text",
                text=f"README.md has been updated successfully"
            )]

        elif name == "create_backup":
            backup_name = arguments.get("backup_name", f"backup_{asyncio.get_event_loop().time()}")
            backup_dir = PROJECT_ROOT / "backups" / backup_name

            backup_dir.mkdir(parents=True, exist_ok=True)

            # Copy project files
            for f in PROJECT_ROOT.glob("*"):
                if f.is_file() and not f.name.startswith('.') and f.name != "mcp-filesystem-server.py":
                    import shutil
                    shutil.copy2(f, backup_dir / f.name)

            return [TextContent(
                type="text",
                text=f"Backup created at: {backup_dir}\n" +
                     f"Files backed up: {len(list(backup_dir.glob('*')))}"
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def main():
    """Start the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
