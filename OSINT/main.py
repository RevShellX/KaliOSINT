#!/usr/bin/env python3
"""
KaliOSINT Main Entry Point
Advanced OSINT Terminal Tool for Kali Linux
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import and run the main application
try:
    from core.main import KaliOSINT
    
    def main():
        """Main entry point for KaliOSINT"""
        print("🔍 Starting KaliOSINT...")
        
        # Initialize and run the OSINT tool
        osint_tool = KaliOSINT()
        osint_tool.main_menu()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error importing KaliOSINT modules: {e}")
    print("📂 Please ensure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    print("   python scripts/install.py")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n\n👋 KaliOSINT terminated by user")
    sys.exit(0)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
