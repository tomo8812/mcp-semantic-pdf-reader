import json
from pathlib import Path
from typing import Any, Dict, Optional

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

class PdfProcessor:
    def __init__(self):
        # Configure pipeline options
        self.pipeline_options = PdfPipelineOptions()
        
        # Optimize for performance:
        # 1. Disable OCR by default (heavy resource usage). Enable only if needed.
        self.pipeline_options.do_ocr = False 
        
        # 2. Enable table structure recognition (useful but less heavy than OCR)
        self.pipeline_options.do_table_structure = True
        
        # 3. Limit resource usage via AcceleratorOptions
        self.pipeline_options.accelerator_options = AcceleratorOptions(
            num_threads=4, # Limit threads to avoid hogging CPU
            device=AcceleratorDevice.AUTO
        )
        
        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=self.pipeline_options)
            }
        )

    def process_pdf(self, file_path: str, ocr: bool = False, page_range: str = None) -> str:
        """
        Process a PDF file and return its content as Markdown.
        
        Args:
            file_path: Absolute path to the PDF file
            ocr: Whether to enable OCR (slower but better for scanned docs)
            page_range: Optional page range (e.g. "1-5", "1,3,5"). 1-based indexing.
        """
        import pypdf
        import tempfile
        import os

        try:
            target_path = file_path
            temp_pdf = None

            # Handle page range if specified
            if page_range:
                try:
                    reader = pypdf.PdfReader(file_path)
                    writer = pypdf.PdfWriter()
                    
                    # Parse page range (simple implementation: "1-5" or "1,3,5")
                    pages_to_keep = set()
                    parts = page_range.split(',')
                    for part in parts:
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            pages_to_keep.update(range(start, end + 1))
                        else:
                            pages_to_keep.add(int(part))
                    
                    # Add selected pages (convert 1-based to 0-based)
                    for p in sorted(pages_to_keep):
                        if 1 <= p <= len(reader.pages):
                            writer.add_page(reader.pages[p-1])
                    
                    # Save to temp file
                    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
                    os.close(fd)
                    writer.write(temp_path)
                    target_path = temp_path
                    temp_pdf = temp_path
                except Exception as e:
                    raise ValueError(f"Invalid page range or failed to split PDF: {str(e)}")

            if ocr:
                # Create a temporary converter with OCR enabled
                ocr_options = PdfPipelineOptions()
                ocr_options.do_ocr = True
                ocr_options.do_table_structure = True
                ocr_options.accelerator_options = self.pipeline_options.accelerator_options
                
                converter = DocumentConverter(
                    allowed_formats=[InputFormat.PDF],
                    format_options={
                        InputFormat.PDF: PdfFormatOption(pipeline_options=ocr_options)
                    }
                )
                result = converter.convert(target_path)
            else:
                # Use the default optimized converter
                result = self.converter.convert(target_path)
                
            # Export to markdown
            markdown_content = result.document.export_to_markdown()
            
            # Cleanup temp file
            if temp_pdf and os.path.exists(temp_pdf):
                os.remove(temp_pdf)
                
            return markdown_content
        except Exception as e:
            if temp_pdf and os.path.exists(temp_pdf):
                os.remove(temp_pdf)
            raise RuntimeError(f"Failed to process PDF: {str(e)}")

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file using pypdf for speed.
        """
        import pypdf
        try:
            reader = pypdf.PdfReader(file_path)
            info = reader.metadata
            
            metadata = {
                "title": info.title if info and info.title else "",
                "author": info.author if info and info.author else "",
                "page_count": len(reader.pages),
                "is_encrypted": reader.is_encrypted
            }
            return metadata
        except Exception as e:
            raise RuntimeError(f"Failed to extract metadata: {str(e)}")
