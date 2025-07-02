#!/usr/bin/env python3
"""
Test Enhanced KaliOSINT Integration
"""

import sys
import os

def test_imports():
    """Test if all enhanced modules can be imported"""
    print("Testing Enhanced KaliOSINT Integration...")
    print("=" * 50)
    
    # Test base KaliOSINT
    try:
        from kaliosint import KaliOSINT
        print("✓ Base KaliOSINT module: OK")
    except Exception as e:
        print(f"✗ Base KaliOSINT module: {e}")
        return False
    
    # Test enhanced phone OSINT
    try:
        from enhanced_phone_osint import EnhancedPhoneOSINT
        print("✓ Enhanced Phone OSINT module: OK")
    except Exception as e:
        print(f"✗ Enhanced Phone OSINT module: {e}")
    
    # Test enhanced username search
    try:
        from enhanced_username_search import EnhancedUsernameSearch
        print("✓ Enhanced Username Search module: OK")
    except Exception as e:
        print(f"✗ Enhanced Username Search module: {e}")
    
    # Test social media OSINT
    try:
        from social_media_osint import SocialMediaOSINT
        print("✓ Social Media OSINT module: OK")
    except Exception as e:
        print(f"✗ Social Media OSINT module: {e}")
    
    # Test core dependencies
    print("\nTesting Core Dependencies:")
    dependencies = [
        'requests', 'rich', 'beautifulsoup4', 'phonenumbers', 
        'instaloader', 'aiohttp', 'fake_useragent', 'fuzzywuzzy'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep}: OK")
        except ImportError as e:
            print(f"✗ {dep}: {e}")
    
    print("\n" + "=" * 50)
    print("Integration Test Complete!")
    
    return True

def test_enhanced_features():
    """Test enhanced features initialization"""
    print("\nTesting Enhanced Features Initialization...")
    print("-" * 40)
    
    try:
        from kaliosint import KaliOSINT
        osint_tool = KaliOSINT()
        print("✓ KaliOSINT tool initialized successfully")
        
        # Test if enhanced methods are available
        enhanced_methods = [
            '_basic_phone_analysis_menu',
            '_basic_social_media_menu'
        ]
        
        for method in enhanced_methods:
            if hasattr(osint_tool, method):
                print(f"✓ Enhanced method {method}: Available")
            else:
                print(f"✗ Enhanced method {method}: Not found")
                
    except Exception as e:
        print(f"✗ Failed to initialize enhanced features: {e}")

def main():
    """Main test function"""
    print("🔍 KaliOSINT Enhanced Integration Test")
    print("📱 Toutatis & Mr.Holmes Integration")
    print()
    
    if test_imports():
        test_enhanced_features()
        print("\n🎉 All tests completed!")
        print("\n🚀 Ready to run enhanced KaliOSINT!")
        print("   Use: python kaliosint.py")
    else:
        print("\n❌ Some tests failed. Check dependencies.")

if __name__ == "__main__":
    main()
