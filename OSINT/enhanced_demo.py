#!/usr/bin/env python3
"""
Enhanced KaliOSINT Demo - Showcasing Toutatis and Mr.Holmes Integration
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

def main():
    console = Console()
    
    # Banner
    console.print(Panel.fit(
        "[bold cyan]KaliOSINT Enhanced Demo[/bold cyan]\n"
        "[yellow]Toutatis & Mr.Holmes Integration Showcase[/yellow]",
        style="blue"
    ))
    
    console.print()
    
    # Enhanced Phone OSINT Features
    console.print(Panel.fit(
        "[bold green]📱 Enhanced Phone OSINT Features (PhoneInfoga-inspired)[/bold green]",
        style="green"
    ))
    
    phone_table = Table(title="Phone Analysis Capabilities")
    phone_table.add_column("Feature", style="cyan")
    phone_table.add_column("Description", style="white")
    phone_table.add_column("APIs Used", style="yellow")
    
    phone_features = [
        ("Comprehensive Analysis", "Multi-API phone number investigation", "NumVerify, Truecaller, Carrier lookup"),
        ("Social Media Search", "Find phone across social platforms", "Facebook, Instagram, WhatsApp"),
        ("Reputation Check", "Spam and fraud detection", "Truecaller, HLR lookup"),
        ("Number Variations", "Generate and test variations", "International formats, prefixes"),
        ("Instagram Lookup", "Toutatis-inspired IG phone search", "Instagram API simulation"),
        ("Geographic Analysis", "Location and carrier mapping", "GeoIP, Carrier databases"),
        ("Format Analysis", "Number validation and parsing", "Google libphonenumber"),
        ("OSINT Correlation", "Cross-reference with breaches", "HaveIBeenPwned, LeakCheck")
    ]
    
    for feature, desc, apis in phone_features:
        phone_table.add_row(feature, desc, apis)
    
    console.print(phone_table)
    console.print()
    
    # Enhanced Username Search Features
    console.print(Panel.fit(
        "[bold magenta]👤 Enhanced Username Search (Mr.Holmes-inspired)[/bold magenta]",
        style="magenta"
    ))
    
    username_table = Table(title="Username Investigation Capabilities")
    username_table.add_column("Feature", style="cyan")
    username_table.add_column("Description", style="white")
    username_table.add_column("Platforms", style="yellow")
    
    username_features = [
        ("Multi-Platform Search", "Search across 200+ platforms", "Social, Gaming, Professional"),
        ("Profile Scraping", "Deep profile data extraction", "Instagram, Twitter, LinkedIn"),
        ("Cross-Platform Analysis", "Correlate accounts across platforms", "Advanced matching algorithms"),
        ("Username Variations", "Generate and test variations", "Common patterns, typos, l33t"),
        ("Instagram Deep Investigation", "Toutatis-style IG analysis", "Profile, posts, connections"),
        ("Reputation Analysis", "Check username reputation", "Spam, fraud, harassment reports"),
        ("Historical Data", "Archive and wayback searches", "Archive.org, cached data"),
        ("OSINT Correlation", "Link to breach data", "Email/phone correlations")
    ]
    
    for feature, desc, platforms in username_features:
        username_table.add_row(feature, desc, platforms)
    
    console.print(username_table)
    console.print()
    
    # Instagram OSINT (Toutatis Integration)
    console.print(Panel.fit(
        "[bold red]📸 Instagram OSINT (Toutatis Integration)[/bold red]",
        style="red"
    ))
    
    instagram_table = Table(title="Instagram Investigation Features")
    instagram_table.add_column("Data Point", style="cyan")
    instagram_table.add_column("Information Extracted", style="white")
    instagram_table.add_column("Method", style="yellow")
    
    instagram_features = [
        ("Profile Data", "Bio, follower count, verification status", "Public API calls"),
        ("Contact Info", "Email, phone (if public)", "Profile parsing"),
        ("Post Analysis", "Content, hashtags, locations", "Media scraping"),
        ("Follower Networks", "Connections and relationships", "Graph analysis"),
        ("Activity Patterns", "Posting times, frequency", "Temporal analysis"),
        ("Location Intelligence", "Geotagged posts, check-ins", "GPS metadata"),
        ("Content Analysis", "Face recognition, objects", "AI/ML processing"),
        ("Historical Data", "Deleted posts, changes", "Archive searches")
    ]
    
    for data_point, info, method in instagram_features:
        instagram_table.add_row(data_point, info, method)
    
    console.print(instagram_table)
    console.print()
    
    # API Integration Status
    console.print(Panel.fit(
        "[bold yellow]🔗 API Integration Status[/bold yellow]",
        style="yellow"
    ))
    
    api_table = Table(title="External API Integrations")
    api_table.add_column("Service", style="cyan")
    api_table.add_column("Purpose", style="white")
    api_table.add_column("Status", style="green")
    api_table.add_column("Rate Limits", style="yellow")
    
    api_integrations = [
        ("NumVerify", "Phone validation & carrier lookup", "✓ Integrated", "1000/month free"),
        ("Truecaller", "Phone reputation & spam detection", "✓ Integrated", "API key required"),
        ("Instagram Basic", "Public profile information", "✓ Integrated", "Rate limited"),
        ("HaveIBeenPwned", "Breach data correlation", "✓ Integrated", "Free tier available"),
        ("Shodan", "Phone/email in IoT devices", "✓ Integrated", "100/month free"),
        ("WhoisXML", "Domain/phone correlations", "✓ Integrated", "1000/month free"),
        ("Social Media APIs", "Platform-specific searches", "✓ Integrated", "Varies by platform"),
        ("TOR/Proxy Support", "Anonymous investigations", "✓ Integrated", "No limits")
    ]
    
    for service, purpose, status, limits in api_integrations:
        api_table.add_row(service, purpose, status, limits)
    
    console.print(api_table)
    console.print()
    
    # Usage Examples
    console.print(Panel.fit(
        "[bold white]💡 Usage Examples[/bold white]",
        style="white"
    ))
    
    examples_text = Text()
    examples_text.append("Enhanced Phone Investigation:\n", style="bold cyan")
    examples_text.append("python kaliosint.py → Option 2 → Option 1 → +1234567890\n\n", style="white")
    
    examples_text.append("Advanced Username Search:\n", style="bold magenta")
    examples_text.append("python kaliosint.py → Option 4 → Option 1 → john_doe\n\n", style="white")
    
    examples_text.append("Instagram Deep Investigation:\n", style="bold red")
    examples_text.append("python kaliosint.py → Option 4 → Option 5 → target_username\n\n", style="white")
    
    examples_text.append("Cross-Platform Username Check:\n", style="bold yellow")
    examples_text.append("python kaliosint.py → Option 4 → Option 3 → social_user\n", style="white")
    
    console.print(Panel(examples_text, title="How to Use Enhanced Features"))
    console.print()
    
    # Security Notice
    console.print(Panel.fit(
        "[bold red]⚠️  SECURITY & LEGAL NOTICE ⚠️[/bold red]\n"
        "[yellow]• Use responsibly and ethically[/yellow]\n"
        "[yellow]• Respect privacy and terms of service[/yellow]\n"
        "[yellow]• Educational and research purposes only[/yellow]\n"
        "[yellow]• Consider using VPN/TOR for anonymity[/yellow]",
        style="red"
    ))

if __name__ == "__main__":
    main()
