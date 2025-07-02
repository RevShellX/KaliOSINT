#!/usr/bin/env python3
"""
Social Media and Dark Web OSINT Tools
Advanced social media intelligence gathering
"""

import requests
import json
import time
import re
from datetime import datetime
import subprocess
from pathlib import Path

class SocialMediaOSINT:
    def __init__(self, parent):
        self.parent = parent
        self.console = parent.console
        self.config = parent.config
        self.save_result = parent.save_result
    
    def twitter_analysis(self, username):
        """Analyze Twitter/X profile"""
        try:
            self.console.print(f"\n[bold green]Twitter Analysis for @{username}[/bold green]")
            
            # Twitter API v2 would require bearer token
            # For demonstration, we'll use public endpoints
            
            twitter_info = {
                "username": username,
                "profile_url": f"https://twitter.com/{username}",
                "search_url": f"https://twitter.com/search?q=from%3A{username}",
                "analysis_date": datetime.now().isoformat()
            }
            
            # Basic profile check
            try:
                response = requests.get(f"https://twitter.com/{username}", timeout=10)
                if response.status_code == 200:
                    twitter_info["profile_exists"] = True
                    # Simple content analysis
                    content = response.text
                    
                    # Extract basic information from HTML (basic scraping)
                    bio_match = re.search(r'"description":"([^"]*)"', content)
                    if bio_match:
                        twitter_info["bio"] = bio_match.group(1)
                    
                    followers_match = re.search(r'"followers_count":(\d+)', content)
                    if followers_match:
                        twitter_info["followers_count"] = int(followers_match.group(1))
                    
                    following_match = re.search(r'"friends_count":(\d+)', content)
                    if following_match:
                        twitter_info["following_count"] = int(following_match.group(1))
                        
                else:
                    twitter_info["profile_exists"] = False
                    
            except Exception as e:
                twitter_info["error"] = str(e)
            
            # Display results
            from rich.table import Table
            twitter_table = Table(title=f"Twitter Analysis: @{username}")
            twitter_table.add_column("Field", style="cyan")
            twitter_table.add_column("Value", style="white")
            
            for key, value in twitter_info.items():
                if key != "analysis_date":
                    twitter_table.add_row(key.replace("_", " ").title(), str(value))
            
            self.console.print(twitter_table)
            
            # Save results
            self.save_result("twitter_analysis", username, twitter_info)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")
    
    def instagram_analysis(self, username):
        """Analyze Instagram profile"""
        try:
            self.console.print(f"\n[bold green]Instagram Analysis for {username}[/bold green]")
            
            instagram_info = {
                "username": username,
                "profile_url": f"https://instagram.com/{username}",
                "analysis_date": datetime.now().isoformat()
            }
            
            # Basic profile check
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(f"https://instagram.com/{username}/", 
                                      headers=headers, timeout=10)
                
                if response.status_code == 200:
                    instagram_info["profile_exists"] = True
                    content = response.text
                    
                    # Basic information extraction
                    if 'followers' in content:
                        instagram_info["has_followers_info"] = True
                    
                    if 'posts' in content:
                        instagram_info["has_posts"] = True
                        
                else:
                    instagram_info["profile_exists"] = False
                    
            except Exception as e:
                instagram_info["error"] = str(e)
            
            # Additional OSINT techniques
            instagram_info["related_searches"] = [
                f"site:instagram.com/{username}",
                f"\"{username}\" site:instagram.com",
                f"instagram.com/{username} archived"
            ]
            
            # Display results
            from rich.table import Table
            instagram_table = Table(title=f"Instagram Analysis: {username}")
            instagram_table.add_column("Field", style="cyan")
            instagram_table.add_column("Value", style="white")
            
            for key, value in instagram_info.items():
                if key not in ["analysis_date", "related_searches"]:
                    instagram_table.add_row(key.replace("_", " ").title(), str(value))
            
            self.console.print(instagram_table)
            
            if "related_searches" in instagram_info:
                self.console.print("\n[bold yellow]Related Search Queries:[/bold yellow]")
                for search in instagram_info["related_searches"]:
                    self.console.print(f"• {search}")
            
            # Save results
            self.save_result("instagram_analysis", username, instagram_info)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")
    
    def linkedin_search(self, name):
        """LinkedIn profile search"""
        try:
            self.console.print(f"\n[bold green]LinkedIn Search for {name}[/bold green]")
            
            # Generate possible LinkedIn URLs
            name_variations = [
                name.lower().replace(" ", "-"),
                name.lower().replace(" ", ""),
                name.lower().replace(" ", "."),
                "-".join(name.lower().split()),
                "".join(name.lower().split())
            ]
            
            linkedin_info = {
                "search_name": name,
                "possible_profiles": [],
                "search_urls": [],
                "analysis_date": datetime.now().isoformat()
            }
            
            # Generate search URLs
            for variation in name_variations:
                linkedin_info["possible_profiles"].append(f"https://linkedin.com/in/{variation}")
            
            # Google search URLs for LinkedIn profiles
            linkedin_info["search_urls"] = [
                f"site:linkedin.com/in \"{name}\"",
                f"site:linkedin.com/pub \"{name}\"",
                f"\"{name}\" LinkedIn profile",
                f"\"{name}\" site:linkedin.com"
            ]
            
            # Display results
            from rich.table import Table
            linkedin_table = Table(title=f"LinkedIn Search: {name}")
            linkedin_table.add_column("Type", style="cyan")
            linkedin_table.add_column("URLs/Queries", style="white")
            
            linkedin_table.add_row("Possible Profiles", "\n".join(linkedin_info["possible_profiles"][:5]))
            linkedin_table.add_row("Search Queries", "\n".join(linkedin_info["search_urls"]))
            
            self.console.print(linkedin_table)
            
            # Save results
            self.save_result("linkedin_search", name, linkedin_info)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")

