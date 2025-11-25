import asyncio
import json
import sys
import os
import io
import anyio

# Disable symlinks for HuggingFace Hub to avoid WinError 1314 on Windows
# This must be set before any library using huggingface_hub is imported/used
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .pdf_processor import PdfProcessor

class SemanticPdfReaderServer:
    def __init__(self):
        self.processor = PdfProcessor()
        self.server = Server("mcp-semantic-pdf-reader")
        
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return [
                Tool(
                    name="read_pdf_structure",
                    description="Read a PDF file and return its content as structured Markdown. Preserves layout, tables, and headers.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Absolute path to the PDF file"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="get_pdf_metadata",
                    description="Extract metadata from a PDF file (title, page count, etc.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Absolute path to the PDF file"
                            }
                        },
                        "required": ["path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
            if name == "read_pdf_structure":
                path = arguments.get("path")
                if not path:
                    raise ValueError("Missing 'path' argument")
                
                try:
                    markdown = self.processor.process_pdf(path)
                    return [TextContent(type="text", text=markdown)]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error processing PDF: {str(e)}")]

            elif name == "get_pdf_metadata":
                path = arguments.get("path")
                if not path:
                    raise ValueError("Missing 'path' argument")
                
                try:
                    metadata = self.processor.get_metadata(path)
                    return [TextContent(type="text", text=json.dumps(metadata, ensure_ascii=False, indent=2))]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting metadata: {str(e)}")]

            else:
                raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        # Create custom streams with newline='' to avoid \r\n on Windows
        # This is necessary because mcp.server.stdio.stdio_server uses default TextIOWrapper which adds \r on Windows
        stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', newline='')
        stdout_wrapper = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
        
        stdin = anyio.wrap_file(stdin_wrapper)
        stdout = anyio.wrap_file(stdout_wrapper)

        async with stdio_server(stdin=stdin, stdout=stdout) as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

def main():
    # Write to stderr so it doesn't interfere with stdout JSON-RPC
    print("Starting Semantic PDF Reader MCP Server...", file=sys.stderr)
    server = SemanticPdfReaderServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
