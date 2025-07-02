#!/usr/bin/env python3
"""
Quick script to show the KaliOSINT menu without interaction
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

def show_menu():
    console = Console()
    
    # Display banner
    banner = """
    ██╗  ██╗ █████╗ ██╗     ██╗     ██████╗ ███████╗██╗███╗   ██╗████████╗
    ██║ ██╔╝██╔══██╗██║     ██║    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
    █████╔╝ ███████║██║     ██║    ██║   ██║███████╗██║██╔██╗ ██║   ██║   
    ██╔═██╗ ██╔══██║██║     ██║    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
    ██║  ██╗██║  ██║███████╗██║    ╚██████╔╝███████║██║██║ ╚████║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    
    🔍 Comprehensive Kali Linux OSINT Terminal Tool
    📊 Open Source Intelligence Gathering Made Easy
    🛡️  Professional Grade Information Reconnaissance
    """
    
    console.print(Panel(banner, title="[bold cyan]KaliOSINT v1.0[/bold cyan]", 
                       border_style="bright_blue", box=box.DOUBLE))
    
    # Create menu table
    table = Table(title="🎯 OSINT Operations Menu", box=box.ROUNDED, 
                  title_style="bold magenta")
    table.add_column("Option", style="cyan", justify="center", width=8)
    table.add_column("Category", style="green bold", width=20)
    table.add_column("Description", style="white", width=50)
    
    menu_items = [
        ("0", "🚪 Exit", "Exit the program"),
        ("1", "🌐 Domain OSINT", "Comprehensive domain reconnaissance"),
        ("2", "🖥️  IP Address OSINT", "IP address investigation and analysis"),
        ("3", "📧 Email OSINT", "Email address investigation"),
        ("4", "📱 Phone OSINT", "Phone number investigation"),
        ("5", "👤 Username OSINT", "Username search across platforms"),
        ("6", "🔍 Google Dorking", "Advanced Google search techniques"),
        ("7", "🗂️  Metadata Analysis", "File metadata extraction"),
        ("8", "🕷️  Web Crawling", "Website crawling and analysis"),
        ("9", "🔗 Social Media OSINT", "Social media investigation"),
        ("10", "🌊 Threat Intelligence", "Threat intelligence gathering"),
        ("11", "🌐 Network Scanning", "Network discovery and scanning"),
        ("12", "🔒 Crypto Investigation", "Cryptocurrency investigation"),
        ("13", "🕳️  Dark Web Monitoring", "Dark web intelligence"),
        ("14", "⚙️  Configuration", "Tool configuration and settings"),
        ("15", "📊 Generate Report", "Generate investigation report")
    ]
    
    for option, category, description in menu_items:
        table.add_row(option, category, description)
    
    console.print(table)
    
    # Show features summary
    features_panel = Panel(
        """
🎯 [bold green]Key Features:[/bold green]
• Multi-threaded scanning and reconnaissance
• API integrations (VirusTotal, Shodan, etc.)
• Automated report generation (JSON, HTML, PDF)
• Dark web and cryptocurrency investigation
• Social media intelligence gathering
• Advanced Google dorking techniques
• Metadata analysis and extraction
• Network discovery and port scanning

🔧 [bold yellow]Usage:[/bold yellow]
Simply run: [bold cyan]python kaliosint.py[/bold cyan]
Then select an option from the menu above.

📁 [bold blue]Results:[/bold blue]
All investigation results are saved in the 'osint_results' directory
with timestamped files for easy organization.
        """,
        title="[bold green]Tool Information[/bold green]",
        border_style="green"
    )
    
    console.print(features_panel)

if __name__ == "__main__":
    show_menu()
