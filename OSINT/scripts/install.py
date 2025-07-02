#!/usr/bin/env python3
"""
KaliOSINT Installation Script
Automated setup for KaliOSINT OSINT Framework
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def banner():
    """Display installation banner"""
    banner_text = """
 ██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██║ ██╔╝██╔══██╗██║     ██║██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 █████╔╝ ███████║██║     ██║██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██╔═██╗ ██╔══██║██║     ██║██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ██║  ██╗██║  ██║███████╗██║╚██████╔╝███████║██║██║ ╚████║   ██║   
 ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    """
    
    panel = Panel(
        f"[bold cyan]{banner_text}[/bold cyan]\n"
        f"[bold white]Advanced OSINT Terminal Tool[/bold white]\n"
        f"[yellow]Installation Script v1.0[/yellow]\n"
        f"[red]🔧 Setting up your OSINT environment...[/red]",
        style="bright_blue",
        title="[bold red]🔍 KaliOSINT Installer[/bold red]",
        title_align="center"
    )
    
    console.print(panel)
    console.print()

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        console.print("[red]❌ Error: Python 3.8 or higher is required[/red]")
        console.print(f"[yellow]Current version: {version.major}.{version.minor}.{version.micro}[/yellow]")
        return False
    
    console.print(f"[green]✅ Python {version.major}.{version.minor}.{version.micro} detected[/green]")
    return True

def check_os():
    """Check operating system compatibility"""
    os_name = platform.system()
    console.print(f"[cyan]🖥️  Operating System: {os_name}[/cyan]")
    
    if os_name == "Linux":
        try:
            with open("/etc/os-release") as f:
                content = f.read()
                if "kali" in content.lower():
                    console.print("[green]✅ Kali Linux detected - Optimal environment[/green]")
                else:
                    console.print("[yellow]⚠️  Non-Kali Linux detected - Should work fine[/yellow]")
        except:
            console.print("[yellow]⚠️  Linux distribution unknown[/yellow]")
    elif os_name == "Windows":
        console.print("[yellow]⚠️  Windows detected - Some features may be limited[/yellow]")
    elif os_name == "Darwin":
        console.print("[yellow]⚠️  macOS detected - Some features may be limited[/yellow]")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    console.print("\n[bold cyan]📦 Installing Python dependencies...[/bold cyan]")
    
    try:
        # Read requirements file
        requirements_file = Path(__file__).parent.parent / "requirements.txt"
        
        if not requirements_file.exists():
            console.print("[red]❌ requirements.txt not found[/red]")
            return False
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Installing packages...", total=None)
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print("[green]✅ All dependencies installed successfully[/green]")
                return True
            else:
                console.print(f"[red]❌ Error installing dependencies: {result.stderr}[/red]")
                return False
                
    except Exception as e:
        console.print(f"[red]❌ Error during installation: {e}[/red]")
        return False

def setup_directories():
    """Create necessary directories"""
    console.print("\n[bold cyan]📁 Setting up directories...[/bold cyan]")
    
    home_dir = Path.home()
    kaliosint_dir = home_dir / ".kaliosint"
    
    directories = [
        kaliosint_dir,
        kaliosint_dir / "results",
        kaliosint_dir / "config",
        kaliosint_dir / "logs",
        kaliosint_dir / "cache"
    ]
    
    for directory in directories:
        try:
            directory.mkdir(exist_ok=True)
            console.print(f"[green]✅ Created: {directory}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error creating {directory}: {e}[/red]")
            return False
    
    return True

def setup_config():
    """Setup configuration files"""
    console.print("\n[bold cyan]⚙️  Setting up configuration...[/bold cyan]")
    
    try:
        # Copy default config
        project_root = Path(__file__).parent.parent
        config_source = project_root / "config" / "default_config.json"
        
        home_dir = Path.home()
        config_dest = home_dir / ".kaliosint" / "config" / "config.json"
        
        if config_source.exists():
            config_dest.parent.mkdir(exist_ok=True)
            
            if not config_dest.exists():
                with open(config_source) as f:
                    config_data = json.load(f)
                
                with open(config_dest, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                console.print(f"[green]✅ Configuration file created: {config_dest}[/green]")
            else:
                console.print(f"[yellow]⚠️  Configuration already exists: {config_dest}[/yellow]")
        
        # Setup API keys template
        api_template = project_root / "config" / "api_keys.json.template"
        api_dest = home_dir / ".kaliosint" / "config" / "api_keys.json"
        
        if api_template.exists() and not api_dest.exists():
            with open(api_template) as f:
                api_data = json.load(f)
            
            with open(api_dest, 'w') as f:
                json.dump(api_data, f, indent=2)
            
            console.print(f"[green]✅ API keys template created: {api_dest}[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error setting up configuration: {e}[/red]")
        return False

def create_launcher():
    """Create launcher script"""
    console.print("\n[bold cyan]🚀 Creating launcher script...[/bold cyan]")
    
    try:
        project_root = Path(__file__).parent.parent
        launcher_content = f"""#!/bin/bash
# KaliOSINT Launcher Script
cd "{project_root}"
python main.py "$@"
"""
        
        launcher_path = project_root / "kaliosint"
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(launcher_path, 0o755)
        
        console.print(f"[green]✅ Launcher created: {launcher_path}[/green]")
        console.print("[cyan]You can now run: ./kaliosint[/cyan]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error creating launcher: {e}[/red]")
        return False

def final_setup():
    """Final setup tasks"""
    console.print("\n[bold cyan]🎯 Final setup...[/bold cyan]")
    
    console.print("\n[bold green]🎉 Installation completed successfully![/bold green]")
    console.print("\n[bold yellow]Next steps:[/bold yellow]")
    console.print("1. Configure your API keys in ~/.kaliosint/config/api_keys.json")
    console.print("2. Run: python main.py (or ./kaliosint)")
    console.print("3. Start your OSINT investigations!")
    
    console.print("\n[bold cyan]📚 Documentation:[/bold cyan]")
    console.print("• README.md - General information")
    console.print("• docs/ - Detailed documentation")
    console.print("• config/ - Configuration examples")
    
    console.print("\n[bold red]⚠️  Remember:[/bold red]")
    console.print("• Use this tool responsibly and legally")
    console.print("• Only investigate targets you own or have permission to test")
    console.print("• Follow your local laws and regulations")

def main():
    """Main installation function"""
    banner()
    
    console.print("[bold yellow]🔍 KaliOSINT Installation Wizard[/bold yellow]")
    console.print("This script will install KaliOSINT and its dependencies.\n")
    
    if not Confirm.ask("Do you want to continue with the installation?"):
        console.print("[yellow]Installation cancelled by user[/yellow]")
        return
    
    # Pre-installation checks
    console.print("\n[bold cyan]🔍 Pre-installation checks...[/bold cyan]")
    
    if not check_python_version():
        return
    
    if not check_os():
        return
    
    # Installation steps
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Setting up directories", setup_directories),
        ("Configuring application", setup_config),
        ("Creating launcher", create_launcher),
    ]
    
    for step_name, step_func in steps:
        console.print(f"\n[bold cyan]📋 {step_name}...[/bold cyan]")
        if not step_func():
            console.print(f"[red]❌ Failed at: {step_name}[/red]")
            return
    
    final_setup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Installation interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
