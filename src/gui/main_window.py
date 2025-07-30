"""
Graphical User Interface for the file merger application.
"""

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from ..core.file_detector import FileTypeDetector
from ..core.file_merger import FileMerger


class FileManagerGUI:
    """Main GUI application for file merging."""

    def __init__(self):
        """Initialize the GUI application."""
        self.merger = FileMerger()
        self.detector = FileTypeDetector()
        self.selected_files = []

        # Create main window
        self.root = tk.Tk()
        self.root.title("File Merger - PDF & Excel")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="File Merger", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # File selection frame
        file_frame = ttk.LabelFrame(
            main_frame, text="Select Files to Merge", padding="10"
        )
        file_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        file_frame.columnconfigure(1, weight=1)

        # File selection buttons
        ttk.Button(file_frame, text="Add Files", command=self._add_files).grid(
            row=0, column=0, padx=(0, 10)
        )
        ttk.Button(
            file_frame, text="Remove Selected", command=self._remove_selected
        ).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Clear All", command=self._clear_files).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(file_frame, text="Move Up", command=self._move_up).grid(
            row=0, column=3, padx=5
        )
        ttk.Button(file_frame, text="Move Down", command=self._move_down).grid(
            row=0, column=4, padx=(5, 0)
        )

        # File list
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # File listbox with scrollbar
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview
        )
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # File info frame
        info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10")
        info_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        info_frame.columnconfigure(0, weight=1)

        self.info_text = scrolledtext.ScrolledText(
            info_frame, height=6, state=tk.DISABLED
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Merge Options", padding="10")
        options_frame.grid(
            row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # PDF options
        self.add_bookmarks_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Add bookmarks to PDF (recommended)",
            variable=self.add_bookmarks_var,
        ).grid(row=0, column=0, sticky=tk.W)

        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="Output file:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.output_entry = ttk.Entry(output_frame)
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(output_frame, text="Browse", command=self._browse_output).grid(
            row=0, column=2
        )

        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        ttk.Button(action_frame, text="Preview", command=self._preview_merge).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(
            action_frame,
            text="Merge Files",
            command=self._merge_files,
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Exit", command=self.root.quit).pack(
            side=tk.RIGHT
        )

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.grid(
            row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0)
        )

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

        # Bind events
        self.file_listbox.bind("<<ListboxSelect>>", self._on_file_select)
        self.file_listbox.bind("<Double-Button-1>", self._on_file_double_click)

    def _create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Add Files...", command=self._add_files, accelerator="Ctrl+O"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Clear All", command=self._clear_files)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=self.root.quit, accelerator="Ctrl+Q"
        )

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Preview Merge", command=self._preview_merge)
        tools_menu.add_command(label="Validate Files", command=self._validate_files)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Help", command=self._show_help)

        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self._add_files())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Delete>", lambda e: self._remove_selected())

    def _add_files(self):
        """Add files to the merge list."""
        file_types = [
            ("All supported", "*.pdf *.xlsx *.xls *.xlsm"),
            ("PDF files", "*.pdf"),
            ("Excel files", "*.xlsx *.xls *.xlsm"),
            ("All files", "*.*"),
        ]

        files = filedialog.askopenfilenames(
            title="Select files to merge", filetypes=file_types
        )

        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
                    self.file_listbox.insert(tk.END, Path(file_path).name)

            self._update_status(f"Added {len(files)} file(s)")
            self._update_file_info()

    def _remove_selected(self):
        """Remove selected files from the list."""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return

        # Remove in reverse order to maintain indices
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.selected_files[index]

        self._update_status(f"Removed {len(selected_indices)} file(s)")
        self._update_file_info()

    def _clear_files(self):
        """Clear all files from the list."""
        if self.selected_files and messagebox.askyesno("Confirm", "Clear all files?"):
            self.file_listbox.delete(0, tk.END)
            self.selected_files.clear()
            self._update_status("Cleared all files")
            self._update_file_info()

    def _move_up(self):
        """Move selected file up in the list."""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == 0:
            return

        index = selected[0]
        # Swap in listbox
        item = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index - 1, item)
        self.file_listbox.selection_set(index - 1)

        # Swap in file list
        self.selected_files[index], self.selected_files[index - 1] = (
            self.selected_files[index - 1],
            self.selected_files[index],
        )

    def _move_down(self):
        """Move selected file down in the list."""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == self.file_listbox.size() - 1:
            return

        index = selected[0]
        # Swap in listbox
        item = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index + 1, item)
        self.file_listbox.selection_set(index + 1)

        # Swap in file list
        self.selected_files[index], self.selected_files[index + 1] = (
            self.selected_files[index + 1],
            self.selected_files[index],
        )

    def _browse_output(self):
        """Browse for output file location."""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select input files first")
            return

        # Detect file type to set appropriate extension
        file_type = self.detector.detect_file_type(self.selected_files[0])
        if file_type == "pdf":
            default_ext = ".pdf"
            file_types = [("PDF files", "*.pdf"), ("All files", "*.*")]
        else:
            default_ext = ".xlsx"
            file_types = [("Excel files", "*.xlsx"), ("All files", "*.*")]

        filename = filedialog.asksaveasfilename(
            title="Save merged file as",
            defaultextension=default_ext,
            filetypes=file_types,
        )

        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def _on_file_select(self, event):
        """Handle file selection in listbox."""
        self._update_file_info()

    def _on_file_double_click(self, event):
        """Handle double-click on file in listbox."""
        selected = self.file_listbox.curselection()
        if selected:
            file_path = self.selected_files[selected[0]]
            if messagebox.askyesno("Open File", f"Open {Path(file_path).name}?"):
                try:
                    # Try to open with default application
                    import os

                    os.startfile(file_path)  # Windows
                except Exception:
                    try:
                        import subprocess

                        subprocess.run(["open", file_path])  # macOS
                    except Exception:
                        try:
                            subprocess.run(["xdg-open", file_path])  # Linux
                        except Exception:
                            messagebox.showerror("Error", "Could not open file")

    def _update_file_info(self):
        """Update the file information display."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        if not self.selected_files:
            self.info_text.insert(tk.END, "No files selected")
        else:
            # Show overall information
            file_type, valid_files, errors = self.detector.validate_files(
                self.selected_files
            )

            info = f"Total files: {len(self.selected_files)}\n"

            if errors:
                info += f"Errors: {len(errors)}\n"
                for error in errors:
                    info += f"  • {error}\n"
            elif file_type:
                info += f"File type: {file_type.upper()}\n"
                info += f"Valid files: {len(valid_files)}\n"

                # Calculate total size
                total_size = sum(self.detector.get_file_size(f) for f in valid_files)
                info += f"Total size: {self.detector.format_file_size(total_size)}\n"

            info += "\nFiles:\n"

            # Show individual file information
            selected_indices = self.file_listbox.curselection()
            if selected_indices:
                for index in selected_indices:
                    if index < len(self.selected_files):
                        file_info = self.merger.get_file_info(
                            self.selected_files[index]
                        )
                        info += f"\n{index + 1}. {file_info['name']}\n"
                        info += (
                            f"   Size: {file_info.get('size_formatted', 'Unknown')}\n"
                        )
                        info += f"   Type: {file_info.get('type', 'Unknown')}\n"

                        if file_info.get("type") == "pdf" and "pages" in file_info:
                            info += f"   Pages: {file_info['pages']}\n"
                        elif file_info.get("type") == "excel" and "sheets" in file_info:
                            info += f"   Sheets: {file_info['sheets']}\n"
                            if "sheet_names" in file_info:
                                sheet_names = file_info["sheet_names"][:3]
                                if len(file_info["sheet_names"]) > 3:
                                    sheet_names.append("...")
                                info += f"   Sheet names: {', '.join(sheet_names)}\n"
            else:
                for i, file_path in enumerate(self.selected_files, 1):
                    info += f"  {i}. {Path(file_path).name}\n"

        self.info_text.insert(tk.END, info)
        self.info_text.configure(state=tk.DISABLED)

    def _preview_merge(self):
        """Preview the merge operation."""
        if len(self.selected_files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 files to merge")
            return

        preview = self.merger.preview_merge(self.selected_files)

        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Merge Preview")
        preview_window.geometry("600x500")
        preview_window.transient(self.root)
        preview_window.grab_set()

        # Preview content
        preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if preview["errors"]:
            content = "ERRORS FOUND:\n\n"
            for error in preview["errors"]:
                content += f"• {error}\n"
        else:
            content = "MERGE PREVIEW\n\n"
            content += f"File type: {preview['file_type'].upper()}\n"
            content += f"Files to merge: {preview['file_count']}\n"
            content += f"Total size: {preview['total_size_formatted']}\n"
            estimated_size = preview["estimated_output_size_formatted"]
            content += f"Estimated output size: {estimated_size}\n\n"

            content += "FILES:\n"
            for i, file_info in enumerate(preview["files_info"], 1):
                status = "✓" if file_info["accessible"] else "✗"
                content += f"\n{i}. {status} {file_info['name']}\n"
                content += f"   Size: {file_info['size_formatted']}\n"

                if preview["file_type"] == "pdf" and "pages" in file_info:
                    content += f"   Pages: {file_info['pages']}\n"
                elif preview["file_type"] == "excel" and "sheets" in file_info:
                    content += f"   Sheets: {file_info['sheets']}\n"
                    if "sheet_names" in file_info:
                        content += (
                            f"   Sheet names: {', '.join(file_info['sheet_names'])}\n"
                        )

            if preview["warnings"]:
                content += "\nWARNINGS:\n"
                for warning in preview["warnings"]:
                    content += f"• {warning}\n"

        preview_text.insert(tk.END, content)
        preview_text.configure(state=tk.DISABLED)

        # Close button
        ttk.Button(preview_window, text="Close", command=preview_window.destroy).pack(
            pady=(0, 10)
        )

    def _validate_files(self):
        """Validate all selected files."""
        if not self.selected_files:
            messagebox.showinfo("Info", "No files to validate")
            return

        self._update_status("Validating files...")

        def validate():
            results = []
            for file_path in self.selected_files:
                file_type = self.detector.detect_file_type(file_path)
                if file_type:
                    valid = self.merger._validate_file_integrity(file_path, file_type)
                    results.append((Path(file_path).name, file_type, valid))
                else:
                    results.append((Path(file_path).name, "Unknown", False))

            # Show results in main thread
            self.root.after(0, lambda: self._show_validation_results(results))

        threading.Thread(target=validate, daemon=True).start()

    def _show_validation_results(self, results):
        """Show file validation results."""
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("File Validation Results")
        results_window.geometry("500x400")
        results_window.transient(self.root)
        results_window.grab_set()

        # Results content
        results_text = scrolledtext.ScrolledText(results_window, wrap=tk.WORD)
        results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        content = "FILE VALIDATION RESULTS\n\n"

        valid_count = sum(1 for _, _, valid in results if valid)
        content += f"Valid files: {valid_count}/{len(results)}\n\n"

        for filename, file_type, valid in results:
            status = "✓ VALID" if valid else "✗ INVALID"
            content += f"{status} - {filename} ({file_type})\n"

        results_text.insert(tk.END, content)
        results_text.configure(state=tk.DISABLED)

        # Close button
        ttk.Button(results_window, text="Close", command=results_window.destroy).pack(
            pady=(0, 10)
        )

        self._update_status("File validation completed")

    def _merge_files(self):
        """Perform the file merge operation."""
        if len(self.selected_files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 files to merge")
            return

        output_file = self.output_entry.get().strip()
        if not output_file:
            # Auto-generate output filename
            file_type = self.detector.detect_file_type(self.selected_files[0])
            if not file_type:
                messagebox.showerror("Error", "Cannot determine file type")
                return

            output_file = self.merger._generate_output_filename(
                self.selected_files, file_type, str(Path.home() / "Desktop")
            )
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

        # Start merge in background thread
        self._start_merge_operation(output_file)

    def _start_merge_operation(self, output_file):
        """Start the merge operation in a background thread."""
        self.progress.start(10)
        self._update_status("Merging files...")

        # Disable UI during merge
        self._set_ui_enabled(False)

        def merge_worker():
            try:
                result = self.merger.merge_files(
                    self.selected_files,
                    output_file,
                    add_bookmarks=self.add_bookmarks_var.get(),
                )

                # Update UI in main thread
                self.root.after(0, lambda: self._merge_completed(result))

            except Exception as e:
                error_result = {
                    "success": False,
                    "message": f"Unexpected error: {str(e)}",
                    "errors": [str(e)],
                }
                self.root.after(0, lambda: self._merge_completed(error_result))

        threading.Thread(target=merge_worker, daemon=True).start()

    def _merge_completed(self, result):
        """Handle merge operation completion."""
        self.progress.stop()
        self._set_ui_enabled(True)

        if result["success"]:
            self._update_status("Merge completed successfully")

            message = f"{result['message']}\n\nOutput file: {result['output_file']}"
            if messagebox.askyesno("Success", f"{message}\n\nOpen output folder?"):
                try:
                    import os

                    output_dir = str(Path(result["output_file"]).parent)
                    os.startfile(output_dir)  # Windows
                except Exception:
                    pass
        else:
            self._update_status("Merge failed")

            error_msg = result["message"]
            if result.get("errors"):
                error_msg += "\n\nErrors:\n" + "\n".join(
                    f"• {error}" for error in result["errors"]
                )

            messagebox.showerror("Merge Failed", error_msg)

    def _set_ui_enabled(self, enabled):
        """Enable or disable UI elements."""
        state = tk.NORMAL if enabled else tk.DISABLED

        # This is a simplified version - in a full implementation,
        # you would disable/enable all relevant widgets
        self.file_listbox.configure(state=state)
        self.output_entry.configure(state=state)

    def _update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        self.root.update_idletasks()

    def _show_about(self):
        """Show about dialog."""
        about_text = """File Merger v1.0

