"""
CLI Questionnaire Module
Interactive questionnaire components for CLI
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any

console = Console()

def display_section_header(title: str, description: str):
    """Display section header with styling"""
    panel_content = f"[bold]{title}[/bold]\n\n{description}"
    console.print(Panel(panel_content, border_style="blue"))

def select_from_options(title: str, options: List[str], descriptions: Dict[str, str] = None) -> int:
    """Display options and get user selection"""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    
    for i, option in enumerate(options, 1):
        description = descriptions.get(option, "") if descriptions else ""
        if description:
            console.print(f"  {i}. {option} - {description}")
        else:
            console.print(f"  {i}. {option}")
    
    while True:
        try:
            choice = IntPrompt.ask("Select option", choices=[str(i) for i in range(1, len(options) + 1)])
            return choice - 1
        except:
            console.print("Please enter a valid option number.")

def collect_list_input(prompt: str, max_items: int = None) -> List[str]:
    """Collect multiple items from user"""
    items = []
    console.print(f"\n{prompt}")
    console.print("(Press Enter with empty input to finish)")
    
    while True:
        if max_items and len(items) >= max_items:
            break
            
        item = Prompt.ask(f"Item {len(items) + 1} (or press Enter to finish)", default="")
        if not item:
            break
        items.append(item)
    
    return items

def confirm_selection(message: str, default: bool = True) -> bool:
    """Get confirmation from user"""
    return Confirm.ask(message, default=default)

def display_progress_summary(current_section: str, total_sections: int, current_number: int):
    """Display progress through questionnaire"""
    progress_bar = "█" * current_number + "░" * (total_sections - current_number)
    console.print(f"\nProgress: [{progress_bar}] {current_number}/{total_sections} - {current_section}")

def display_input_summary_table(data: Dict[str, Any], title: str = "Summary"):
    """Display data in a formatted table"""
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in data.items():
        if isinstance(value, list):
            value_str = ", ".join(value) if value else "None"
        else:
            value_str = str(value) if value else "None"
        
        # Format key for display
        display_key = key.replace('_', ' ').title()
        table.add_row(display_key, value_str)
    
    console.print(table)

