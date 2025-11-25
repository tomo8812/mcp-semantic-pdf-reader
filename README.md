# MCP Semantic PDF Reader

A Model Context Protocol (MCP) server that provides semantic PDF reading capabilities using [Docling](https://github.com/DS4SD/docling).

## Features

- **Structure Preservation**: Converts PDFs to Markdown while maintaining headers, paragraphs, lists, and tables.
- **Table Extraction**: Accurately converts PDF tables into Markdown table format.
- **Metadata Extraction**: Retrieves document metadata (title, author, etc.).
- **Token Efficient**: Optimizes output for LLM consumption.

## Tools

1. `read_pdf_structure`: Reads a PDF and returns structured Markdown.
2. `get_pdf_metadata`: Returns metadata of the PDF file.

## Installation

```bash
pip install .
```

## Usage

Run the server:

```bash
mcp-semantic-pdf-reader
```