A Python application for merging PDF and Excel files.

Features:
• Merge multiple PDF files with layout preservation
• Merge Excel files into separate sheets
• Automatic file type detection
• File validation and error handling
• Both GUI and CLI interfaces

Supported formats:
• PDF (.pdf)
• Excel (.xlsx, .xls, .xlsm)

© 2024 File Merger Application"""

        messagebox.showinfo("About File Merger", about_text)

    def _show_help(self):
        """Show help information."""
        help_text = """How to use File Merger:

1. ADD FILES
   • Click "Add Files" to select files to merge
   • All files must be of the same type (PDF or Excel)
   • Minimum 2 files required

2. REORDER FILES (optional)
   • Select a file and use "Move Up"/"Move Down" buttons
   • Or drag and drop (if supported)

3. SET OPTIONS
   • For PDFs: Choose whether to add bookmarks
   • For Excel: All sheets will be merged automatically

4. CHOOSE OUTPUT
   • Enter output file path or click "Browse"
   • If left empty, filename will be auto-generated

5. MERGE
   • Click "Preview" to see merge details
   • Click "Merge Files" to start the operation

Tips:
• Use "Preview" to check for errors before merging
• Validate files if you suspect corruption
• Larger files may take longer to merge"""

        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x400")
        help_window.transient(self.root)

        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.configure(state=tk.DISABLED)

        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(
            pady=(0, 10)
        )

    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")


def main():
    """Main entry point for GUI."""
    app = FileManagerGUI()
    app.run()


if __name__ == "__main__":
    main()
