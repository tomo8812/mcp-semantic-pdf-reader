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

## Installation & Usage

### Option 1: Docker (Recommended)

Dockerを使用することで、複雑な依存関係を気にせずに実行できます。

```bash
# Build the image
docker build -t mcp-semantic-pdf-reader .

# Run the server (mounting the directory containing your PDFs)
# Replace /path/to/your/pdfs with the actual path to your PDF files
docker run -i --rm -v /path/to/your/pdfs:/data mcp-semantic-pdf-reader
```

Note: When using with an MCP client (like Claude Desktop), you'll need to configure it to run the docker command.

### Option 2: uv (Fast Python Package Manager)

`uv` を使用している場合、インストールせずに直接実行できます。

```bash
# Run directly from source
uv run --with . mcp-semantic-pdf-reader
```

### Option 3: pip (Local Installation)

```bash
pip install .
mcp-semantic-pdf-reader
```

### Option 4: uvx (Run from GitHub)

GitHubリポジトリから直接実行することも可能です（リポジトリが公開されている、またはアクセス可能である必要があります）。

```bash
# Replace 'your-username' with your actual GitHub username
uvx --from git+https://github.com/your-username/mcp-semantic-pdf-reader mcp-semantic-pdf-reader
```
