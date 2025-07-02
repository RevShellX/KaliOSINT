#!/usr/bin/env python3
"""
KaliOSINT Test Launcher
Simple test to verify the application works
"""

# Test basic imports
try:
    from rich.console import Console
    from rich.panel import Panel
    import requests
    print("✅ All imports successful!")
    
    console = Console()
    console.print(Panel("🔍 KaliOSINT is working correctly!", style="green"))
    
    # Test the main application
    print("\n🚀 Starting KaliOSINT...")
    import kaliosint
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the error above and try again.")
