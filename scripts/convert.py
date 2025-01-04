# #!/usr/bin/env python3
# """
# Interactive workflow for notebook conversion with recursive directory selection
# """

# import questionary
# from pathlib import Path
# from rich.console import Console
# from rich import print as rprint
# import nbformat
# import json
# import shutil
# from typing import Optional, List

# console = Console()
# DEFAULT_NOTEBOOK_DIR = Path.home() / 'mlops' / 'notebooks'

# class NotebookWorkflow:
#     def __init__(self):
#         self.current_dir = Path.cwd()
#         self.default_output_dir = DEFAULT_NOTEBOOK_DIR

#     def get_subdirectories(self, path: Path) -> List[str]:
#         """Get list of subdirectories for a given path"""
#         try:
#             subdirs = [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith('.')]
#             return sorted(subdirs)
#         except Exception as e:
#             rprint(f"[red]Error accessing directory {path}: {str(e)}[/red]")
#             return []

#     def select_directory(self, start_path: Path = None) -> Optional[Path]:
#         """Recursively select directory"""
#         if start_path is None:
#             start_path = self.current_dir

#         while True:
#             # Show current path
#             rprint(f"\n[cyan]Current directory:[/cyan] {start_path}")

#             # Get subdirectories
#             subdirs = self.get_subdirectories(start_path)
            
#             # Create choices list
#             choices = [
#                 "Select this directory",
#                 "Use default notebooks directory",
#                 "Go up one level",
#                 *subdirs,
#                 "Cancel"
#             ]

#             choice = questionary.select(
#                 "Select directory or navigate:",
#                 choices=choices
#             ).ask()

#             if choice == "Cancel":
#                 return None
#             elif choice == "Select this directory":
#                 return start_path
#             elif choice == "Use default notebooks directory":
#                 self.default_output_dir.mkdir(parents=True, exist_ok=True)
#                 return self.default_output_dir
#             elif choice == "Go up one level":
#                 parent = start_path.parent
#                 if parent != start_path:  # Prevent going above root
#                     start_path = parent
#             else:
#                 # Navigate to selected subdirectory
#                 start_path = start_path / choice

#     def start_workflow(self):
#         """Main workflow loop"""
#         # Ensure default notebook directory exists
#         self.default_output_dir.mkdir(parents=True, exist_ok=True)
        
#         while True:
#             action = questionary.select(
#                 "What would you like to do?",
#                 choices=[
#                     "Convert a file",
#                     "Show available files",
#                     "Change working directory",
#                     "Exit"
#                 ]
#             ).ask()
            
#             if action == "Exit":
#                 break
#             elif action == "Convert a file":
#                 self.conversion_workflow()
#             elif action == "Show available files":
#                 self.show_files()
#             elif action == "Change working directory":
#                 self.change_directory()

#     def conversion_workflow(self):
#         """Handle file conversion workflow"""
#         # Select source file type
#         source_type = questionary.select(
#             "What type of file are you converting FROM?",
#             choices=[
#                 "Python script (.py)",
#                 "Notebook (.ipynb)",
#                 "JSON (.json)",
#                 "Go back"
#             ]
#         ).ask()
        
#         if source_type == "Go back":
#             return
            
#         # Find files of selected type
#         extension = {
#             "Python script (.py)": ".py",
#             "Notebook (.ipynb)": ".ipynb",
#             "JSON (.json)": ".json"
#         }[source_type]
        
#         files = list(self.current_dir.rglob(f"*{extension}"))
        
#         if not files:
#             rprint(f"[red]No {extension} files found in {self.current_dir}[/red]")
#             return
            
#         # Select specific file
#         file_choices = [str(f.relative_to(self.current_dir)) for f in files]
#         file_choices.append("Go back")
        
#         selected_file = questionary.select(
#             "Which file would you like to convert?",
#             choices=file_choices
#         ).ask()
        
#         if selected_file == "Go back":
#             return

#         # Select target format
#         valid_targets = {
#             ".py": ["Notebook (.ipynb)"],
#             ".ipynb": ["Python script (.py)", "JSON (.json)"],
#             ".json": ["Notebook (.ipynb)"]
#         }
        
#         target_type = questionary.select(
#             "Convert to what format?",
#             choices=valid_targets[extension] + ["Go back"]
#         ).ask()
        
#         if target_type == "Go back":
#             return