class DarkWebOSINT:
    def __init__(self, parent):
        self.parent = parent
        self.console = parent.console
        self.config = parent.config
        self.save_result = parent.save_result
    
    def dark_web_search_guide(self):
        """Provide dark web search guidance"""
        try:
            self.console.print("\n[bold red]Dark Web Investigation Guide[/bold red]")
            
            from rich.panel import Panel
            warning_panel = Panel(
                "[bold red]⚠️  WARNING ⚠️[/bold red]\n\n"
                "Dark web investigation requires extreme caution:\n"
                "• Use Tor Browser with proper security settings\n"
                "• Use a VPN for additional anonymity\n"
                "• Never download files or enter personal information\n"
                "• Be aware of legal implications in your jurisdiction\n"
                "• Consider using Tails OS for maximum security",
                style="red",
                title="Security Warning"
            )
            self.console.print(warning_panel)
            
            from rich.table import Table
            darkweb_table = Table(title="Dark Web Search Resources")
            darkweb_table.add_column("Resource Type", style="cyan")
            darkweb_table.add_column("Description", style="white")
            darkweb_table.add_column("Access Method", style="yellow")
            
            resources = [
                ("Search Engines", "Ahmia, DuckDuckGo Onion", "Tor Browser"),
                ("Forums", "Various discussion forums", "Tor Browser + Caution"),
                ("Marketplaces", "Commercial platforms", "Tor Browser + VPN"),
                ("Leak Sites", "Data breach information", "Tor Browser + VPN"),
                ("Paste Sites", "Anonymous text sharing", "Tor Browser"),
                ("Social Networks", "Anonymous social platforms", "Tor Browser")
            ]
            
            for resource_type, description, access_method in resources:
                darkweb_table.add_row(resource_type, description, access_method)
            
            self.console.print(darkweb_table)
            
            # Tools and techniques
            self.console.print("\n[bold yellow]Recommended Tools:[/bold yellow]")
            tools = [
                "• Tor Browser (official)",
                "• Tails OS (for maximum anonymity)",
                "• VPN service (additional layer)",
                "• OnionScan (onion service analysis)",
                "• Ahmia (clearnet dark web search)",
                "• Hunchly (investigation case management)"
            ]
            
            for tool in tools:
                self.console.print(tool)
            
            # Legal considerations
            legal_panel = Panel(
                "[bold yellow]Legal Considerations:[/bold yellow]\n\n"
                "• Research local laws regarding dark web access\n"
                "• Understand the difference between access and participation\n"
                "• Document your methodology for legal compliance\n"
                "• Consider law enforcement coordination for serious cases\n"
                "• Maintain ethical boundaries in your investigation",
                style="yellow",
                title="Legal & Ethical Guidelines"
            )
            self.console.print(legal_panel)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")
    
    def tor_setup_guide(self):
        """Provide Tor setup guidance"""
        try:
            self.console.print("\n[bold cyan]Tor Browser Setup Guide[/bold cyan]")
            
            from rich.table import Table
            setup_table = Table(title="Tor Browser Configuration")
            setup_table.add_column("Step", style="cyan")
            setup_table.add_column("Action", style="white")
            setup_table.add_column("Security Level", style="yellow")
            
            steps = [
                ("1", "Download Tor Browser from official site", "Essential"),
                ("2", "Verify download signature", "Essential"),
                ("3", "Configure security level to 'Safest'", "High"),
                ("4", "Disable JavaScript", "High"),
                ("5", "Use bridges if in restricted country", "Medium"),
                ("6", "Never download files", "Essential"),
                ("7", "Clear cookies after each session", "High"),
                ("8", "Use VPN for additional layer", "Medium")
            ]
            
            for step, action, security in steps:
                setup_table.add_row(step, action, security)
            
            self.console.print(setup_table)
            
            # Security tips
            from rich.panel import Panel
            security_panel = Panel(
                "[bold green]Security Best Practices:[/bold green]\n\n"
                "• Always verify SSL certificates\n"
                "• Never enable plugins or add-ons\n"
                "• Don't log into personal accounts\n"
                "• Use separate computer/VM if possible\n"
                "• Monitor network traffic\n"
                "• Keep detailed investigation logs",
                style="green",
                title="Security Best Practices"
            )
            self.console.print(security_panel)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")

