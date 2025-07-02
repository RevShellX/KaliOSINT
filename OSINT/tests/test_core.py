#!/usr/bin/env python3
"""
KaliOSINT Core Tests
Basic test suite for core functionality
"""

import sys
import pytest
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class TestCoreImports:
    """Test that core modules can be imported"""
    
    def test_import_main(self):
        """Test importing the main KaliOSINT class"""
        try:
            from core.main import KaliOSINT
            assert KaliOSINT is not None
        except ImportError as e:
            pytest.fail(f"Failed to import KaliOSINT: {e}")
    
    def test_create_instance(self):
        """Test creating a KaliOSINT instance"""
        try:
            from core.main import KaliOSINT
            osint = KaliOSINT()
            assert osint is not None
            assert hasattr(osint, 'console')
            assert hasattr(osint, 'config')
        except Exception as e:
            pytest.fail(f"Failed to create KaliOSINT instance: {e}")

class TestEnhancedModules:
    """Test enhanced OSINT modules"""
    
    def test_import_phone_osint(self):
        """Test importing enhanced phone OSINT module"""
        try:
            from modules.enhanced.phone_osint import EnhancedPhoneOSINT
            assert EnhancedPhoneOSINT is not None
        except ImportError:
            pytest.skip("Enhanced phone OSINT module not available")
    
    def test_import_username_search(self):
        """Test importing enhanced username search module"""
        try:
            from modules.enhanced.username_search import EnhancedUsernameSearch
            assert EnhancedUsernameSearch is not None
        except ImportError:
            pytest.skip("Enhanced username search module not available")
    
    def test_import_social_media(self):
        """Test importing social media module"""
        try:
            from modules.enhanced.social_media import SocialMediaOSINT
            assert SocialMediaOSINT is not None
        except ImportError:
            pytest.skip("Social media OSINT module not available")

class TestConfiguration:
    """Test configuration management"""
    
    def test_config_directory_creation(self):
        """Test that config directories can be created"""
        try:
            from core.main import KaliOSINT
            osint = KaliOSINT()
            assert osint.config_dir.exists()
        except Exception as e:
            pytest.fail(f"Failed to create config directory: {e}")
    
    def test_load_config(self):
        """Test loading configuration"""
        try:
            from core.main import KaliOSINT
            osint = KaliOSINT()
            config = osint.load_config()
            assert isinstance(config, dict)
        except Exception as e:
            pytest.fail(f"Failed to load config: {e}")

class TestDependencies:
    """Test that required dependencies are available"""
    
    def test_rich_import(self):
        """Test Rich library import"""
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            assert Console is not None
            assert Table is not None
            assert Panel is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Rich: {e}")
    
    def test_requests_import(self):
        """Test requests library import"""
        try:
            import requests
            assert requests is not None
        except ImportError as e:
            pytest.fail(f"Failed to import requests: {e}")
    
    def test_phonenumbers_import(self):
        """Test phonenumbers library import"""
        try:
            import phonenumbers
            from phonenumbers import geocoder, carrier
            assert phonenumbers is not None
            assert geocoder is not None
            assert carrier is not None
        except ImportError as e:
            pytest.fail(f"Failed to import phonenumbers: {e}")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