#         # Get output location using recursive directory selection
#         rprint("\n[yellow]Select output directory:[/yellow]")
#         output_dir = self.select_directory()
        
#         if output_dir is None:
#             rprint("[red]Conversion cancelled[/red]")
#             return

#         # Perform conversion
#         try:
#             source_path = self.current_dir / selected_file
#             target_extension = {
#                 "Python script (.py)": ".py",
#                 "Notebook (.ipynb)": ".ipynb",
#                 "JSON (.json)": ".json"
#             }[target_type]
            
#             output_dir = Path(output_dir)
#             output_dir.mkdir(parents=True, exist_ok=True)
#             output_path = output_dir / f"{source_path.stem}{target_extension}"
            
#             self.convert_file(source_path, output_path)
#             rprint(f"[green]Successfully converted to:[/green] {output_path}")
            
#             # Ask what to do next
#             next_action = questionary.select(
#                 "What would you like to do next?",
#                 choices=[
#                     "Convert another file",
#                     "Show available files",
#                     "Change directory",
#                     "Exit"
#                 ]
#             ).ask()
            
#             if next_action == "Convert another file":
#                 self.conversion_workflow()
#             elif next_action == "Show available files":
#                 self.show_files()
#             elif next_action == "Change directory":
#                 self.change_directory()
                
#         except Exception as e:
#             rprint(f"[red]Error during conversion: {str(e)}[/red]")
#             self.conversion_workflow()

#     def convert_file(self, source: Path, target: Path):
#         """Convert between file formats"""
#         if source.suffix == target.suffix:
#             shutil.copy2(source, target)
#             return
            
#         if source.suffix == '.py' and target.suffix == '.ipynb':
#             self.py_to_notebook(source, target)
#         elif source.suffix == '.ipynb' and target.suffix == '.py':
#             self.notebook_to_py(source, target)
#         elif source.suffix == '.ipynb' and target.suffix == '.json':
#             self.notebook_to_json(source, target)
#         elif source.suffix == '.json' and target.suffix == '.ipynb':
#             self.json_to_notebook(source, target)
#         else:
#             raise ValueError(f"Unsupported conversion: {source.suffix} to {target.suffix}")

#     def py_to_notebook(self, source: Path, target: Path):
#         """Convert Python script to notebook"""
#         nb = nbformat.v4.new_notebook()
#         current_cells = []
#         current_type = 'code'
        
#         with open(source) as f:
#             lines = f.readlines()
            
#         for line in lines:
#             if line.startswith('#%% md'):
#                 if current_cells:
#                     if current_type == 'code':
#                         nb.cells.append(nbformat.v4.new_code_cell(''.join(current_cells)))
#                     else:
#                         nb.cells.append(nbformat.v4.new_markdown_cell(''.join(current_cells)))
#                 current_cells = []
#                 current_type = 'markdown'
#                 continue
                
#             if current_type == 'markdown':
#                 if line.startswith('# '):
#                     line = line[2:]
#                 current_cells.append(line)
#             else:
#                 current_cells.append(line)
        
#         if current_cells:
#             if current_type == 'code':
#                 nb.cells.append(nbformat.v4.new_code_cell(''.join(current_cells)))
#             else:
#                 nb.cells.append(nbformat.v4.new_markdown_cell(''.join(current_cells)))
        
#         nbformat.write(nb, target)

#     def notebook_to_py(self, source: Path, target: Path):
#         """Convert notebook to Python script"""
#         with open(source) as f:
#             nb = nbformat.read(f, as_version=4)
            
#         with open(target, 'w') as f:
#             for cell in nb.cells:
#                 if cell.cell_type == 'markdown':
#                     f.write('#%% md\n')
#                     for line in cell.source.split('\n'):
#                         f.write(f'# {line}\n')
#                     f.write('\n')
#                 elif cell.cell_type == 'code':
#                     f.write(cell.source + '\n\n')

#     def notebook_to_json(self, source: Path, target: Path):
#         """Convert notebook to JSON"""
#         shutil.copy2(source, target)

#     def json_to_notebook(self, source: Path, target: Path):
#         """Convert JSON to notebook"""
#         shutil.copy2(source, target)

#     def show_files(self):
#         """Display available files"""
#         rprint("\n[yellow]Available files:[/yellow]")
        
