#!/usr/bin/env python3
"""
KaliOSINT - Advanced OSINT Terminal Tool
A comprehensive Open Source Intelligence gathering tool for Kali Linux
"""

import os
import sys
import json
import time
import re
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

# Rich console for beautiful output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich.layout import Layout

# Core libraries
import click
import pyfiglet
from colorama import init, Fore, Back, Style
from tabulate import tabulate

# OSINT specific imports
import whois
import dns.resolver
import phonenumbers
from phonenumbers import geocoder, carrier
import shodan
import nmap
import feedparser
from urllib.parse import urlparse, urljoin
import validators
from ipwhois import IPWhois
import socket
import ssl
# import geoip2.database  # Commented out for now

# Initialize colorama and rich console
init(autoreset=True)
console = Console()

class KaliOSINT:
    def __init__(self):
        self.console = Console()
        self.config_dir = Path.home() / ".kaliosint"
        self.config_file = self.config_dir / "config.json"
        self.results_dir = self.config_dir / "results"
        self.setup_directories()
        self.config = self.load_config()
        
        # API Keys (to be configured by user)
        self.shodan_api = self.config.get('shodan_api', '')
        self.censys_api_id = self.config.get('censys_api_id', '')
        self.censys_api_secret = self.config.get('censys_api_secret', '')
        
    def setup_directories(self):
        """Create necessary directories"""
        self.config_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def banner(self):
        """Display KaliOSINT banner"""
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
        
        self.console.print(banner_panel)
        self.console.print()
    
    def main_menu(self):
        """Display main menu and handle user input"""
        while True:
            self.console.clear()
            self.banner()
            
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
                menu_table.add_row(option, desc, f"[{self.get_category_color(category)}]{category}[/{self.get_category_color(category)}]")
            
            self.console.print(menu_table)
            self.console.print()
            
            choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=[str(i) for i in range(16)])
            
            if choice == "0":
                self.console.print("[bold red]Goodbye! 👋[/bold red]")
                sys.exit(0)
            elif choice == "1":
                self.domain_ip_menu()
            elif choice == "2":
                self.phone_analysis_menu()
            elif choice == "3":
                self.email_investigation_menu()
            elif choice == "4":
                self.social_media_menu()
            elif choice == "5":
                self.website_analysis_menu()
            elif choice == "6":
                self.search_intelligence_menu()
            elif choice == "7":
                self.crypto_investigation_menu()
            elif choice == "8":
                self.network_scanning_menu()
            elif choice == "9":
                self.metadata_analysis_menu()
            elif choice == "10":
                self.geolocation_menu()
            elif choice == "11":
                self.dark_web_menu()
            elif choice == "12":
                self.breach_data_menu()
            elif choice == "13":
                self.company_intelligence_menu()
            elif choice == "14":
                self.config_menu()
            elif choice == "15":
                self.generate_report()
    
    def get_category_color(self, category):
        """Get color for category"""
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

    def domain_ip_menu(self):
        """Domain and IP investigation submenu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Domain & IP Investigation[/bold cyan]", style="blue"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")
            
            options = [
                ("1", "WHOIS Lookup"),
                ("2", "DNS Records Analysis"),
                ("3", "Subdomain Enumeration"),
                ("4", "IP Geolocation"),
                ("5", "Port Scanning"),
                ("6", "SSL Certificate Analysis"),
                ("7", "Reverse IP Lookup"),
                ("8", "Domain History"),
                ("0", "Back to Main Menu")
            ]
            
            for option, tool in options:
                table.add_row(option, tool)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                target = Prompt.ask("Enter domain or IP")
                self.whois_lookup(target)
            elif choice == "2":
                domain = Prompt.ask("Enter domain")
                self.dns_analysis(domain)
            elif choice == "3":
                domain = Prompt.ask("Enter domain")
                self.subdomain_enum(domain)
            elif choice == "4":
                ip = Prompt.ask("Enter IP address")
                self.ip_geolocation(ip)
            elif choice == "5":
                target = Prompt.ask("Enter IP or domain")
                self.port_scan(target)
            elif choice == "6":
                domain = Prompt.ask("Enter domain")
                self.ssl_analysis(domain)
            elif choice == "7":
                ip = Prompt.ask("Enter IP address")
                self.reverse_ip_lookup(ip)
            elif choice == "8":
                domain = Prompt.ask("Enter domain")
                self.domain_history(domain)
    
    def whois_lookup(self, target):
        """Perform WHOIS lookup"""
        try:
            with self.console.status(f"[bold green]Performing WHOIS lookup for {target}..."):
                w = whois.whois(target)
            
            self.console.print(f"\n[bold green]WHOIS Information for {target}[/bold green]")
            
            info_table = Table(title="WHOIS Data")
            info_table.add_column("Field", style="cyan")
            info_table.add_column("Value", style="white")
            
            whois_fields = [
                ("Domain Name", str(w.domain_name) if w.domain_name else "N/A"),
                ("Registrar", str(w.registrar) if w.registrar else "N/A"),
                ("Creation Date", str(w.creation_date) if w.creation_date else "N/A"),
                ("Expiration Date", str(w.expiration_date) if w.expiration_date else "N/A"),
                ("Updated Date", str(w.updated_date) if w.updated_date else "N/A"),
                ("Status", str(w.status) if w.status else "N/A"),
                ("Name Servers", str(w.name_servers) if w.name_servers else "N/A"),
                ("Organization", str(w.org) if w.org else "N/A"),
                ("Country", str(w.country) if w.country else "N/A"),
                ("Email", str(w.emails) if w.emails else "N/A")
            ]
            
            for field, value in whois_fields:
                info_table.add_row(field, value)
            
            self.console.print(info_table)
            
            # Save results
            self.save_result("whois", target, {
                "domain": str(w.domain_name) if w.domain_name else "N/A",
                "registrar": str(w.registrar) if w.registrar else "N/A",
                "creation_date": str(w.creation_date) if w.creation_date else "N/A",
                "expiration_date": str(w.expiration_date) if w.expiration_date else "N/A",
                "raw_data": str(w)
            })
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")
    
    def dns_analysis(self, domain):
        """Perform DNS analysis"""
        try:
            self.console.print(f"\n[bold green]DNS Analysis for {domain}[/bold green]")
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            results = {}
            
            dns_table = Table(title="DNS Records")
            dns_table.add_column("Type", style="cyan")
            dns_table.add_column("Value", style="white")
            
            for record_type in record_types:
                try:
                    with self.console.status(f"[bold green]Querying {record_type} records..."):
                        answers = dns.resolver.resolve(domain, record_type)
                        records = [str(rdata) for rdata in answers]
                        results[record_type] = records
                        
                        for record in records:
                            dns_table.add_row(record_type, record)
                            
                except dns.resolver.NXDOMAIN:
                    results[record_type] = ["Domain not found"]
                except dns.resolver.NoAnswer:
                    results[record_type] = ["No records found"]
                except Exception as e:
                    results[record_type] = [f"Error: {str(e)}"]
            
            self.console.print(dns_table)
            
            # Save results
            self.save_result("dns", domain, results)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")
    
    def subdomain_enum(self, domain):
        """Enumerate subdomains"""
        try:
            self.console.print(f"\n[bold green]Subdomain Enumeration for {domain}[/bold green]")
            
            # Common subdomain wordlist
            common_subdomains = [
                'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
                'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'api', 'admin', 'dev',
                'test', 'staging', 'blog', 'shop', 'support', 'help', 'portal', 'mobile',
                'cdn', 'static', 'assets', 'images', 'img', 'video', 'videos', 'secure',
                'login', 'auth', 'ssh', 'vpn', 'git', 'gitlab', 'github', 'bitbucket'
            ]
            
            found_subdomains = []
            
            with self.console.status("[bold green]Enumerating subdomains..."):
                for sub in track(common_subdomains, description="Checking subdomains..."):
                    subdomain = f"{sub}.{domain}"
                    try:
                        dns.resolver.resolve(subdomain, 'A')
                        found_subdomains.append(subdomain)
                    except:
                        pass
            
            if found_subdomains:
                sub_table = Table(title="Found Subdomains")
                sub_table.add_column("Subdomain", style="green")
                sub_table.add_column("Status", style="cyan")
                
                for subdomain in found_subdomains:
                    sub_table.add_row(subdomain, "Active")
                
                self.console.print(sub_table)
                
                # Save results
                self.save_result("subdomains", domain, {"found_subdomains": found_subdomains})
            else:
                self.console.print("[yellow]No subdomains found in common wordlist[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")
    
    def phone_analysis_menu(self):
        """Enhanced phone number analysis menu"""
        try:
            from src.modules.enhanced.phone_osint import AdvancedPhoneOSINT
            enhanced_phone = AdvancedPhoneOSINT(self)
            
            while True:
                self.console.clear()
                self.console.print(Panel("[bold cyan]Enhanced Phone Number Analysis[/bold cyan]", style="green"))
                
                table = Table()
                table.add_column("Option", style="cyan")
                table.add_column("Tool", style="white")
                table.add_column("Description", style="yellow")
                
                options = [
                    ("1", "Comprehensive Phone Analysis", "Full analysis with multiple APIs"),
                    ("2", "Social Media Phone Search", "Search phone across social platforms"),
                    ("3", "Phone Reputation Check", "Check phone reputation & spam reports"),
                    ("4", "Phone Variations & Formats", "Generate and test phone variations"),
                    ("5", "Instagram Phone Lookup", "Toutatis-inspired Instagram search"),
                    ("6", "Basic Phone Validation", "Standard validation & carrier info"),
                    ("7", "Phone Geolocation", "Geographic location analysis"),
                    ("8", "Phone Format Analysis", "Number format and country analysis"),
                    ("0", "Back to Main Menu", "")
                ]
                
                for option, tool, desc in options:
                    table.add_row(option, tool, desc)
                
                self.console.print(table)
                choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
                
                if choice == "0":
                    break
                elif choice == "1":
                    phone = Prompt.ask("Enter phone number (with country code)")
                    enhanced_phone.comprehensive_phone_analysis(phone)
                elif choice == "2":
                    phone = Prompt.ask("Enter phone number")
                    enhanced_phone.social_media_phone_search(phone)
                elif choice == "3":
                    phone = Prompt.ask("Enter phone number")
                    enhanced_phone.phone_reputation_check(phone)
                elif choice == "4":
                    phone = Prompt.ask("Enter phone number")
                    enhanced_phone.phone_variations_analysis(phone)
                elif choice == "5":
                    phone = Prompt.ask("Enter phone number")
                    enhanced_phone.instagram_phone_lookup(phone)
                elif choice == "6":
                    phone = Prompt.ask("Enter phone number (with country code)")
                    self.phone_validation(phone)
                elif choice == "7":
                    phone = Prompt.ask("Enter phone number (with country code)")
                    self.phone_geolocation(phone)
                elif choice == "8":
                    phone = Prompt.ask("Enter phone number")
                    self.phone_format_analysis(phone)
        except ImportError as e:
            self.console.print(f"[red]Enhanced phone module not available: {e}[/red]")
            self.console.print("[yellow]Falling back to basic phone analysis...[/yellow]")
            self._basic_phone_analysis_menu()
    
    def _basic_phone_analysis_menu(self):
        """Basic phone number analysis menu (fallback)"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Phone Number Analysis[/bold cyan]", style="green"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")
            
            options = [
                ("1", "Phone Number Validation"),
                ("2", "Carrier Information"),
                ("3", "Geolocation by Phone"),
                ("4", "Number Format Analysis"),
                ("5", "Social Media Search by Phone"),
                ("0", "Back to Main Menu")
            ]
            
            for option, tool in options:
                table.add_row(option, tool)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                phone = Prompt.ask("Enter phone number (with country code)")
                self.phone_validation(phone)
            elif choice == "2":
                phone = Prompt.ask("Enter phone number (with country code)")
                self.phone_carrier_info(phone)
            elif choice == "3":
                phone = Prompt.ask("Enter phone number (with country code)")
                self.phone_geolocation(phone)
            elif choice == "4":
                phone = Prompt.ask("Enter phone number")
                self.phone_format_analysis(phone)
            elif choice == "5":
                phone = Prompt.ask("Enter phone number")
                self.social_phone_search(phone)
    
    def email_investigation_menu(self):
        """Email investigation menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Email Investigation[/bold cyan]", style="green"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")
            
            options = [
                ("1", "Email Validation"),
                ("2", "Breach Data Search"),
                ("3", "Email Header Analysis"),
                ("4", "Social Media by Email"),
                ("5", "Domain from Email Analysis"),
                ("6", "Email Pattern Generation"),
                ("0", "Back to Main Menu")
            ]
            
            for option, tool in options:
                table.add_row(option, tool)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                email = Prompt.ask("Enter email address")
                self.email_validation(email)
            elif choice == "2":
                email = Prompt.ask("Enter email address")
                self.breach_search(email)
            elif choice == "3":
                self.email_header_analysis()
            elif choice == "4":
                email = Prompt.ask("Enter email address")
                self.social_email_search(email)
            elif choice == "5":
                email = Prompt.ask("Enter email address")
                self.email_domain_analysis(email)
            elif choice == "6":
                self.email_pattern_generator()
    
    def social_media_menu(self):
        """Enhanced social media intelligence menu"""
        try:
            from src.modules.enhanced.social_media import SocialMediaOSINT
            from src.modules.enhanced.username_search import EnhancedUsernameSearch
            
            social_osint = SocialMediaOSINT(self)
            enhanced_username = EnhancedUsernameSearch(self)
            
            while True:
                self.console.clear()
                self.console.print(Panel("[bold cyan]Enhanced Social Media Intelligence[/bold cyan]", style="magenta"))
                
                table = Table()
                table.add_column("Option", style="cyan")
                table.add_column("Platform", style="white")
                table.add_column("Description", style="yellow")
                
                options = [
                    ("1", "Advanced Username Search", "Mr.Holmes-inspired multi-platform search"),
                    ("2", "Username Variations & Analysis", "Generate and test username variations"),
                    ("3", "Cross-Platform Username Check", "Check username across 200+ platforms"),
                    ("4", "Profile Scraping & Analysis", "Deep profile analysis and data extraction"),
                    ("5", "Instagram Deep Investigation", "Toutatis-inspired Instagram OSINT"),
                    ("6", "Twitter/X Analysis", "Analyze Twitter profiles and tweets"),
                    ("7", "LinkedIn Intelligence", "LinkedIn profile search"),
                    ("8", "Facebook Investigation", "Facebook profile analysis"),
                    ("9", "TikTok Analysis", "TikTok profile investigation"),
                    ("10", "YouTube Channel Analysis", "YouTube channel investigation"),
                    ("11", "Reddit User Analysis", "Reddit user investigation"),
                    ("12", "Basic Username Search", "Simple username search"),
                    ("0", "Back to Main Menu", "")
                ]
                
                for option, platform, desc in options:
                    table.add_row(option, platform, desc)
                
                self.console.print(table)
                choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
                
                if choice == "0":
                    break
                elif choice == "1":
                    username = Prompt.ask("Enter username")
                    enhanced_username.advanced_username_search(username)
                elif choice == "2":
                    username = Prompt.ask("Enter username")
                    enhanced_username.username_variations_analysis(username)
                elif choice == "3":
                    username = Prompt.ask("Enter username")
                    enhanced_username.cross_platform_username_check(username)
                elif choice == "4":
                    username = Prompt.ask("Enter username")
                    platform = Prompt.ask("Enter platform (optional)", default="auto")
                    enhanced_username.profile_scraping_analysis(username, platform)
                elif choice == "5":
                    username = Prompt.ask("Enter Instagram username")
                    enhanced_username.instagram_deep_investigation(username)
                elif choice == "6":
                    username = Prompt.ask("Enter Twitter username (without @)")
                    social_osint.twitter_analysis(username)
                elif choice == "7":
                    name = Prompt.ask("Enter full name for LinkedIn search")
                    social_osint.linkedin_search(name)
                elif choice == "8":
                    username = Prompt.ask("Enter Facebook username")
                    social_osint.facebook_analysis(username)
                elif choice == "9":
                    username = Prompt.ask("Enter TikTok username")
                    social_osint.tiktok_analysis(username)
                elif choice == "10":
                    username = Prompt.ask("Enter YouTube channel name/ID")
                    social_osint.youtube_analysis(username)
                elif choice == "11":
                    username = Prompt.ask("Enter Reddit username")
                    social_osint.reddit_analysis(username)
                elif choice == "12":
                    username = Prompt.ask("Enter username")
                    self.username_search(username)
        except ImportError as e:
            self.console.print(f"[red]Enhanced social media modules not available: {e}[/red]")
            self.console.print("[yellow]Falling back to basic social media analysis...[/yellow]")
            self._basic_social_media_menu()
    
    def _basic_social_media_menu(self):
        """Basic social media intelligence menu (fallback)"""
        try:
            from src.modules.enhanced.social_media import SocialMediaOSINT
            social_osint = SocialMediaOSINT(self)
            
            while True:
                self.console.clear()
                self.console.print(Panel("[bold cyan]Social Media Intelligence[/bold cyan]", style="magenta"))
                
                table = Table()
                table.add_column("Option", style="cyan")
                table.add_column("Platform", style="white")
                table.add_column("Description", style="yellow")
                
                options = [
                    ("1", "Username Search", "Search username across platforms"),
                    ("2", "Twitter/X Analysis", "Analyze Twitter profiles and tweets"),
                    ("3", "Instagram Investigation", "Instagram profile analysis"),
                    ("4", "LinkedIn Intelligence", "LinkedIn profile search"),
                    ("5", "Facebook Investigation", "Facebook profile analysis"),
                    ("6", "TikTok Analysis", "TikTok profile investigation"),
                    ("7", "YouTube Channel Analysis", "YouTube channel investigation"),
                    ("8", "Reddit User Analysis", "Reddit user investigation"),
                    ("0", "Back to Main Menu", "")
                ]
                
                for option, platform, desc in options:
                    table.add_row(option, platform, desc)
                
                self.console.print(table)
                choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
                
                if choice == "0":
                    break
                elif choice == "1":
                    username = Prompt.ask("Enter username")
                    self.username_search(username)
                elif choice == "2":
                    username = Prompt.ask("Enter Twitter username (without @)")
                    social_osint.twitter_analysis(username)
                elif choice == "3":
                    username = Prompt.ask("Enter Instagram username")
                    social_osint.instagram_analysis(username)
                elif choice == "4":
                    name = Prompt.ask("Enter full name for LinkedIn search")
                    social_osint.linkedin_search(name)
        except ImportError:
            self.console.print("[red]Social media module not available[/red]")
            Prompt.ask("Press Enter to continue")
    
    def website_analysis_menu(self):
        """Website analysis menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Website Analysis[/bold cyan]", style="cyan"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")
            
            options = [
                ("1", "Website Technology Stack"),
                ("2", "Robots.txt Analysis"),
                ("3", "Sitemap Discovery"),
                ("4", "HTTP Headers Analysis"),
                ("5", "Website Screenshot"),
                ("6", "Form Analysis"),
                ("7", "JavaScript Files Analysis"),
                ("8", "Cookie Analysis"),
                ("9", "Website History (Wayback)"),
                ("10", "Security Headers Check"),
                ("0", "Back to Main Menu")
            ]
            
            for option, tool in options:
                table.add_row(option, tool)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                url = Prompt.ask("Enter website URL")
                self.website_tech_stack(url)
            elif choice == "2":
                url = Prompt.ask("Enter website URL")
                self.robots_analysis(url)
            elif choice == "3":
                url = Prompt.ask("Enter website URL")
                self.sitemap_discovery(url)
            elif choice == "4":
                url = Prompt.ask("Enter website URL")
                self.http_headers_analysis(url)
            elif choice == "9":
                url = Prompt.ask("Enter website URL")
                self.wayback_analysis(url)
            elif choice == "10":
                url = Prompt.ask("Enter website URL")
                self.security_headers_check(url)
    
    def search_intelligence_menu(self):
        """Search engine intelligence menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Search Engine Intelligence[/bold cyan]", style="yellow"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Search Type", style="white")
            
            options = [
                ("1", "Google Dorking Guide"),
                ("2", "Bing Search Operators"),
                ("3", "DuckDuckGo Search"),
                ("4", "Shodan Search"),
                ("5", "Censys Search"),
                ("6", "Custom Search Queries"),
                ("0", "Back to Main Menu")
            ]
            
            for option, tool in options:
                table.add_row(option, tool)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                self.google_dorking_guide()
            elif choice == "4":
                if self.config.get('shodan_api'):
                    query = Prompt.ask("Enter Shodan search query")
                    self.shodan_search(query)
                else:
                    self.console.print("[red]Shodan API key not configured[/red]")
                    Prompt.ask("Press Enter to continue")
    
    def crypto_investigation_menu(self):
        """Cryptocurrency investigation menu"""
        try:
            from social_media_osint import CryptoOSINT
            crypto_osint = CryptoOSINT(self)
            
            while True:
                self.console.clear()
                self.console.print(Panel("[bold cyan]Cryptocurrency Investigation[/bold cyan]", style="red"))
                
                table = Table()
                table.add_column("Option", style="cyan")
                table.add_column("Cryptocurrency", style="white")
                
                options = [
                    ("1", "Bitcoin Address Analysis"),
                    ("2", "Ethereum Address Analysis"),
                    ("3", "Blockchain Transaction Tracking"),
                    ("4", "Cryptocurrency Exchange Search"),
                    ("5", "Darknet Market Investigation"),
                    ("0", "Back to Main Menu")
                ]
                
                for option, crypto in options:
                    table.add_row(option, crypto)
                
                self.console.print(table)
                choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
                
                if choice == "0":
                    break
                elif choice == "1":
                    address = Prompt.ask("Enter Bitcoin address")
                    crypto_osint.bitcoin_address_analysis(address)
        except ImportError:
            self.console.print("[red]Crypto module not available[/red]")
            Prompt.ask("Press Enter to continue")
    
    def network_scanning_menu(self):
        """Network scanning menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Network Scanning[/bold cyan]", style="blue"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Scan Type", style="white")
            table.add_column("Description", style="yellow")
            
            options = [
                ("1", "Quick Port Scan", "Fast TCP port scan"),
                ("2", "Comprehensive Scan", "Detailed service detection"),
                ("3", "Vulnerability Scan", "Check for known vulnerabilities"),
                ("4", "OS Detection", "Operating system fingerprinting"),
                ("5", "Service Version Detection", "Detect service versions"),
                ("6", "UDP Scan", "UDP port scanning"),
                ("7", "Stealth Scan", "SYN stealth scanning"),
                ("8", "Network Discovery", "Discover live hosts"),
                ("9", "Script Scan", "NSE script scanning"),
                ("0", "Back to Main Menu", "")
            ]
            
            for option, scan_type, desc in options:
                table.add_row(option, scan_type, desc)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                target = Prompt.ask("Enter target (IP/domain)")
                self.quick_port_scan(target)
            elif choice == "2":
                target = Prompt.ask("Enter target (IP/domain)")
                self.comprehensive_scan(target)
            elif choice == "8":
                network = Prompt.ask("Enter network range (e.g., 192.168.1.0/24)")
                self.network_discovery(network)
    
    def metadata_analysis_menu(self):
        """Metadata analysis menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Metadata Analysis[/bold cyan]", style="white"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("File Type", style="white")
            
            options = [
                ("1", "Image Metadata (EXIF)"),
                ("2", "Document Metadata"),
                ("3", "Audio/Video Metadata"),
                ("4", "PDF Document Analysis"),
                ("5", "Office Document Analysis"),
                ("0", "Back to Main Menu")
            ]
            
            for option, file_type in options:
                table.add_row(option, file_type)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                file_path = Prompt.ask("Enter image file path")
                self.image_metadata_analysis(file_path)
    
    def geolocation_menu(self):
        """Geolocation intelligence menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Geolocation Intelligence[/bold cyan]", style="bright_green"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Location Type", style="white")
            
            options = [
                ("1", "IP Geolocation"),
                ("2", "GPS Coordinate Analysis"),
                ("3", "Address Investigation"),
                ("4", "Timezone Analysis"),
                ("5", "Satellite Imagery"),
                ("0", "Back to Main Menu")
            ]
            
            for option, location_type in options:
                table.add_row(option, location_type)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                ip = Prompt.ask("Enter IP address")
                self.ip_geolocation(ip)
    
    def dark_web_menu(self):
        """Dark web monitoring menu"""
        try:
            from social_media_osint import DarkWebOSINT
            darkweb_osint = DarkWebOSINT(self)
            
            while True:
                self.console.clear()
                self.console.print(Panel("[bold red]Dark Web Monitoring[/bold red]", style="bright_red"))
                
                table = Table()
                table.add_column("Option", style="cyan")
                table.add_column("Tool", style="white")
                
                options = [
                    ("1", "Dark Web Search Guide"),
                    ("2", "Tor Setup Instructions"),
                    ("3", "Onion Link Analysis"),
                    ("4", "Marketplace Monitoring"),
                    ("5", "Leak Site Monitoring"),
                    ("0", "Back to Main Menu")
                ]
                
                for option, tool in options:
                    table.add_row(option, tool)
                
                self.console.print(table)
                choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
                
                if choice == "0":
                    break
                elif choice == "1":
                    darkweb_osint.dark_web_search_guide()
                elif choice == "2":
                    darkweb_osint.tor_setup_guide()
        except ImportError:
            self.console.print("[red]Dark web module not available[/red]")
            Prompt.ask("Press Enter to continue")
    
    def breach_data_menu(self):
        """Breach data search menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Breach Data Search[/bold cyan]", style="bright_yellow"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Search Type", style="white")
            
            options = [
                ("1", "Email in Breaches"),
                ("2", "Username in Breaches"),
                ("3", "Domain in Breaches"),
                ("4", "Password Analysis"),
                ("5", "Breach Database Search"),
                ("0", "Back to Main Menu")
            ]
            
            for option, search_type in options:
                table.add_row(option, search_type)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                email = Prompt.ask("Enter email address")
                self.hibp_email_search(email)
    
    def company_intelligence_menu(self):
        """Company intelligence menu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Company Intelligence[/bold cyan]", style="bright_blue"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Intelligence Type", style="white")
            
            options = [
                ("1", "Company Domain Analysis"),
                ("2", "Employee Information"),
                ("3", "Financial Information"),
                ("4", "News & Media Monitoring"),
                ("5", "Technology Stack Analysis"),
                ("0", "Back to Main Menu")
            ]
            
            for option, intel_type in options:
                table.add_row(option, intel_type)
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]")
            
            if choice == "0":
                break
            elif choice == "1":
                domain = Prompt.ask("Enter company domain")
                self.company_domain_analysis(domain)
    
    def generate_report(self):
        """Generate investigation report"""
        self.console.print(Panel("[bold cyan]Generate Investigation Report[/bold cyan]", style="bright_cyan"))
        
        # List available results
        results_files = list(self.results_dir.glob("*.json"))
        
        if not results_files:
            self.console.print("[yellow]No investigation results found[/yellow]")
            Prompt.ask("Press Enter to continue")
            return
        
        self.console.print(f"[green]Found {len(results_files)} investigation results[/green]")
        
        # Generate HTML report
        report_name = Prompt.ask("Enter report name (without extension)", default="osint_report")
        
        try:
            report_path = self.results_dir / f"{report_name}.html"
            self.create_html_report(results_files, report_path)
            self.console.print(f"[green]Report generated: {report_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error generating report: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def phone_validation(self, phone_number):
        """Validate and analyze phone number"""
        try:
            self.console.print(f"\n[bold green]Phone Number Analysis for {phone_number}[/bold green]")
            
            # Parse phone number
            parsed = phonenumbers.parse(phone_number, None)
            
            # Validation
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)
            
            # Get carrier and location
            carrier_name = carrier.name_for_number(parsed, "en")
            location = geocoder.description_for_number(parsed, "en")
            
            # Format options
            international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            # Create results table
            phone_table = Table(title="Phone Number Information")
            phone_table.add_column("Field", style="cyan")
            phone_table.add_column("Value", style="white")
            
            phone_info = [
                ("Original Number", phone_number),
                ("Is Valid", "✅ Yes" if is_valid else "❌ No"),
                ("Is Possible", "✅ Yes" if is_possible else "❌ No"),
                ("Carrier", carrier_name or "Unknown"),
                ("Location", location or "Unknown"),
                ("Country Code", f"+{parsed.country_code}"),
                ("National Number", str(parsed.national_number)),
                ("International Format", international),
                ("National Format", national),
                ("E164 Format", e164)
            ]
            
            for field, value in phone_info:
                phone_table.add_row(field, value)
            
            self.console.print(phone_table)
            
            # Save results
            self.save_result("phone_analysis", phone_number, {
                "is_valid": is_valid,
                "is_possible": is_possible,
                "carrier": carrier_name,
                "location": location,
                "formats": {
                    "international": international,
                    "national": national,
                    "e164": e164
                }
            })
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def phone_carrier_info(self, phone_number):
        """Get phone carrier information"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            carrier_name = carrier.name_for_number(parsed, "en")
            location = geocoder.description_for_number(parsed, "en")
            
            carrier_table = Table(title="Carrier Information")
            carrier_table.add_column("Field", style="cyan")
            carrier_table.add_column("Value", style="white")
            
            carrier_table.add_row("Phone Number", phone_number)
            carrier_table.add_row("Carrier", carrier_name or "Unknown")
            carrier_table.add_row("Location", location or "Unknown")
            carrier_table.add_row("Country Code", f"+{parsed.country_code}")
            
            self.console.print(carrier_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def phone_geolocation(self, phone_number):
        """Get phone geolocation"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            location = geocoder.description_for_number(parsed, "en")
            
            geo_table = Table(title="Phone Geolocation")
            geo_table.add_column("Field", style="cyan")
            geo_table.add_column("Value", style="white")
            
            geo_table.add_row("Phone Number", phone_number)
            geo_table.add_row("Geographic Location", location or "Unknown")
            geo_table.add_row("Country Code", f"+{parsed.country_code}")
            geo_table.add_row("Type", "Mobile" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "Other")
            
            self.console.print(geo_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def phone_format_analysis(self, phone_number):
        """Analyze phone number formats"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            
            formats = {
                "International": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "National": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "E164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "RFC3966": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
            }
            
            format_table = Table(title="Phone Number Formats")
            format_table.add_column("Format", style="cyan")
            format_table.add_column("Value", style="white")
            
            for format_name, formatted_number in formats.items():
                format_table.add_row(format_name, formatted_number)
            
            self.console.print(format_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def social_phone_search(self, phone_number):
        """Search phone number on social media"""
        try:
            self.console.print(f"\n[bold green]Social Media Search for {phone_number}[/bold green]")
            
            # Clean phone number for searching
            clean_phone = re.sub(r'[^\d+]', '', phone_number)
            
            search_queries = [
                f"\"{phone_number}\"",
                f"\"{clean_phone}\"",
                f"site:facebook.com \"{phone_number}\"",
                f"site:twitter.com \"{phone_number}\"",
                f"site:instagram.com \"{phone_number}\"",
                f"site:linkedin.com \"{phone_number}\""
            ]
            
            search_table = Table(title="Social Media Search Queries")
            search_table.add_column("Platform", style="cyan")
            search_table.add_column("Search Query", style="white")
            
            platforms = ["General", "General Alt", "Facebook", "Twitter", "Instagram", "LinkedIn"]
            for platform, query in zip(platforms, search_queries):
                search_table.add_row(platform, query)
            
            self.console.print(search_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def email_validation(self, email):
        """Validate email address"""
        try:
            self.console.print(f"\n[bold green]Email Validation for {email}[/bold green]")
            
            # Basic regex validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid_format = bool(re.match(email_pattern, email))
            
            # Extract domain
            domain = email.split('@')[1] if '@' in email else None
            
            # MX record check
            mx_valid = False
            if domain:
                try:
                    mx_records = dns.resolver.resolve(domain, 'MX')
                    mx_valid = len(mx_records) > 0
                except:
                    pass
            
            # Create results table
            email_table = Table(title="Email Validation Results")
            email_table.add_column("Check", style="cyan")
            email_table.add_column("Result", style="white")
            email_table.add_column("Status", style="yellow")
            
            checks = [
                ("Format Validation", "Valid" if is_valid_format else "Invalid", 
                 "✅" if is_valid_format else "❌"),
                ("Domain", domain or "N/A", "✅" if domain else "❌"),
                ("MX Records", "Found" if mx_valid else "Not Found", 
                 "✅" if mx_valid else "❌")
            ]
            
            for check, result, status in checks:
                email_table.add_row(check, result, status)
            
            self.console.print(email_table)
            
            # Save results
            self.save_result("email_validation", email, {
                "valid_format": is_valid_format,
                "domain": domain,
                "mx_valid": mx_valid,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def breach_search(self, email):
        """Search email in breach databases"""
        try:
            self.console.print(f"\n[bold green]Breach Search for {email}[/bold green]")
            
            # This would require HaveIBeenPwned API
            breach_info = {
                "email": email,
                "search_date": datetime.now().isoformat(),
                "resources": [
                    "https://haveibeenpwned.com/",
                    "https://www.dehashed.com/",
                    "https://breachdirectory.org/",
                    "https://www.ghostproject.fr/"
                ]
            }
            
            resource_table = Table(title="Breach Search Resources")
            resource_table.add_column("Resource", style="cyan")
            resource_table.add_column("URL", style="white")
            
            resources = [
                ("Have I Been Pwned", "https://haveibeenpwned.com/"),
                ("DeHashed", "https://www.dehashed.com/"),
                ("Breach Directory", "https://breachdirectory.org/"),
                ("Ghost Project", "https://www.ghostproject.fr/")
            ]
            
            for name, url in resources:
                resource_table.add_row(name, url)
            
            self.console.print(resource_table)
            self.console.print(f"\n[yellow]Note: Manual verification required on these platforms[/yellow]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def email_header_analysis(self):
        """Analyze email headers"""
        self.console.print("\n[bold green]Email Header Analysis[/bold green]")
        
        self.console.print("""
[bold yellow]Email Header Analysis Instructions:[/bold yellow]

1. Copy the full email headers from your email client
2. Look for these important fields:
   • Return-Path: Shows the sender's email address
   • Received: Shows the path the email took
   • Message-ID: Unique identifier for the email
   • X-Originating-IP: Original sender's IP address
   • Authentication-Results: SPF, DKIM, DMARC results

3. Online tools for header analysis:
   • https://mxtoolbox.com/EmailHeaders.aspx
   • https://www.whatismyipaddress.com/email-header-analyzer
   • https://mailheader.org/

4. Key indicators of suspicious emails:
   • Mismatched Return-Path and From fields
   • Missing or invalid authentication results
   • Suspicious originating IP addresses
   • Unusual routing paths
        """)
        
        Prompt.ask("\nPress Enter to continue")

    def social_email_search(self, email):
        """Search email on social media"""
        try:
            self.console.print(f"\n[bold green]Social Media Search for {email}[/bold green]")
            
            search_queries = [
                f"\"{email}\"",
                f"site:facebook.com \"{email}\"",
                f"site:twitter.com \"{email}\"",
                f"site:instagram.com \"{email}\"",
                f"site:linkedin.com \"{email}\"",
                f"site:github.com \"{email}\"",
                f"site:reddit.com \"{email}\""
            ]
            
            search_table = Table(title="Email Social Media Search Queries")
            search_table.add_column("Platform", style="cyan")
            search_table.add_column("Search Query", style="white")
            
            platforms = ["General", "Facebook", "Twitter", "Instagram", "LinkedIn", "GitHub", "Reddit"]
            for platform, query in zip(platforms, search_queries):
                search_table.add_row(platform, query)
            
            self.console.print(search_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def email_domain_analysis(self, email):
        """Analyze domain from email"""
        try:
            domain = email.split('@')[1] if '@' in email else None
            if domain:
                self.console.print(f"\n[bold green]Domain Analysis for {domain}[/bold green]")
                self.whois_lookup(domain)
            else:
                self.console.print("[red]Invalid email format[/red]")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")

    def email_pattern_generator(self):
        """Generate email patterns for a company"""
        try:
            company = Prompt.ask("Enter company name")
            domain = Prompt.ask("Enter company domain")
            first_name = Prompt.ask("Enter first name")
            last_name = Prompt.ask("Enter last name")
            
            patterns = [
                f"{first_name.lower()}.{last_name.lower()}@{domain}",
                f"{first_name.lower()}{last_name.lower()}@{domain}",
                f"{first_name[0].lower()}{last_name.lower()}@{domain}",
                f"{first_name.lower()}{last_name[0].lower()}@{domain}",
                f"{first_name[0].lower()}.{last_name.lower()}@{domain}",
                f"{last_name.lower()}.{first_name.lower()}@{domain}",
                f"{last_name.lower()}@{domain}",
                f"{first_name.lower()}@{domain}"
            ]
            
            pattern_table = Table(title=f"Email Patterns for {company}")
            pattern_table.add_column("Pattern", style="cyan")
            pattern_table.add_column("Email", style="white")
            
            for i, pattern in enumerate(patterns, 1):
                pattern_table.add_row(f"Pattern {i}", pattern)
            
            self.console.print(pattern_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def username_search(self, username):
        """Search username across multiple platforms"""
        try:
            self.console.print(f"\n[bold green]Username Search for '{username}'[/bold green]")
            
            # Common social media platforms
            platforms = {
                "GitHub": f"https://github.com/{username}",
                "Twitter": f"https://twitter.com/{username}",
                "Instagram": f"https://instagram.com/{username}",
                "LinkedIn": f"https://linkedin.com/in/{username}",
                "Facebook": f"https://facebook.com/{username}",
                "Reddit": f"https://reddit.com/user/{username}",
                "YouTube": f"https://youtube.com/@{username}",
                "TikTok": f"https://tiktok.com/@{username}",
                "Pinterest": f"https://pinterest.com/{username}",
                "Tumblr": f"https://{username}.tumblr.com",
                "Medium": f"https://medium.com/@{username}",
                "DeviantArt": f"https://{username}.deviantart.com",
                "Behance": f"https://behance.net/{username}",
                "GitLab": f"https://gitlab.com/{username}",
                "Bitbucket": f"https://bitbucket.org/{username}",
                "Dribbble": f"https://dribbble.com/{username}",
                "Twitch": f"https://twitch.tv/{username}",
                "Steam": f"https://steamcommunity.com/id/{username}",
                "Spotify": f"https://open.spotify.com/user/{username}",
                "SoundCloud": f"https://soundcloud.com/{username}"
            }
            
            results = []
            
            with self.console.status("[bold green]Checking platforms..."):
                for platform, url in platforms.items():
                    try:
                        response = requests.get(url, timeout=5, allow_redirects=True)
                        if response.status_code == 200:
                            # Simple heuristic to check if profile exists
                            if not any(phrase in response.text.lower() for phrase in 
                                     ['user not found', 'page not found', 'profile not found', 
                                      'account suspended', 'user does not exist']):
                                results.append({
                                    "platform": platform,
                                    "url": url,
                                    "status": "Found",
                                    "status_code": response.status_code
                                })
                            else:
                                results.append({
                                    "platform": platform,
                                    "url": url,
                                    "status": "Not Found",
                                    "status_code": response.status_code
                                })
                        else:
                            results.append({
                                "platform": platform,
                                "url": url,
                                "status": "Not Found",
                                "status_code": response.status_code
                            })
                    except:
                        results.append({
                            "platform": platform,
                            "url": url,
                            "status": "Error",
                            "status_code": "N/A"
                        })
                    
                    time.sleep(0.1)  # Rate limiting
            
            # Display results
            results_table = Table(title=f"Username Search Results for '{username}'")
            results_table.add_column("Platform", style="cyan")
            results_table.add_column("URL", style="white")
            results_table.add_column("Status", style="yellow")
            
            found_count = 0
            for result in results:
                status_style = "green" if result["status"] == "Found" else "red"
                if result["status"] == "Found":
                    found_count += 1
                results_table.add_row(
                    result["platform"], 
                    result["url"], 
                    f"[{status_style}]{result['status']}[/{status_style}]"
                )
            
            self.console.print(results_table)
            self.console.print(f"\n[bold green]Found {found_count} potential matches out of {len(platforms)} platforms[/bold green]")
            
            # Save results
            self.save_result("username_search", username, {
                "platforms_checked": len(platforms),
                "matches_found": found_count,
                "results": results
            })
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def website_tech_stack(self, url):
        """Analyze website technology stack"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.console.print(f"\n[bold green]Technology Stack Analysis for {url}[/bold green]")
            
            with self.console.status("[bold green]Analyzing website..."):
                response = requests.get(url, timeout=10)
                headers = response.headers
                content = response.text
            
            # Analyze headers
            tech_info = {
                "Server": headers.get('Server', 'Unknown'),
                "X-Powered-By": headers.get('X-Powered-By', 'Not specified'),
                "Content-Type": headers.get('Content-Type', 'Unknown'),
                "X-Generator": headers.get('X-Generator', 'Not specified'),
                "X-Frame-Options": headers.get('X-Frame-Options', 'Not set'),
                "X-Content-Type-Options": headers.get('X-Content-Type-Options', 'Not set'),
                "Strict-Transport-Security": headers.get('Strict-Transport-Security', 'Not set')
            }
            
            # Analyze content for technologies
            technologies = []
            
            # Check for common frameworks and libraries
            tech_patterns = {
                "WordPress": [r'wp-content', r'wp-includes', r'/wp-json/'],
                "Drupal": [r'Drupal\.settings', r'sites/default/files'],
                "Joomla": [r'/components/com_', r'Joomla!'],
                "React": [r'react', r'__REACT_DEVTOOLS_GLOBAL_HOOK__'],
                "Angular": [r'ng-version', r'angular'],
                "Vue.js": [r'vue\.js', r'__vue__'],
                "jQuery": [r'jquery', r'\$\(document\)\.ready'],
                "Bootstrap": [r'bootstrap', r'btn btn-'],
                "Laravel": [r'laravel_session', r'csrf-token'],
                "Django": [r'csrfmiddlewaretoken', r'__admin_media_prefix__'],
                "Ruby on Rails": [r'csrf-param', r'authenticity_token'],
                "Express.js": [r'express'],
                "ASP.NET": [r'__VIEWSTATE', r'asp\.net'],
                "PHP": [r'PHPSESSID', r'\.php'],
                "Node.js": [r'node\.js', r'nodejs']
            }
            
            for tech, patterns in tech_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        technologies.append(tech)
                        break
            
            # Create results table
            tech_table = Table(title="Technology Stack Information")
            tech_table.add_column("Component", style="cyan")
            tech_table.add_column("Value", style="white")
            
            for component, value in tech_info.items():
                tech_table.add_row(component, value)
            
            self.console.print(tech_table)
            
            if technologies:
                self.console.print(f"\n[bold yellow]Detected Technologies:[/bold yellow]")
                for tech in set(technologies):
                    self.console.print(f"• {tech}")
            
            # Save results
            self.save_result("website_tech", url, {
                "headers": dict(headers),
                "detected_technologies": list(set(technologies)),
                "tech_info": tech_info
            })
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def robots_analysis(self, url):
        """Analyze robots.txt file"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            robots_url = urljoin(url, '/robots.txt')
            
            self.console.print(f"\n[bold green]Robots.txt Analysis for {robots_url}[/bold green]")
            
            response = requests.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                self.console.print(f"\n[bold cyan]Robots.txt Content:[/bold cyan]")
                self.console.print(response.text)
                
                # Analyze for interesting directories
                disallowed = re.findall(r'Disallow:\s*(.+)', response.text)
                if disallowed:
                    self.console.print(f"\n[bold yellow]Disallowed Paths:[/bold yellow]")
                    for path in disallowed:
                        self.console.print(f"• {path.strip()}")
                
            else:
                self.console.print(f"[red]Robots.txt not found (Status: {response.status_code})[/red]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def sitemap_discovery(self, url):
        """Discover website sitemaps"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.console.print(f"\n[bold green]Sitemap Discovery for {url}[/bold green]")
            
            sitemap_urls = [
                '/sitemap.xml',
                '/sitemap_index.xml',
                '/sitemap.txt',
                '/sitemap/',
                '/sitemaps.xml'
            ]
            
            found_sitemaps = []
            
            for sitemap_path in sitemap_urls:
                sitemap_url = urljoin(url, sitemap_path)
                try:
                    response = requests.get(sitemap_url, timeout=5)
                    if response.status_code == 200:
                        found_sitemaps.append(sitemap_url)
                except:
                    pass
            
            if found_sitemaps:
                sitemap_table = Table(title="Found Sitemaps")
                sitemap_table.add_column("Sitemap URL", style="green")
                
                for sitemap in found_sitemaps:
                    sitemap_table.add_row(sitemap)
                
                self.console.print(sitemap_table)
            else:
                self.console.print("[yellow]No sitemaps found[/yellow]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def http_headers_analysis(self, url):
        """Analyze HTTP headers"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.console.print(f"\n[bold green]HTTP Headers Analysis for {url}[/bold green]")
            
            response = requests.get(url, timeout=10)
            
            headers_table = Table(title="HTTP Response Headers")
            headers_table.add_column("Header", style="cyan")
            headers_table.add_column("Value", style="white")
            
            for header, value in response.headers.items():
                headers_table.add_row(header, value)
            
            self.console.print(headers_table)
            
            # Security headers analysis
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Sniffing Protection',
                'X-XSS-Protection': 'XSS Protection',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer Policy'
            }
            
            security_table = Table(title="Security Headers Analysis")
            security_table.add_column("Security Header", style="cyan")
            security_table.add_column("Status", style="white")
            security_table.add_column("Value", style="yellow")
            
            for header, description in security_headers.items():
                value = response.headers.get(header, 'Not Set')
                status = "✅ Set" if value != 'Not Set' else "❌ Missing"
                security_table.add_row(description, status, value[:50] + "..." if len(value) > 50 else value)
            
            self.console.print(security_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def wayback_analysis(self, url):
        """Analyze website history using Wayback Machine"""
        try:
            self.console.print(f"\n[bold green]Wayback Machine Analysis for {url}[/bold green]")
            
            wayback_url = f"https://web.archive.org/web/{url}"
            api_url = f"https://archive.org/wayback/available?url={url}"
            
            try:
                response = requests.get(api_url, timeout=10)
                data = response.json()
                
                if data.get('archived_snapshots', {}).get('closest'):
                    snapshot = data['archived_snapshots']['closest']
                    
                    wayback_table = Table(title="Wayback Machine Information")
                    wayback_table.add_column("Field", style="cyan")
                    wayback_table.add_column("Value", style="white")
                    
                    wayback_table.add_row("URL", snapshot.get('url', 'N/A'))
                    wayback_table.add_row("Timestamp", snapshot.get('timestamp', 'N/A'))
                    wayback_table.add_row("Status", snapshot.get('status', 'N/A'))
                    wayback_table.add_row("Available", "Yes" if snapshot.get('available') else "No")
                    
                    self.console.print(wayback_table)
                    self.console.print(f"\n[bold yellow]Wayback Machine URL:[/bold yellow] {wayback_url}")
                else:
                    self.console.print("[yellow]No archived snapshots found[/yellow]")
                    
            except Exception as e:
                self.console.print(f"[red]Error checking Wayback Machine: {e}[/red]")
                self.console.print(f"[yellow]Manual check: {wayback_url}[/yellow]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def security_headers_check(self, url):
        """Check website security headers"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.console.print(f"\n[bold green]Security Headers Check for {url}[/bold green]")
            
            response = requests.get(url, timeout=10)
            
            security_checks = {
                'Strict-Transport-Security': {
                    'description': 'HTTP Strict Transport Security',
                    'recommendation': 'Should be present for HTTPS sites'
                },
                'X-Frame-Options': {
                    'description': 'Clickjacking Protection',
                    'recommendation': 'Should be DENY or SAMEORIGIN'
                },
                'X-Content-Type-Options': {
                    'description': 'MIME Sniffing Protection',
                    'recommendation': 'Should be nosniff'
                },
                'X-XSS-Protection': {
                    'description': 'XSS Protection',
                    'recommendation': 'Should be 1; mode=block'
                },
                'Content-Security-Policy': {
                    'description': 'Content Security Policy',
                    'recommendation': 'Should be present with strict policy'
                },
                'Referrer-Policy': {
                    'description': 'Referrer Policy',
                    'recommendation': 'Should control referrer information'
                }
            }
            
            security_table = Table(title="Security Headers Assessment")
            security_table.add_column("Header", style="cyan")
            security_table.add_column("Status", style="white")
            security_table.add_column("Value", style="yellow")
            security_table.add_column("Assessment", style="magenta")
            
            for header, info in security_checks.items():
                value = response.headers.get(header, 'Not Set')
                
                if value == 'Not Set':
                    status = "❌ Missing"
                    assessment = "Needs Improvement"
                else:
                    status = "✅ Present"
                    assessment = "Good"
                
                security_table.add_row(
                    info['description'],
                    status,
                    value[:30] + "..." if len(value) > 30 else value,
                    assessment
                )
            
            self.console.print(security_table)
            
            # Overall security score
            present_headers = sum(1 for header in security_checks.keys() if response.headers.get(header))
            total_headers = len(security_checks)
            score = (present_headers / total_headers) * 100
            
            score_color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
            self.console.print(f"\n[bold {score_color}]Security Score: {score:.1f}% ({present_headers}/{total_headers} headers present)[/bold {score_color}]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def google_dorking_guide(self):
        """Display Google dorking guide"""
        self.console.print("\n[bold green]Google Dorking Guide[/bold green]")
        
        dorking_table = Table(title="Google Search Operators")
        dorking_table.add_column("Operator", style="cyan")
        dorking_table.add_column("Description", style="white")
        dorking_table.add_column("Example", style="yellow")
        
        operators = [
            ("site:", "Search within specific site", "site:example.com"),
            ("filetype:", "Search for specific file types", "filetype:pdf"),
            ("intitle:", "Search in page title", "intitle:\"index of\""),
            ("inurl:", "Search in URL", "inurl:admin"),
            ("intext:", "Search in page text", "intext:password"),
            ("cache:", "View cached version", "cache:example.com"),
            ("related:", "Find related sites", "related:example.com"),
            ("link:", "Find pages linking to site", "link:example.com"),
            ("\"\"", "Exact phrase search", "\"error message\""),
            ("-", "Exclude term", "cats -dogs"),
            ("*", "Wildcard", "how to * python"),
            ("..", "Number range", "camera $50..$100"),
            ("|", "OR operator", "cats | dogs"),
            ("()", "Group terms", "(cats | dogs) food")
        ]
        
        for operator, description, example in operators:
            dorking_table.add_row(operator, description, example)
        
        self.console.print(dorking_table)
        
        # Common dorks
        self.console.print("\n[bold yellow]Common OSINT Dorks:[/bold yellow]")
        common_dorks = [
            'site:pastebin.com "password"',
            'filetype:sql "password"',
            'intitle:"index of" "config.php"',
            'site:github.com "api_key"',
            'filetype:log "error"',
            'inurl:admin site:target.com',
            'site:linkedin.com "works at CompanyName"',
            'site:twitter.com "email" "@gmail.com"'
        ]
        
        for dork in common_dorks:
            self.console.print(f"• {dork}")
        
        Prompt.ask("\nPress Enter to continue")

    def shodan_search(self, query):
        """Search using Shodan"""
        try:
            if not self.config.get('shodan_api'):
                self.console.print("[red]Shodan API key not configured[/red]")
                return
            
            api = shodan.Shodan(self.config['shodan_api'])
            
            self.console.print(f"\n[bold green]Shodan Search: {query}[/bold green]")
            
            with self.console.status("[bold green]Searching Shodan..."):
                results = api.search(query)
            
            shodan_table = Table(title="Shodan Search Results")
            shodan_table.add_column("IP", style="cyan")
            shodan_table.add_column("Port", style="white")
            shodan_table.add_column("Organization", style="yellow")
            shodan_table.add_column("Location", style="magenta")
            
            for result in results['matches'][:10]:  # Limit to first 10 results
                ip = result.get('ip_str', 'N/A')
                port = str(result.get('port', 'N/A'))
                org = result.get('org', 'N/A')
                location = f"{result.get('location', {}).get('city', 'N/A')}, {result.get('location', {}).get('country_name', 'N/A')}"
                
                shodan_table.add_row(ip, port, org, location)
            
            self.console.print(shodan_table)
            self.console.print(f"\n[bold green]Total results: {results['total']} (showing first 10)[/bold green]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def quick_port_scan(self, target):
        """Perform quick port scan"""
        try:
            self.console.print(f"\n[bold green]Quick Port Scan for {target}[/bold green]")
            
            # Common ports to scan
            common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443]
            
            nm = nmap.PortScanner()
            
            with self.console.status("[bold green]Scanning ports..."):
                # Scan common ports
                nm.scan(target, ','.join(map(str, common_ports)), '-T4')
            
            # Process results
            scan_results = []
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port].get('name', 'unknown')
                        version = nm[host][proto][port].get('version', '')
                        
                        scan_results.append({
                            "port": port,
                            "protocol": proto,
                            "state": state,
                            "service": service,
                            "version": version
                        })
            
            if scan_results:
                # Create results table
                ports_table = Table(title=f"Open Ports on {target}")
                ports_table.add_column("Port", style="cyan")
                ports_table.add_column("Protocol", style="yellow")
                ports_table.add_column("State", style="green")
                ports_table.add_column("Service", style="white")
                ports_table.add_column("Version", style="magenta")
                
                for result in scan_results:
                    if result['state'] == 'open':
                        ports_table.add_row(
                            str(result['port']),
                            result['protocol'],
                            result['state'],
                            result['service'],
                            result['version']
                        )
                
                self.console.print(ports_table)
                
                # Save results
                self.save_result("port_scan", target, {
                    "scan_type": "quick",
                    "ports_scanned": common_ports,
                    "results": scan_results
                })
            else:
                self.console.print("[yellow]No open ports found in common port range[/yellow]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def comprehensive_scan(self, target):
        """Perform comprehensive scan"""
        try:
            self.console.print(f"\n[bold green]Comprehensive Scan for {target}[/bold green]")
            
            nm = nmap.PortScanner()
            
            with self.console.status("[bold green]Performing comprehensive scan..."):
                # Comprehensive scan with service detection
                nm.scan(target, arguments='-T4 -A -v')
            
            for host in nm.all_hosts():
                self.console.print(f"\n[bold cyan]Host: {host} ({nm[host].hostname()})[/bold cyan]")
                self.console.print(f"State: {nm[host].state()}")
                
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    
                    if ports:
                        ports_table = Table(title=f"{proto.upper()} Ports")
                        ports_table.add_column("Port", style="cyan")
                        ports_table.add_column("State", style="green")
                        ports_table.add_column("Service", style="white")
                        ports_table.add_column("Version", style="magenta")
                        
                        for port in ports:
                            state = nm[host][proto][port]['state']
                            service = nm[host][proto][port].get('name', 'unknown')
                            version = nm[host][proto][port].get('version', '')
                            
                            ports_table.add_row(str(port), state, service, version)
                        
                        self.console.print(ports_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def network_discovery(self, network):
        """Discover live hosts in network"""
        try:
            self.console.print(f"\n[bold green]Network Discovery for {network}[/bold green]")
            
            nm = nmap.PortScanner()
            
            with self.console.status("[bold green]Discovering hosts..."):
                nm.scan(hosts=network, arguments='-sn')
            
            hosts_table = Table(title="Live Hosts")
            hosts_table.add_column("IP Address", style="cyan")
            hosts_table.add_column("Hostname", style="white")
            hosts_table.add_column("Status", style="green")
            
            for host in nm.all_hosts():
                hostname = nm[host].hostname() or 'Unknown'
                status = nm[host].state()
                hosts_table.add_row(host, hostname, status)
            
            self.console.print(hosts_table)
            self.console.print(f"\n[bold green]Found {len(nm.all_hosts())} live hosts[/bold green]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def ip_geolocation(self, ip):
        """Get IP geolocation"""
        try:
            self.console.print(f"\n[bold green]IP Geolocation for {ip}[/bold green]")
            
            # Free IP geolocation API
            api_url = f"http://ip-api.com/json/{ip}"
            
            response = requests.get(api_url, timeout=10)
            data = response.json()
            
            if data['status'] == 'success':
                geo_table = Table(title="IP Geolocation Information")
                geo_table.add_column("Field", style="cyan")
                geo_table.add_column("Value", style="white")
                
                fields = [
                    ("IP Address", data.get('query', 'N/A')),
                    ("Country", data.get('country', 'N/A')),
                    ("Region", data.get('regionName', 'N/A')),
                    ("City", data.get('city', 'N/A')),
                    ("ZIP Code", data.get('zip', 'N/A')),
                    ("Latitude", str(data.get('lat', 'N/A'))),
                    ("Longitude", str(data.get('lon', 'N/A'))),
                    ("Timezone", data.get('timezone', 'N/A')),
                    ("ISP", data.get('isp', 'N/A')),
                    ("Organization", data.get('org', 'N/A')),
                    ("AS Number", data.get('as', 'N/A'))
                ]
                
                for field, value in fields:
                    geo_table.add_row(field, value)
                
                self.console.print(geo_table)
                
                # Save results
                self.save_result("ip_geolocation", ip, data)
            else:
                self.console.print("[red]Could not retrieve geolocation data[/red]")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def image_metadata_analysis(self, file_path):
        """Analyze image metadata"""
        try:
            self.console.print(f"\n[bold green]Image Metadata Analysis for {file_path}[/bold green]")
            
            if not os.path.exists(file_path):
                self.console.print("[red]File not found[/red]")
                return
            
            # This would require PIL/Pillow and exifread libraries
            self.console.print("""
[bold yellow]Image Metadata Analysis Instructions:[/bold yellow]

To analyze image metadata, you can use:

1. ExifTool (recommended):
   • Install: apt install exiftool
   • Usage: exiftool image.jpg

2. Online tools:
   • http://exif.regex.info/exif.cgi
   • https://www.metadata2go.com/

3. Python libraries:
   • pip install pillow exifread
   • Extract GPS coordinates, camera info, timestamps

Key metadata to look for:
• GPS coordinates (lat/long)
• Camera make and model
• Timestamp information
• Software used
• Copyright information
            """)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def hibp_email_search(self, email):
        """Search email in Have I Been Pwned"""
        try:
            self.console.print(f"\n[bold green]Have I Been Pwned Search for {email}[/bold green]")
            
            if self.config.get('hibp_api'):
                # Use API if available
                headers = {
                    'hibp-api-key': self.config['hibp_api'],
                    'user-agent': 'KaliOSINT'
                }
                
                api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
                
                try:
                    response = requests.get(api_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        breaches = response.json()
                        
                        breach_table = Table(title="Found Breaches")
                        breach_table.add_column("Breach", style="cyan")
                        breach_table.add_column("Date", style="white")
                        breach_table.add_column("Data Classes", style="yellow")
                        
                        for breach in breaches:
                            name = breach.get('Name', 'Unknown')
                            date = breach.get('BreachDate', 'Unknown')
                            data_classes = ', '.join(breach.get('DataClasses', []))
                            
                            breach_table.add_row(name, date, data_classes[:50] + "..." if len(data_classes) > 50 else data_classes)
                        
                        self.console.print(breach_table)
                        self.console.print(f"[bold red]Found in {len(breaches)} breaches[/bold red]")
                        
                    elif response.status_code == 404:
                        self.console.print("[green]Email not found in any breaches[/green]")
                    else:
                        self.console.print(f"[red]Error: {response.status_code}[/red]")
                        
                except Exception as e:
                    self.console.print(f"[red]API Error: {e}[/red]")
            else:
                self.console.print("[yellow]HIBP API key not configured. Manual check required:[/yellow]")
                self.console.print(f"https://haveibeenpwned.com/account/{email}")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def company_domain_analysis(self, domain):
        """Analyze company domain"""
        try:
            self.console.print(f"\n[bold green]Company Domain Analysis for {domain}[/bold green]")
            
            # Perform multiple analysis types
            self.whois_lookup(domain)
            self.dns_analysis(domain)
            self.subdomain_enum(domain)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")

    def ssl_analysis(self, domain):
        """Analyze SSL certificate"""
        try:
            self.console.print(f"\n[bold green]SSL Certificate Analysis for {domain}[/bold green]")
            
            context = ssl.create_default_context()
            
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            ssl_table = Table(title="SSL Certificate Information")
            ssl_table.add_column("Field", style="cyan")
            ssl_table.add_column("Value", style="white")
            
            ssl_info = [
                ("Subject", dict(x[0] for x in cert['subject'])['commonName']),
                ("Issuer", dict(x[0] for x in cert['issuer'])['commonName']),
                ("Version", str(cert.get('version', 'N/A'))),
                ("Serial Number", str(cert.get('serialNumber', 'N/A'))),
                ("Not Before", cert.get('notBefore', 'N/A')),
                ("Not After", cert.get('notAfter', 'N/A')),
                ("Signature Algorithm", cert.get('signatureAlgorithm', 'N/A'))
            ]
            
            for field, value in ssl_info:
                ssl_table.add_row(field, value)
            
            self.console.print(ssl_table)
            
            # Subject Alternative Names
            if 'subjectAltName' in cert:
                self.console.print(f"\n[bold yellow]Subject Alternative Names:[/bold yellow]")
                for san in cert['subjectAltName']:
                    self.console.print(f"• {san[1]}")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def reverse_ip_lookup(self, ip):
        """Perform reverse IP lookup"""
        try:
            self.console.print(f"\n[bold green]Reverse IP Lookup for {ip}[/bold green]")
            
            # Reverse DNS lookup
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                self.console.print(f"[bold cyan]Hostname:[/bold cyan] {hostname}")
            except:
                self.console.print("[yellow]No reverse DNS record found[/yellow]")
            
            # Additional reverse IP tools
            self.console.print(f"\n[bold yellow]Online Reverse IP Tools:[/bold yellow]")
            tools = [
                f"https://www.yougetsignal.com/tools/web-sites-on-web-server/?remoteAddress={ip}",
                f"https://domains.yougetsignal.com/domains.php?remoteAddress={ip}",
                f"https://www.robtex.com/ip-lookup/{ip}",
                f"https://viewdns.info/reverseip/?host={ip}"
            ]
            
            for tool in tools:
                self.console.print(f"• {tool}")
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def domain_history(self, domain):
        """Analyze domain history"""
        try:
            self.console.print(f"\n[bold green]Domain History for {domain}[/bold green]")
            
            # Historical analysis resources
            resources = [
                f"https://web.archive.org/web/*/{domain}",
                f"https://who.is/whois-history/{domain}",
                f"https://www.domaintools.com/research/whois-history/search/?q={domain}",
                f"https://viewdns.info/dnshistory/?domain={domain}"
            ]
            
            history_table = Table(title="Domain History Resources")
            history_table.add_column("Resource", style="cyan")
            history_table.add_column("URL", style="white")
            
            resource_names = [
                "Wayback Machine",
                "Who.is History",
                "DomainTools",
                "ViewDNS History"
            ]
            
            for name, url in zip(resource_names, resources):
                history_table.add_row(name, url)
            
            self.console.print(history_table)
            
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to continue")

    def create_html_report(self, results_files, report_path):
        """Create HTML investigation report"""
        try:
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>KaliOSINT Investigation Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }
        .result { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .timestamp { color: #7f8c8d; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 KaliOSINT Investigation Report</h1>
        <p>Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
"""
            
            # Process each result file
            for result_file in results_files:
                try:
                    with open(result_file, 'r') as f:
                        result_data = json.load(f)
                    
                    html_content += f"""
    <div class="section">
        <h2>{result_data.get('investigation_type', 'Unknown').replace('_', ' ').title()}</h2>
        <div class="result">
            <h3>Target: {result_data.get('target', 'N/A')}</h3>
            <p class="timestamp">Timestamp: {result_data.get('timestamp', 'N/A')}</p>
            <pre>{json.dumps(result_data.get('data', {}), indent=2)}</pre>
        </div>
    </div>
"""
                except Exception as e:
                    continue
            
            html_content += """
</body>
</html>
"""
            
            with open(report_path, 'w') as f:
                f.write(html_content)
            
        except Exception as e:
            raise Exception(f"Failed to create HTML report: {e}")

# Add placeholder methods for remaining functionality
def main():
    """Main function"""
    try:
        osint_tool = KaliOSINT()
        osint_tool.main_menu()
    except KeyboardInterrupt:
        print("\n\n[bold red]Program interrupted by user. Goodbye! 👋[/bold red]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[bold red]Fatal error: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