class CryptoOSINT:
    def __init__(self, parent):
        self.parent = parent
        self.console = parent.console
        self.config = parent.config
        self.save_result = parent.save_result
    
    def bitcoin_address_analysis(self, address):
        """Analyze Bitcoin address"""
        try:
            self.console.print(f"\n[bold green]Bitcoin Address Analysis for {address}[/bold green]")
            
            # Basic address validation
            bitcoin_info = {
                "address": address,
                "analysis_date": datetime.now().isoformat(),
                "address_type": self.identify_bitcoin_address_type(address)
            }
            
            # Check address format
            if self.validate_bitcoin_address(address):
                bitcoin_info["valid_format"] = True
                
                # Free APIs for blockchain analysis
                apis_to_try = [
                    f"https://blockstream.info/api/address/{address}",
                    f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
                ]
                
                for api_url in apis_to_try:
                    try:
                        response = requests.get(api_url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            bitcoin_info["blockchain_data"] = data
                            break
                    except:
                        continue
                
            else:
                bitcoin_info["valid_format"] = False
            
            # Additional analysis resources
            bitcoin_info["analysis_resources"] = [
                f"https://www.blockchain.com/btc/address/{address}",
                f"https://blockstream.info/address/{address}",
                f"https://live.blockcypher.com/btc/address/{address}/",
                f"https://btc.com/btc/address/{address}"
            ]
            
            # Display results
            from rich.table import Table
            bitcoin_table = Table(title=f"Bitcoin Address Analysis")
            bitcoin_table.add_column("Field", style="cyan")
            bitcoin_table.add_column("Value", style="white")
            
            for key, value in bitcoin_info.items():
                if key not in ["blockchain_data", "analysis_resources"]:
                    bitcoin_table.add_row(key.replace("_", " ").title(), str(value))
            
            self.console.print(bitcoin_table)
            
            if "analysis_resources" in bitcoin_info:
                self.console.print("\n[bold yellow]Analysis Resources:[/bold yellow]")
                for resource in bitcoin_info["analysis_resources"]:
                    self.console.print(f"• {resource}")
            
            # Save results
            self.save_result("bitcoin_analysis", address, bitcoin_info)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        from rich.prompt import Prompt
        Prompt.ask("\nPress Enter to continue")
    
    def validate_bitcoin_address(self, address):
        """Basic Bitcoin address validation"""
        # Basic format validation
        if len(address) < 26 or len(address) > 35:
            return False
        
        # Check for valid characters
        valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        for char in address:
            if char not in valid_chars:
                return False
        
        return True
    
    def identify_bitcoin_address_type(self, address):
        """Identify Bitcoin address type"""
        if address.startswith('1'):
            return "P2PKH (Legacy)"
        elif address.startswith('3'):
            return "P2SH (Script Hash)"
        elif address.startswith('bc1'):
            return "Bech32 (SegWit)"
        else:
            return "Unknown"
