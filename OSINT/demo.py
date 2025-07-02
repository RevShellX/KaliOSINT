#!/usr/bin/env python3
"""
KaliOSINT Demo Script
Demonstrates the main features of the OSINT tool
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import kaliosint modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    import pyfiglet
    
    console = Console()
    
    # Display banner
    def show_banner():
        banner_text = pyfiglet.figlet_format("KaliOSINT", font="slant")
        
        banner_panel = Panel(
            f"[bold cyan]{banner_text}[/bold cyan]\n"
            f"[bold white]Advanced OSINT Terminal Tool for Kali Linux[/bold white]\n"
            f"[yellow]Version 1.0 | Developed for Ethical Hacking & OSINT[/yellow]\n"
            f"[red]⚠️  Use responsibly and legally ⚠️[/red]",
            style="bright_blue",
            title="[bold red]🔍 OSINT Framework[/bold red]",
            title_align="center"
        )
        
        console.print(banner_panel)
        console.print()
    
    # Show main menu
    def show_menu():
        menu_table = Table(title="[bold cyan]Main Menu[/bold cyan]", show_header=True)
        menu_table.add_column("Option", style="cyan", width=10)
        menu_table.add_column("Description", style="white")
        menu_table.add_column("Category", style="yellow")
        
        menu_items = [
            ("1", "Domain & IP Investigation", "Network"),
            ("2", "Phone Number Analysis", "Personal"),
            ("3", "Email Investigation", "Personal"), 
            ("4", "Social Media Intelligence", "Social"),
            ("5", "Website Analysis", "Web"),
            ("6", "Search Engine Intelligence", "Search"),
            ("7", "Cryptocurrency Investigation", "Financial"),
            ("8", "Network Scanning", "Network"),
            ("9", "Metadata Analysis", "Files"),
            ("10", "Geolocation Intelligence", "Location"),
            ("11", "Dark Web Monitoring", "Deep Web"),
            ("12", "Breach Data Search", "Security"),
            ("13", "Company Intelligence", "Business"),
            ("14", "Configuration & API Keys", "Settings"),
            ("15", "Generate Report", "Output"),
            ("0", "Exit", "System")
        ]
        
        for option, desc, category in menu_items:
            color = get_category_color(category)
            menu_table.add_row(option, desc, f"[{color}]{category}[/{color}]")
        
        console.print(menu_table)
        console.print()
    
    def get_category_color(category):
        colors = {
            "Network": "blue",
            "Personal": "green",
            "Social": "magenta",
            "Web": "cyan",
            "Search": "yellow",
            "Financial": "red",
            "Files": "white",
            "Location": "bright_green",
            "Deep Web": "bright_red",
            "Security": "bright_yellow",
            "Business": "bright_blue",
            "Settings": "bright_magenta",
            "Output": "bright_cyan",
            "System": "bright_white"
        }
        return colors.get(category, "white")
    
    # Demo functionality
    def demo_whois():
        console.print("\n[bold green]Demo: WHOIS Lookup Functionality[/bold green]")
        
        demo_table = Table(title="WHOIS Information for example.com")
        demo_table.add_column("Field", style="cyan")
        demo_table.add_column("Value", style="white")
        
        demo_data = [
            ("Domain Name", "example.com"),
            ("Registrar", "IANA"),
            ("Creation Date", "1995-08-14"),
            ("Expiration Date", "2024-08-13"),
            ("Status", "Active"),
            ("Name Servers", "A.IANA-SERVERS.NET, B.IANA-SERVERS.NET"),
            ("Organization", "Internet Assigned Numbers Authority"),
            ("Country", "US")
        ]
        
        for field, value in demo_data:
            demo_table.add_row(field, value)
        
        console.print(demo_table)
    
    def demo_social_search():
        console.print("\n[bold green]Demo: Social Media Username Search[/bold green]")
        
        results_table = Table(title="Username Search Results for 'johndoe'")
        results_table.add_column("Platform", style="cyan")
        results_table.add_column("URL", style="white")
        results_table.add_column("Status", style="yellow")
        
        demo_results = [
            ("GitHub", "https://github.com/johndoe", "[green]Found[/green]"),
            ("Twitter", "https://twitter.com/johndoe", "[green]Found[/green]"),
            ("Instagram", "https://instagram.com/johndoe", "[red]Not Found[/red]"),
            ("LinkedIn", "https://linkedin.com/in/johndoe", "[green]Found[/green]"),
            ("Reddit", "https://reddit.com/user/johndoe", "[green]Found[/green]")
        ]
        
        for platform, url, status in demo_results:
            results_table.add_row(platform, url, status)
        
        console.print(results_table)
        console.print("\n[bold green]Found 4 potential matches out of 20 platforms[/bold green]")
    
    def demo_port_scan():
        console.print("\n[bold green]Demo: Network Port Scan Results[/bold green]")
        
        ports_table = Table(title="Open Ports on 192.168.1.1")
        ports_table.add_column("Port", style="cyan")
        ports_table.add_column("Protocol", style="yellow")
        ports_table.add_column("State", style="green")
        ports_table.add_column("Service", style="white")
        ports_table.add_column("Version", style="magenta")
        
        demo_ports = [
            ("22", "tcp", "open", "ssh", "OpenSSH 8.2"),
            ("80", "tcp", "open", "http", "Apache 2.4.41"),
            ("443", "tcp", "open", "https", "Apache 2.4.41"),
            ("8080", "tcp", "open", "http", "Jetty 9.4.39")
        ]
        
        for port, protocol, state, service, version in demo_ports:
            ports_table.add_row(port, protocol, state, service, version)
        
        console.print(ports_table)
    
    def show_features():
        console.print("\n[bold yellow]🚀 Key Features of KaliOSINT:[/bold yellow]")
        
        features = [
            "🌐 Comprehensive Domain & IP Investigation",
            "📱 Advanced Phone Number Analysis", 
            "📧 Email Investigation & Breach Search",
            "📱 Social Media Intelligence Across 20+ Platforms",
            "🌐 Website Technology Stack Analysis",
            "🔍 Search Engine Intelligence & Google Dorking",
            "💰 Cryptocurrency Investigation Tools",
            "🖥️  Network Scanning & Service Detection",
            "📄 Metadata Analysis for Files",
            "🌍 Geolocation Intelligence",
            "🕴️ Dark Web Monitoring Guidance",
            "🔐 Breach Data Search Integration",
            "🏢 Company Intelligence Gathering",
            "📊 Professional Report Generation"
        ]
        
        for feature in features:
            console.print(f"  {feature}")
        
        console.print(f"\n[bold cyan]📁 Results automatically saved to: ~/.kaliosint/results/[/bold cyan]")
        console.print(f"[bold cyan]⚙️  Configuration stored in: ~/.kaliosint/config.json[/bold cyan]")
    
    def show_api_info():
        console.print("\n[bold yellow]🔑 Supported API Integrations:[/bold yellow]")
        
        api_table = Table(title="API Integrations")
        api_table.add_column("Service", style="cyan")
        api_table.add_column("Purpose", style="white")
        api_table.add_column("Website", style="yellow")
        
        apis = [
            ("Shodan", "IoT Device Search", "https://shodan.io/"),
            ("Censys", "Certificate Search", "https://censys.io/"),
            ("VirusTotal", "Malware Analysis", "https://virustotal.com/"),
            ("HaveIBeenPwned", "Breach Data", "https://haveibeenpwned.com/"),
            ("Twitter API", "Social Media", "https://developer.twitter.com/")
        ]
        
        for service, purpose, website in apis:
            api_table.add_row(service, purpose, website)
        
        console.print(api_table)
        console.print("\n[bold green]Configure API keys in: Main Menu → Configuration & API Keys[/bold green]")
    
    # Main demo execution
    def main():
        console.clear()
        show_banner()
        
        console.print("[bold white]🎯 KaliOSINT is now running successfully![/bold white]")
        console.print("[yellow]This is a demonstration of the main interface and features.[/yellow]\n")
        
        show_menu()
        show_features()
        
        console.print("\n" + "="*80)
        console.print("[bold cyan]📋 Demo: Sample Investigation Results[/bold cyan]")
        console.print("="*80)
        
        demo_whois()
        demo_social_search()
        demo_port_scan()
        
        show_api_info()
        
        console.print("\n" + "="*80)
        console.print("[bold green]✅ KaliOSINT Demo Complete![/bold green]")
        console.print("="*80)
        
        console.print(f"\n[bold yellow]🚀 To start the full interactive version:[/bold yellow]")
        console.print(f"[white]   python kaliosint.py[/white]")
        
        console.print(f"\n[bold yellow]📖 For detailed usage examples:[/bold yellow]")
        console.print(f"[white]   See EXAMPLES.md and README.md[/white]")
        
        console.print(f"\n[bold red]⚠️  Remember: Use this tool responsibly and legally![/bold red]")
        console.print(f"[white]   Only test systems you own or have explicit permission to investigate.[/white]")
        
        return True
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install the required dependencies:")
    print("pip install rich pyfiglet colorama")
    
except Exception as e:
    print(f"❌ Demo error: {e}")
    print("Please check the installation and try again.")
