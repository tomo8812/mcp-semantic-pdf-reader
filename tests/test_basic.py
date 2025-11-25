import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from mcp_semantic_pdf_reader.pdf_processor import PdfProcessor
    print("Successfully imported PdfProcessor")
except ImportError as e:
    print(f"Failed to import PdfProcessor: {e}")
    sys.exit(1)

def test_instantiation():
    try:
        processor = PdfProcessor()
        print("Successfully instantiated PdfProcessor")
    except Exception as e:
        print(f"Failed to instantiate PdfProcessor: {e}")
        # It might fail if dependencies are not fully installed yet or models need downloading
        # Docling often downloads models on first run.

if __name__ == "__main__":
    test_instantiation()
