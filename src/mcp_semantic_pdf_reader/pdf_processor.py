import json
from pathlib import Path
from typing import Any, Dict, Optional

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

class PdfProcessor:
    def __init__(self):
        # Configure pipeline options if needed
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_ocr = True # Enable OCR for better results on scanned docs
        self.pipeline_options.do_table_structure = True # Enable table structure recognition
        
        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={InputFormat.PDF: self.pipeline_options}
        )

    def process_pdf(self, file_path: str) -> str:
        """
        Process a PDF file and return its content as Markdown.
        """
        try:
            result = self.converter.convert(file_path)
            # Export to markdown
            markdown_content = result.document.export_to_markdown()
            return markdown_content
        except Exception as e:
            raise RuntimeError(f"Failed to process PDF: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.
        """
        try:
            # Docling might not expose raw PDF metadata directly in the same way as PyMuPDF.
            # However, we can convert and check the document metadata if available,
            # or use a lightweight library like pypdf just for metadata if docling is too heavy for just metadata.
            # For now, let's see what docling gives us in the result.document.
            
            result = self.converter.convert(file_path)
            doc = result.document
            
            # Construct metadata dictionary
            metadata = {
                "title": doc.name or "",
                "page_count": len(doc.pages) if doc.pages else 0,
                # Docling's internal model might have more info, but let's start with basic info
                # If we need standard PDF metadata (Author, Creator, etc.), we might need to inspect 
                # the source or use another lib. 
                # Let's assume for now we return what we can get easily.
                "origin": doc.origin.filename if doc.origin else "",
            }
            return metadata
        except Exception as e:
            raise RuntimeError(f"Failed to extract metadata: {str(e)}")
