"""
PDF merging functionality with layout preservation.
"""

import logging
from pathlib import Path
from typing import List

import PyPDF2


class PDFMerger:
    """Handles merging of PDF files while preserving layout, fonts, and images."""

    def __init__(self):
        """Initialize the PDF merger."""
        self.logger = logging.getLogger(__name__)

    def merge_pdfs(self, input_files: List[str], output_file: str) -> bool:
        """
        Merge multiple PDF files into a single PDF.

        Args:
            input_files: List of input PDF file paths
            output_file: Output PDF file path

        Returns:
            True if successful, False otherwise
        """
        try:
            merger = PyPDF2.PdfMerger()

            # Add each PDF to the merger
            for pdf_file in input_files:
                try:
                    self.logger.info(f"Adding PDF: {pdf_file}")
                    merger.append(pdf_file)
                except Exception as e:
                    self.logger.error(f"Error adding PDF {pdf_file}: {str(e)}")
                    raise Exception(f"Failed to process {pdf_file}: {str(e)}")

            # Write the merged PDF
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "wb") as output:
                merger.write(output)

            merger.close()
            self.logger.info(
                f"Successfully merged {len(input_files)} PDFs into {output_file}"
            )
            return True

        except Exception as e:
            self.logger.error(f"PDF merge failed: {str(e)}")
            return False

    def validate_pdf(self, file_path: str) -> bool:
        """
        Validate if a PDF file is readable and not corrupted.

        Args:
            file_path: Path to the PDF file

        Returns:
            True if valid, False otherwise
        """
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                # Try to read the first page to check if PDF is valid
                if len(reader.pages) > 0:
                    _ = reader.pages[0]
                return True
        except Exception as e:
            self.logger.error(f"PDF validation failed for {file_path}: {str(e)}")
            return False

    def get_pdf_info(self, file_path: str) -> dict:
        """
        Get information about a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary with PDF information
        """
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                info = {
                    "pages": len(reader.pages),
                    "title": reader.metadata.title if reader.metadata else None,
                    "author": reader.metadata.author if reader.metadata else None,
                    "subject": reader.metadata.subject if reader.metadata else None,
                    "creator": reader.metadata.creator if reader.metadata else None,
                    "encrypted": reader.is_encrypted,
                }

                return info
        except Exception as e:
            self.logger.error(f"Failed to get PDF info for {file_path}: {str(e)}")
            return {"pages": 0, "error": str(e)}

    def merge_with_bookmarks(self, input_files: List[str], output_file: str) -> bool:
        """
        Merge PDFs while preserving bookmarks and adding file-based bookmarks.

        Args:
            input_files: List of input PDF file paths
            output_file: Output PDF file path

        Returns:
            True if successful, False otherwise
        """
        try:
            merger = PyPDF2.PdfMerger()

            for i, pdf_file in enumerate(input_files):
                try:
                    file_name = Path(pdf_file).stem
                    merger.append(pdf_file, outline_item=f"File {i+1}: {file_name}")
                    self.logger.info(f"Added PDF with bookmark: {file_name}")
                except Exception as e:
                    self.logger.error(f"Error adding PDF {pdf_file}: {str(e)}")
                    raise Exception(f"Failed to process {pdf_file}: {str(e)}")

            # Write the merged PDF
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "wb") as output:
                merger.write(output)

            merger.close()
            self.logger.info(
                f"Successfully merged {len(input_files)} PDFs with bookmarks"
            )
            return True

        except Exception as e:
            self.logger.error(f"PDF merge with bookmarks failed: {str(e)}")
            return False
