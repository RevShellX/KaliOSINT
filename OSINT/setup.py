#!/usr/bin/env python3
"""
KaliOSINT Installation and Setup Script
Automatically installs dependencies and sets up the OSINT environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print installation banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    KaliOSINT Setup Script                    ║
║              Advanced OSINT Terminal Tool                    ║
║                                                             ║
║  This script will install all required dependencies        ║
║  and set up your OSINT environment                         ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")

def check_os():
    """Check operating system"""
    os_name = platform.system()
    print(f"🖥️  Operating System: {os_name}")
    
    if os_name == "Linux":
        # Check if it's Kali Linux
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read()
                if 'kali' in content.lower():
                    print("✅ Kali Linux detected - optimal environment!")
                else:
                    print("⚠️  Not Kali Linux - some tools may need manual installation")
        except:
            print("⚠️  Could not detect Linux distribution")
    elif os_name == "Windows":
        print("⚠️  Windows detected - some features may be limited")
    elif os_name == "Darwin":
        print("⚠️  macOS detected - some tools may need manual installation")

def install_python_packages():
    """Install required Python packages"""
    print("\n📦 Installing Python packages...")
    
    packages = [
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "click>=8.1.0",
        "python-whois>=0.8.0",
        "dnspython>=2.3.0",
        "shodan>=1.28.0",
        "phonenumbers>=8.13.0",
        "python-nmap>=0.7.1",
        "feedparser>=6.0.10",
        "pyfiglet>=0.8.0",
        "termcolor>=2.3.0",
        "tabulate>=0.9.0",
        "validators>=0.22.0",
        "ipwhois>=1.2.0",
        "matplotlib>=3.7.0",
        "networkx>=3.1",
        "plotly>=5.17.0"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package.split('>=')[0]}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package.split('>=')[0]} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package.split('>=')[0]}")

def install_system_tools():
    """Install system tools (Linux/Kali specific)"""
    print("\n🔧 Checking system tools...")
    
    if platform.system() == "Linux":
        tools = {
            "nmap": "Network scanning tool",
            "whois": "Domain lookup tool", 
            "dig": "DNS lookup tool",
            "curl": "HTTP client",
            "wget": "File downloader",
            "tor": "Tor anonymity network",
            "proxychains": "Proxy chains tool"
        }
        
        for tool, description in tools.items():
            try:
                result = subprocess.run(["which", tool], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {tool} is installed ({description})")
                else:
                    print(f"⚠️  {tool} not found - install with: apt install {tool}")
            except:
                print(f"❌ Could not check {tool}")

def create_config_structure():
    """Create configuration directory structure"""
    print("\n📁 Creating configuration structure...")
    
    config_dir = Path.home() / ".kaliosint"
    results_dir = config_dir / "results"
    logs_dir = config_dir / "logs"
    
    try:
        config_dir.mkdir(exist_ok=True)
        results_dir.mkdir(exist_ok=True)
        logs_dir.mkdir(exist_ok=True)
        
        print(f"✅ Configuration directory: {config_dir}")
        print(f"✅ Results directory: {results_dir}")
        print(f"✅ Logs directory: {logs_dir}")
        
        # Create default config file
        config_file = config_dir / "config.json"
        if not config_file.exists():
            default_config = {
                "version": "1.0",
                "created": "auto-generated",
                "shodan_api": "",
                "censys_api_id": "",
                "censys_api_secret": "",
                "virustotal_api": "",
                "hibp_api": "",
                "twitter_bearer": ""
            }
            
            import json
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"✅ Default configuration created: {config_file}")
        
    except Exception as e:
        print(f"❌ Error creating directories: {e}")

def setup_aliases():
    """Set up shell aliases for easy access"""
    print("\n🔗 Setting up aliases...")
    
    script_dir = Path(__file__).parent.absolute()
    kaliosint_script = script_dir / "kaliosint.py"
    
    if kaliosint_script.exists():
        print(f"📍 KaliOSINT script location: {kaliosint_script}")
        
        # Bash alias
        bashrc = Path.home() / ".bashrc"
        alias_line = f'alias kaliosint="python3 {kaliosint_script}"\n'
        
        try:
            with open(bashrc, 'a') as f:
                f.write(f"\n# KaliOSINT alias\n{alias_line}")
            print("✅ Bash alias added to ~/.bashrc")
            print("   Use 'kaliosint' command to start the tool")
        except:
            print("⚠️  Could not add bash alias")
        
        # Create executable script
        try:
            exe_script = script_dir / "kaliosint"
            with open(exe_script, 'w') as f:
                f.write(f"#!/bin/bash\npython3 {kaliosint_script} \"$@\"\n")
            
            os.chmod(exe_script, 0o755)
            print(f"✅ Executable script created: {exe_script}")
        except:
            print("⚠️  Could not create executable script")

def print_completion_message():
    """Print installation completion message"""
    message = """
╔══════════════════════════════════════════════════════════════╗
║                  Installation Complete!                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                             ║
║  🚀 KaliOSINT is now ready to use!                         ║
║                                                             ║
║  To start the tool:                                         ║
║  • Run: python3 kaliosint.py                               ║
║  • Or use: kaliosint (if alias was set up)                 ║
║                                                             ║
║  📁 Configuration directory: ~/.kaliosint/                 ║
║  📄 Results will be saved in: ~/.kaliosint/results/        ║
║                                                             ║
║  ⚙️  Next steps:                                            ║
║  1. Configure API keys in the tool settings                ║
║  2. Review the documentation                                ║
║  3. Start your OSINT investigations!                       ║
║                                                             ║
║  ⚠️  Remember: Use this tool responsibly and legally!      ║
║                                                             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(message)

def main():
    """Main installation function"""
    try:
        print_banner()
        
        print("🔍 Checking system requirements...")
        check_python_version()
        check_os()
        
        install_python_packages()
        install_system_tools()
        create_config_structure()
        setup_aliases()
        
        print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