#         extensions = ['.py', '.ipynb', '.json']
#         for ext in extensions:
#             files = list(self.current_dir.rglob(f"*{ext}"))
#             if files:
#                 rprint(f"\n[cyan]{ext} files:[/cyan]")
#                 for f in files:
#                     rprint(f"  {f.relative_to(self.current_dir)}")
        
#         input("\nPress Enter to continue...")

#     def change_directory(self):
#         """Change working directory"""
#         new_dir = questionary.path(
#             "Enter new working directory:",
#             only_directories=True
#         ).ask()
        
#         try:
#             new_path = Path(new_dir).resolve()
#             if new_path.exists():
#                 self.current_dir = new_path
#                 rprint(f"[green]Changed working directory to: {self.current_dir}[/green]")
#             else:
#                 rprint(f"[red]Directory does not exist: {new_dir}[/red]")
#         except Exception as e:
#             rprint(f"[red]Error changing directory: {str(e)}[/red]")

# def main():
#     rprint(f"[bold cyan]Notebook Converter Workflow[/bold cyan]")
#     rprint(f"[yellow]Default notebook directory:[/yellow] {DEFAULT_NOTEBOOK_DIR}")
#     workflow = NotebookWorkflow()
#     workflow.start_workflow()

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
Interactive workflow for notebook conversion with recursive directory selection
and JSON archiving
"""

import questionary
from pathlib import Path
from rich.console import Console
from rich import print as rprint
import nbformat
import json
import shutil
from typing import Optional, List
from datetime import datetime, timedelta

console = Console()
DEFAULT_NOTEBOOK_DIR = Path.home() / 'mlops' / 'notebooks'

class NotebookWorkflow:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.default_output_dir = DEFAULT_NOTEBOOK_DIR

    def get_subdirectories(self, path: Path) -> List[str]:
        """Get list of subdirectories for a given path"""
        try:
            subdirs = [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            return sorted(subdirs)
        except Exception as e:
            rprint(f"[red]Error accessing directory {path}: {str(e)}[/red]")
            return []

    def select_directory(self, start_path: Path = None) -> Optional[Path]:
        """Recursively select directory"""
        if start_path is None:
            start_path = self.current_dir

        while True:
            # Show current path
            rprint(f"\n[cyan]Current directory:[/cyan] {start_path}")

            # Get subdirectories
            subdirs = self.get_subdirectories(start_path)
            
            # Create choices list
            choices = [
                "Select this directory",
                "Use default notebooks directory",
                "Go up one level",
                *subdirs,
                "Cancel"
            ]

            choice = questionary.select(
                "Select directory or navigate:",
                choices=choices
            ).ask()

            if choice == "Cancel":
                return None
            elif choice == "Select this directory":
                return start_path
            elif choice == "Use default notebooks directory":
                self.default_output_dir.mkdir(parents=True, exist_ok=True)
                return self.default_output_dir
            elif choice == "Go up one level":
                parent = start_path.parent
                if parent != start_path:  # Prevent going above root
                    start_path = parent
            else:
                # Navigate to selected subdirectory
                start_path = start_path / choice

    def start_workflow(self):
        """Main workflow loop"""
        # Ensure default notebook directory exists
        self.default_output_dir.mkdir(parents=True, exist_ok=True)
        
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Convert a file",
                    "Show available files",
                    "Change working directory",
                    "Manage JSON archives",
                    "Exit"
                ]
            ).ask()
            
            if action == "Exit":
                break
            elif action == "Convert a file":
                self.conversion_workflow()
            elif action == "Show available files":
                self.show_files()
            elif action == "Change working directory":
                self.change_directory()
            elif action == "Manage JSON archives":
                self.manage_json_archives()

    def manage_json_archives(self):
        """Manage JSON archives"""
        json_dir = self.current_dir / 'notebook_jsons'
        archive_dir = json_dir / 'archive'
        
        if not json_dir.exists() or not archive_dir.exists():
            rprint("[yellow]No archives found.[/yellow]")
            return
            
        # List all archived JSONs
        archived_files = list(archive_dir.glob('*.json'))
        if not archived_files:
            rprint("[yellow]No archived JSON files found.[/yellow]")
            return
        
        # Show archive management options
        action = questionary.select(
            "Archive Management:",
            choices=[
                "List archived JSONs",
                "Restore archived JSON",
                "Delete old archives",
                "Go back"
            ]
        ).ask()
        
        if action == "List archived JSONs":
            rprint("\n[cyan]Archived JSON files:[/cyan]")
            for f in archived_files:
                rprint(f"  {f.name}")
                
        elif action == "Restore archived JSON":
            # Select file to restore
            file_choices = [f.name for f in archived_files] + ["Go back"]
            selected = questionary.select(
                "Select JSON to restore:",
                choices=file_choices
            ).ask()
            
            if selected != "Go back":
                archived_file = archive_dir / selected
                restored_path = json_dir / archived_file.name.split('_')[0] + '.json'
                try:
                    shutil.copy2(archived_file, restored_path)
                    rprint(f"[green]Restored to:[/green] {restored_path}")
                except Exception as e:
                    rprint(f"[red]Error restoring file: {str(e)}[/red]")
                    
        elif action == "Delete old archives":
            # Confirm deletion
            if questionary.confirm("Are you sure you want to delete old archives?").ask():
                cutoff_date = datetime.now() - timedelta(days=30)  # Keep last 30 days
                
                deleted = 0
                for f in archived_files:
                    try:
                        file_date = datetime.strptime(f.stem.split('_')[-2], "%Y%m%d")
                        if file_date < cutoff_date:
                            f.unlink()
                            deleted += 1
                    except Exception:
                        continue
                        
                rprint(f"[green]Deleted {deleted} old archive(s).[/green]")

    def conversion_workflow(self):
        """Handle file conversion workflow"""
        # Select source file type
        source_type = questionary.select(
            "What type of file are you converting FROM?",
            choices=[
                "Python script (.py)",
                "Notebook (.ipynb)",
                "JSON (.json)",
                "Go back"
            ]
        ).ask()
        
        if source_type == "Go back":
            return
            
        # Find files of selected type
        extension = {
            "Python script (.py)": ".py",
            "Notebook (.ipynb)": ".ipynb",
            "JSON (.json)": ".json"
        }[source_type]
        
        # Special handling for JSON files
        if extension == '.json':
            json_dir = self.current_dir / 'notebook_jsons'
            if not json_dir.exists():
                rprint(f"[red]notebook_jsons directory not found in {self.current_dir}[/red]")
                return
            files = list(json_dir.glob(f"*{extension}"))
        else:
            files = list(self.current_dir.rglob(f"*{extension}"))
        
        if not files:
            rprint(f"[red]No {extension} files found in {self.current_dir if extension != '.json' else json_dir}[/red]")
            return
            
        # Select specific file
        file_choices = [str(f.relative_to(self.current_dir)) for f in files]
        file_choices.append("Go back")
        
        selected_file = questionary.select(
            "Which file would you like to convert?",
            choices=file_choices
        ).ask()
        
        if selected_file == "Go back":
            return

        # Select target format
        valid_targets = {
            ".py": ["Notebook (.ipynb)"],
            ".ipynb": ["Python script (.py)", "JSON (.json)"],
            ".json": ["Notebook (.ipynb)"]
        }
        
        target_type = questionary.select(
            "Convert to what format?",
            choices=valid_targets[extension] + ["Go back"]
        ).ask()
        
        if target_type == "Go back":
            return

        # Get output location using recursive directory selection
        rprint("\n[yellow]Select output directory:[/yellow]")
        output_dir = self.select_directory()
        
        if output_dir is None:
            rprint("[red]Conversion cancelled[/red]")
            return

        # Perform conversion
        try:
            source_path = self.current_dir / selected_file
            target_extension = {
                "Python script (.py)": ".py",
                "Notebook (.ipynb)": ".ipynb",
                "JSON (.json)": ".json"
            }[target_type]
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{source_path.stem}{target_extension}"
            
            self.convert_file(source_path, output_path)
            rprint(f"[green]Successfully converted to:[/green] {output_path}")
            
            # Ask what to do next
            next_action = questionary.select(
                "What would you like to do next?",
                choices=[
                    "Convert another file",
                    "Show available files",
                    "Change directory",
                    "Exit"
                ]
            ).ask()
            
            if next_action == "Convert another file":
                self.conversion_workflow()
            elif next_action == "Show available files":
                self.show_files()
            elif next_action == "Change directory":
                self.change_directory()
                
        except Exception as e:
            rprint(f"[red]Error during conversion: {str(e)}[/red]")
            self.conversion_workflow()

    def convert_file(self, source: Path, target: Path):
        """Convert between file formats"""
        if source.suffix == target.suffix:
            shutil.copy2(source, target)
            return
            
        if source.suffix == '.py' and target.suffix == '.ipynb':
            self.py_to_notebook(source, target)
        elif source.suffix == '.ipynb' and target.suffix == '.py':
            self.notebook_to_py(source, target)
        elif source.suffix == '.ipynb' and target.suffix == '.json':
            self.notebook_to_json(source, target)
        elif source.suffix == '.json' and target.suffix == '.ipynb':
            self.json_to_notebook(source, target)
        else:
            raise ValueError(f"Unsupported conversion: {source.suffix} to {target.suffix}")

    def py_to_notebook(self, source: Path, target: Path):
        """Convert Python script to notebook"""
        nb = nbformat.v4.new_notebook()
        current_cells = []
        current_type = 'code'
        
        with open(source) as f:
            lines = f.readlines()
            
        for line in lines:
            if line.startswith('#%% md'):
                if current_cells:
                    if current_type == 'code':
                        nb.cells.append(nbformat.v4.new_code_cell(''.join(current_cells)))
                    else:
                        nb.cells.append(nbformat.v4.new_markdown_cell(''.join(current_cells)))
                current_cells = []
                current_type = 'markdown'
                continue
                
            if current_type == 'markdown':
                if line.startswith('# '):
                    line = line[2:]
                current_cells.append(line)
            else:
                current_cells.append(line)
        
        if current_cells:
            if current_type == 'code':
                nb.cells.append(nbformat.v4.new_code_cell(''.join(current_cells)))
            else:
                nb.cells.append(nbformat.v4.new_markdown_cell(''.join(current_cells)))
        
        nbformat.write(nb, target)

    def notebook_to_py(self, source: Path, target: Path):
        """Convert notebook to Python script"""
        with open(source) as f:
            nb = nbformat.read(f, as_version=4)
            
        with open(target, 'w') as f:
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    f.write('#%% md\n')
                    for line in cell.source.split('\n'):
                        f.write(f'# {line}\n')
                    f.write('\n')
                elif cell.cell_type == 'code':
                    f.write(cell.source + '\n\n')

    def notebook_to_json(self, source: Path, target: Path):
        """Convert notebook to JSON"""
        shutil.copy2(source, target)

    def json_to_notebook(self, source: Path, target: Path):
        """Convert JSON to notebook and archive the JSON"""
        try:
            # First, make the conversion
            shutil.copy2(source, target)
            
            # Create archive directory if it doesn't exist
            archive_dir = source.parent / 'archive'
            archive_dir.mkdir(exist_ok=True)
            
            # Generate archived file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_dir / f"{source.stem}_{timestamp}.json"
            
            # Move JSON to archive
            shutil.move(str(source), str(archive_path))
            rprint(f"[yellow]Archived JSON to:[/yellow] {archive_path}")
            
        except Exception as e:
            rprint(f"[red]Warning: Could not archive JSON: {str(e)}[/red]")

    def show_files(self):
        """Display available files"""
        rprint("\n[yellow]Available files:[/yellow]")
        
        extensions = ['.py', '.ipynb', '.json']
        for ext in extensions:
            files = list(self.current_dir.rglob(f"*{ext}"))
            if files:
                rprint(f"\n[cyan]{ext} files:[/cyan]")
                for f in files:
                    rprint(f"  {f.relative_to(self.current_dir)}")
        
        input("\nPress Enter to continue...")

    def change_directory(self):
        """Change working directory"""
        new_dir = questionary.path(
            "Enter new working directory:",
            only_directories=True
        ).ask()
        
        try:
            new_path = Path(new_dir).resolve()
            if new_path.exists():
                self.current_dir = new_path
                rprint(f"[green]Changed working directory to: {self.current_dir}[/green]")
            else:
                rprint(f"[red]Directory does not exist: {new_dir}[/red]")
        except Exception as e:
            rprint(f"[red]Error changing directory: {str(e)}[/red]")

def main():
    rprint(f"[bold cyan]Notebook Converter Workflow[/bold cyan]")
    rprint(f"[yellow]Default notebook directory:[/yellow] {DEFAULT_NOTEBOOK_DIR}")
    workflow = NotebookWorkflow()
    workflow.start_workflow()

if __name__ == "__main__":
    main()