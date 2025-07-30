"""
Command Line Interface for the file merger application.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
import argparse

from ..core.file_merger import FileMerger
from ..core.file_detector import FileTypeDetector


class CLIInterface:
    """Command line interface for file merging operations."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.merger = FileMerger()
        self.detector = FileTypeDetector()
    
    def interactive_mode(self):
        """Run the interactive CLI mode."""
        print("\n" + "="*60)
        print("           FILE MERGER - Interactive Mode")
        print("="*60)
        
        try:
            # Get input files
            input_files = self._get_input_files()
            if not input_files:
                print("No files selected. Exiting.")
                return
            
            # Preview the merge
            self._show_preview(input_files)
            
            # Ask for confirmation
            if not self._confirm_merge():
                print("Merge cancelled.")
                return
            
            # Ask for reordering
            input_files = self._handle_reordering(input_files)
            
            # Get output file
            output_file = self._get_output_file(input_files)
            
            # Ask for additional options
            options = self._get_merge_options()
            
            # Perform the merge
            self._perform_merge(input_files, output_file, options)
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    def merge_files(self, input_files: List[str], output_file: str):
        """
        Merge files directly without interactive mode.
        
        Args:
            input_files: List of input file paths
            output_file: Output file path
        """
        try:
            print(f"\nMerging {len(input_files)} files...")
            
            # Show preview
            self._show_preview(input_files)
            
            # Perform merge
            result = self.merger.merge_files(input_files, output_file)
            
            if result['success']:
                print(f"\n✓ Success: {result['message']}")
                print(f"Output file: {result['output_file']}")
            else:
                print(f"\n✗ Failed: {result['message']}")
                if result['errors']:
                    for error in result['errors']:
                        print(f"  Error: {error}")
                        
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    def _get_input_files(self) -> List[str]:
        """Get input files from user."""
        print("\nEnter file paths to merge (minimum 2 files required):")
        print("You can:")
        print("1. Enter file paths one by one (press Enter after each path)")
        print("2. Enter multiple paths separated by semicolons")
        print("3. Type 'browse' to browse for files")
        print("4. Type 'done' when finished entering paths")
        print()
        
        files = []
        
        while True:
            try:
                user_input = input(f"File {len(files) + 1} (or 'done'): ").strip()
                
                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'browse':
                    browsed_files = self._browse_files()
                    files.extend(browsed_files)
                    print(f"Added {len(browsed_files)} files from browser")
                elif ';' in user_input:
                    # Multiple files separated by semicolons
                    paths = [p.strip().strip('"').strip("'") for p in user_input.split(';')]
                    for path in paths:
                        if path and Path(path).exists():
                            files.append(str(Path(path).resolve()))
                        elif path:
                            print(f"  Warning: File not found: {path}")
                elif user_input:
                    # Single file path
                    path = user_input.strip('"').strip("'")
                    if Path(path).exists():
                        files.append(str(Path(path).resolve()))
                    else:
                        print(f"  Warning: File not found: {path}")
                
                if files:
                    print(f"  Current files: {len(files)}")
                    
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"  Error: {str(e)}")
        
        return files
    
    def _browse_files(self) -> List[str]:
        """Browse for files using file dialog (if available)."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            file_types = [
                ("All supported", "*.pdf;*.xlsx;*.xls;*.xlsm"),
                ("PDF files", "*.pdf"),
                ("Excel files", "*.xlsx;*.xls;*.xlsm"),
                ("All files", "*.*")
            ]
            
            files = filedialog.askopenfilenames(
                title="Select files to merge",
                filetypes=file_types
            )
            
            root.destroy()
            return list(files)
            
        except ImportError:
            print("  File browser not available. Please enter paths manually.")
            return []
        except Exception as e:
            print(f"  Browser error: {str(e)}")
            return []
    
    def _show_preview(self, input_files: List[str]):
        """Show preview of the merge operation."""
        print("\n" + "-"*50)
        print("MERGE PREVIEW")
        print("-"*50)
        
        preview = self.merger.preview_merge(input_files)
        
        if preview['errors']:
            print("ERRORS:")
            for error in preview['errors']:
                print(f"  ✗ {error}")
            return
        
        print(f"File type: {preview['file_type'].upper()}")
        print(f"Files to merge: {preview['file_count']}")
        print(f"Total size: {preview['total_size_formatted']}")
        print(f"Estimated output size: {preview['estimated_output_size_formatted']}")
        
        print(f"\nFiles:")
        for i, file_info in enumerate(preview['files_info'], 1):
            status = "✓" if file_info['accessible'] else "✗"
            print(f"  {i}. {status} {file_info['name']} ({file_info['size_formatted']})")
            
            if preview['file_type'] == 'pdf' and 'pages' in file_info:
                print(f"      Pages: {file_info['pages']}")
            elif preview['file_type'] == 'excel' and 'sheets' in file_info:
                print(f"      Sheets: {file_info['sheets']} ({', '.join(file_info['sheet_names'][:3])}{'...' if len(file_info['sheet_names']) > 3 else ''})")
        
        if preview['warnings']:
            print(f"\nWARNINGS:")
            for warning in preview['warnings']:
                print(f"  ⚠ {warning}")
    
    def _confirm_merge(self) -> bool:
        """Ask user to confirm the merge."""
        while True:
            response = input("\nProceed with merge? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def _handle_reordering(self, files: List[str]) -> List[str]:
        """Handle file reordering if user wants to change order."""
        if len(files) <= 2:
            return files
        
        while True:
            response = input(f"\nReorder files? Current order is 1-{len(files)} (y/n): ").strip().lower()
            if response in ['n', 'no']:
                return files
            elif response in ['y', 'yes']:
                break
            else:
                print("Please enter 'y' or 'n'")
        
        print(f"\nCurrent order:")
        for i, file_path in enumerate(files, 1):
            print(f"  {i}. {Path(file_path).name}")
        
        print(f"\nEnter new order as space-separated numbers (1-{len(files)}):")
        print(f"Example: 3 1 2 4")
        
        while True:
            try:
                order_input = input("New order: ").strip()
                new_order = [int(x) - 1 for x in order_input.split()]
                
                if len(new_order) != len(files):
                    print(f"Error: Please provide exactly {len(files)} numbers")
                    continue
                
                if set(new_order) != set(range(len(files))):
                    print(f"Error: Please use each number from 1 to {len(files)} exactly once")
                    continue
                
                reordered_files = self.merger.reorder_files(files, new_order)
                
                print(f"\nNew order:")
                for i, file_path in enumerate(reordered_files, 1):
                    print(f"  {i}. {Path(file_path).name}")
                
                confirm = input("\nConfirm this order? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return reordered_files
                else:
                    continue
                    
            except ValueError:
                print("Error: Please enter valid numbers separated by spaces")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _get_output_file(self, input_files: List[str]) -> str:
        """Get output file path from user."""
        # Detect file type
        file_type = self.detector.detect_file_type(input_files[0])
        extension = '.pdf' if file_type == 'pdf' else '.xlsx'
        
        print(f"\nOutput file options:")
        print("1. Enter full path (with filename)")
        print("2. Enter directory path (filename will be auto-generated)")
        print("3. Press Enter for auto-generated filename in current directory")
        
        while True:
            output_path = input(f"\nOutput path: ").strip().strip('"').strip("'")
            
            if not output_path:
                # Auto-generate in current directory
                return self.merger._generate_output_filename(input_files, file_type, os.getcwd())
            
            path = Path(output_path)
            
            if path.is_dir() or not path.suffix:
                # Directory provided, auto-generate filename
                return self.merger._generate_output_filename(input_files, file_type, str(path))
            
            # Full path provided
            if not path.suffix:
                output_path += extension
            
            # Check if parent directory exists
            if not path.parent.exists():
                create_dir = input(f"Directory {path.parent} doesn't exist. Create it? (y/n): ").strip().lower()
                if create_dir in ['y', 'yes']:
                    path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    continue
            
            return str(path.resolve())
    
    def _get_merge_options(self) -> dict:
        """Get additional merge options from user."""
        options = {}
        
        # For PDFs, ask about bookmarks
        file_type = self.detector.detect_file_type(
            self.merger.preview_merge(['dummy.pdf'])['files_info'][0]['path'] if 
            hasattr(self, '_current_files') else None
        )
        
        if file_type == 'pdf':
            response = input("\nAdd bookmarks for each file? (y/n): ").strip().lower()
            options['add_bookmarks'] = response in ['y', 'yes']
        
        return options
    
    def _perform_merge(self, input_files: List[str], output_file: str, options: dict):
        """Perform the actual merge operation."""
        print(f"\n" + "="*50)
        print("STARTING MERGE")
        print("="*50)
        
        result = self.merger.merge_files(
            input_files, 
            output_file, 
            add_bookmarks=options.get('add_bookmarks', True)
        )
        
        print(f"\n" + "="*50)
        print("MERGE RESULTS")
        print("="*50)
        
        if result['success']:
            print(f"✓ SUCCESS: {result['message']}")
            print(f"Output file: {result['output_file']}")
            
            # Show output file size
            if Path(result['output_file']).exists():
                size = self.detector.get_file_size(result['output_file'])
                print(f"Output size: {self.detector.format_file_size(size)}")
        else:
            print(f"✗ FAILED: {result['message']}")
            
            if result['errors']:
                print(f"\nErrors:")
                for error in result['errors']:
                    print(f"  • {error}")
        
        if result['warnings']:
            print(f"\nWarnings:")
            for warning in result['warnings']:
                print(f"  ⚠ {warning}")


def main():
    """Main entry point for CLI."""
    cli = CLIInterface()
    
    parser = argparse.ArgumentParser(description="File Merger CLI")
    parser.add_argument('files', nargs='*', help='Input files to merge')
    parser.add_argument('-o', '--output', help='Output file path')
    
    args = parser.parse_args()
    
    if args.files and args.output:
        cli.merge_files(args.files, args.output)
    else:
        cli.interactive_mode()


if __name__ == '__main__':
    main()
