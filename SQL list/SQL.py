from injection_types import InjectionManager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import sys

console = Console()

class SQLShell:
    def __init__(self):
        self.running = True
        self.injection_manager = InjectionManager()
        self.commands = {
            'list': self.list_categories,
            'show': self.show_injections,
            'get': self.get_injection,
            'help': self.show_help,
            'exit': self.exit_shell
        }

    def list_categories(self, args=None):
        table = Table(title="Available SQL Injection Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green")
        
        for category in self.injection_manager.categories:
            count = len(self.injection_manager.categories[category])
            table.add_row(category, str(count))
        
        console.print(table)

    def show_injections(self, args):
        if not args:
            console.print("[red]Error: Category name required[/red]")
            return
        
        category = " ".join(args)
        if category in self.injection_manager.categories:
            table = Table(title=f"Injections for {category}")
            table.add_column("#", style="cyan", justify="right")
            table.add_column("Payload", style="green")
            
            for i, injection in enumerate(self.injection_manager.categories[category], 1):
                table.add_row(str(i), injection['payload'])
            
            console.print(table)
        else:
            console.print("[red]Invalid category. Use 'list' to see available categories.[/red]")

    def get_injection(self, args):
        if not args or len(args) < 2:
            console.print("[red]Error: Required format: get <category> <number> [-explain][/red]")
            return

        # Find the position of the last argument that could be a number
        number_pos = -1
        for i, arg in enumerate(args):
            if arg.isdigit():
                number_pos = i
                break
        
        if number_pos == -1:
            console.print("[red]Error: No injection number provided[/red]")
            return

        # Everything before the number is the category
        category = " ".join(args[:number_pos])
        try:
            index = int(args[number_pos])
            explain = "-explain" in args
            
            if category in self.injection_manager.categories:
                injections = self.injection_manager.categories[category]
                if 1 <= index <= len(injections):
                    injection = injections[index - 1]
                    import pyperclip
                    pyperclip.copy(injection['payload'])
                    
                    panel = Panel(
                        Text(injection['payload'], style="green"),
                        title="Copied to clipboard",
                        border_style="cyan"
                    )
                    console.print(panel)
                    
                    if explain:
                        explanation_panel = Panel(
                            Text(injection['explanation'], style="yellow"),
                            title="Explanation",
                            border_style="blue"
                        )
                        console.print(explanation_panel)
                else:
                    console.print("[red]Invalid injection number[/red]")
            else:
                console.print("[red]Invalid category[/red]")
        except ValueError:
            console.print("[red]Invalid injection number[/red]")

    def show_help(self, args=None):
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="green")
        
        help_table.add_row("list", "Show all SQL injection categories")
        help_table.add_row("show <category>", "List injections in a category")
        help_table.add_row(
            "get <category> <number> [-explain]",
            "Get specific injection and copy to clipboard\nUse -explain flag for detailed explanation"
        )
        help_table.add_row("help", "Show this help message")
        help_table.add_row("exit", "Exit the shell")
        
        console.print(help_table)

    def exit_shell(self, args=None):
        self.running = False
        console.print("[yellow]Goodbye![/yellow]")

    def run(self):
        banner = Panel(
            Text("SQL Injection Examples Shell\nType 'help' for available commands", 
                 style="cyan", justify="center"),
            border_style="blue"
        )
        console.print(banner)
        
        while self.running:
            try:
                command = console.input("[blue]sql>[/blue] ").strip().split()
                if not command:
                    continue
                
                cmd = command[0].lower()
                args = command[1:] if len(command) > 1 else None
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    console.print("[red]Unknown command. Type 'help' for available commands[/red]")
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")

def main():
    shell = SQLShell()
    shell.run()

if __name__ == "__main__":
    main()
