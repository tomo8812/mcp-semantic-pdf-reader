import asyncio
import json
import sys
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import StdioServerTransport
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
        transport = StdioServerTransport()
        await self.server.run(transport.read_messages(), transport.write_message)

def main():
    server = SemanticPdfReaderServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
