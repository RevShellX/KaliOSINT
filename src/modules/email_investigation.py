#!/usr/bin/env python3
"""
Email Investigation Module for KaliOSINT
Provides email validation, breach data search, and related functionalities
"""

import requests
import json
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Prompt, Confirm


class EmailInvestigation:
    def __init__(self, console=None, config=None, save_result=None):
        self.console = console or Console()
        self.config = config or {}
        self.save_result = save_result or self._default_save_result
    
    def _default_save_result(self, title, content):
        """Default save result function if none provided"""
        print(f"[SAVE] {title}: {content}")
    
    def email_investigation_menu(self):
        """Email investigation submenu"""
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
                ("6", "Email Reputation Check"),
                ("0", "Back to Main Menu")
            ]
            
            for opt, tool in options:
                table.add_row(opt, tool)
            
            self.console.print(table)
            choice = Prompt.ask("Choose an option", choices=[opt for opt, _ in options])
            
            if choice == "0":
                break
            elif choice == "1":
                email = Prompt.ask("Enter email address")
                self.email_validation(email)
            elif choice == "2":
                email = Prompt.ask("Enter email address")
                self.breach_data_search(email)
            elif choice == "3":
                self.console.print("[yellow]Email header analysis requires manual input of headers[/yellow]")
                self.email_header_analysis()
            elif choice == "4":
                email = Prompt.ask("Enter email address")
                self.social_media_by_email(email)
            elif choice == "5":
                email = Prompt.ask("Enter email address")
                self.domain_from_email_analysis(email)
            elif choice == "6":
                email = Prompt.ask("Enter email address")
                self.email_reputation_check(email)
            
            if choice != "0":
                Prompt.ask("Press Enter to continue...")
    
    def email_validation(self, email):
        """Validate email address format and domain"""
        self.console.print(f"[bold green]Validating email: {email}[/bold green]")
        
        # Basic format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.console.print("[red]❌ Invalid email format[/red]")
            return
        
        domain = email.split('@')[1]
        results = {
            "email": email,
            "domain": domain,
            "format_valid": True,
            "domain_exists": False,
            "mx_records": [],
            "disposable": False
        }
        
        try:
            # Check if domain exists
            import socket
            socket.gethostbyname(domain)
            results["domain_exists"] = True
            self.console.print(f"✅ Domain {domain} exists")
            
            # Check MX records
            try:
                import dns.resolver
                mx_records = dns.resolver.resolve(domain, 'MX')
                results["mx_records"] = [str(mx) for mx in mx_records]
                self.console.print(f"✅ MX records found: {len(results['mx_records'])}")
            except ImportError:
                self.console.print("[yellow]⚠️ dnspython not installed, skipping MX record check[/yellow]")
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Could not check MX records: {e}[/yellow]")
            
            # Check if disposable email
            disposable_domains = [
                "10minutemail.com", "guerrillamail.com", "mailinator.com",
                "tempmail.org", "yopmail.com", "throwaway.email"
            ]
            if domain in disposable_domains:
                results["disposable"] = True
                self.console.print("[yellow]⚠️ Disposable email domain detected[/yellow]")
            
        except socket.gaierror:
            self.console.print(f"[red]❌ Domain {domain} does not exist[/red]")
        
        self.save_result(f"Email Validation - {email}", results)
        return results
    
    def breach_data_search(self, email):
        """Search for email in known data breaches"""
        self.console.print(f"[bold green]Searching breaches for: {email}[/bold green]")
        
        results = {
            "email": email,
            "breaches_found": [],
            "total_breaches": 0,
            "search_date": datetime.now().isoformat()
        }
        
        # Note: Using HaveIBeenPwned API requires API key
        api_key = self.config.get("haveibeenpwned_api_key")
        
        if not api_key:
            self.console.print("[yellow]⚠️ HaveIBeenPwned API key not configured[/yellow]")
            self.console.print("[blue]ℹ️ Add your API key to config/api_keys.json[/blue]")
            return results
        
        try:
            headers = {
                "hibp-api-key": api_key,
                "User-Agent": "KaliOSINT-Tool"
            }
            
            response = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                breaches = response.json()
                results["breaches_found"] = breaches
                results["total_breaches"] = len(breaches)
                
                self.console.print(f"[red]Found {len(breaches)} breaches![/red]")
                
                for breach in breaches:
                    self.console.print(f"  • {breach.get('Name', 'Unknown')} - {breach.get('BreachDate', 'Unknown date')}")
                
            elif response.status_code == 404:
                self.console.print("[green]✅ No breaches found[/green]")
            else:
                self.console.print(f"[red]Error: {response.status_code}[/red]")
                
        except requests.RequestException as e:
            self.console.print(f"[red]Network error: {e}[/red]")
        
        self.save_result(f"Breach Search - {email}", results)
        return results
    
    def email_header_analysis(self):
        """Analyze email headers for metadata"""
        self.console.print("[bold green]Email Header Analysis[/bold green]")
        self.console.print("Paste email headers (end with empty line):")
        
        headers = []
        while True:
            line = input()
            if not line.strip():
                break
            headers.append(line)
        
        if not headers:
            self.console.print("[red]No headers provided[/red]")
            return
        
        header_text = "\n".join(headers)
        results = {
            "analysis_date": datetime.now().isoformat(),
            "ip_addresses": [],
            "servers": [],
            "path": [],
            "suspicious_indicators": []
        }
        
        # Extract IP addresses
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, header_text)
        results["ip_addresses"] = list(set(ips))
        
        # Extract server information
        received_lines = [line for line in headers if line.startswith("Received:")]
        results["path"] = received_lines
        
        # Check for suspicious indicators
        suspicious_patterns = [
            (r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', "Direct IP usage"),
            (r'localhost', "Localhost reference"),
            (r'127\.0\.0\.1', "Loopback address")
        ]
        
        for pattern, description in suspicious_patterns:
            if re.search(pattern, header_text):
                results["suspicious_indicators"].append(description)
        
        self.console.print(f"Found {len(results['ip_addresses'])} IP addresses")
        self.console.print(f"Email path: {len(results['path'])} hops")
        
        if results["suspicious_indicators"]:
            self.console.print(f"[yellow]Suspicious indicators: {results['suspicious_indicators']}[/yellow]")
        
        self.save_result("Email Header Analysis", results)
        return results
    
    def social_media_by_email(self, email):
        """Search for social media accounts associated with email"""
        self.console.print(f"[bold green]Searching social media for: {email}[/bold green]")
        
        results = {
            "email": email,
            "platforms_checked": [],
            "accounts_found": [],
            "search_date": datetime.now().isoformat()
        }
        
        # Common platforms that might reveal email associations
        platforms = [
            ("GitHub", f"https://github.com/{email.split('@')[0]}"),
            ("GitLab", f"https://gitlab.com/{email.split('@')[0]}"),
            ("Reddit", f"https://reddit.com/user/{email.split('@')[0]}"),
        ]
        
        for platform, url in track(platforms, description="Checking platforms..."):
            results["platforms_checked"].append(platform)
            
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    results["accounts_found"].append({
                        "platform": platform,
                        "url": url,
                        "status": "exists"
                    })
                    self.console.print(f"✅ Found potential account on {platform}")
                
            except requests.RequestException:
                pass
        
        self.console.print(f"Checked {len(platforms)} platforms")
        self.console.print(f"Found {len(results['accounts_found'])} potential accounts")
        
        self.save_result(f"Social Media Search - {email}", results)
        return results
    
    def domain_from_email_analysis(self, email):
        """Analyze the domain from email address"""
        domain = email.split('@')[1]
        self.console.print(f"[bold green]Analyzing domain: {domain}[/bold green]")
        
        results = {
            "domain": domain,
            "email": email,
            "whois_info": {},
            "dns_records": {},
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            # Basic domain information
            import socket
            ip = socket.gethostbyname(domain)
            results["ip_address"] = ip
            self.console.print(f"IP Address: {ip}")
            
            # Try to get basic web info
            try:
                response = requests.get(f"http://{domain}", timeout=5)
                results["web_status"] = response.status_code
                results["web_headers"] = dict(response.headers)
                
                if response.status_code == 200:
                    self.console.print("✅ Domain has active website")
                
            except requests.RequestException:
                results["web_status"] = "unreachable"
                self.console.print("❌ Domain website unreachable")
            
        except socket.gaierror:
            self.console.print(f"[red]❌ Could not resolve domain {domain}[/red]")
        
        self.save_result(f"Domain Analysis - {domain}", results)
        return results
    
    def email_reputation_check(self, email):
        """Check email reputation across various services"""
        self.console.print(f"[bold green]Checking reputation for: {email}[/bold green]")
        
        results = {
            "email": email,
            "reputation_scores": {},
            "blacklist_status": {},
            "check_date": datetime.now().isoformat()
        }
        
        domain = email.split('@')[1]
        
        # Check against common blacklists (simplified)
        blacklists = [
            "spamhaus.org",
            "barracuda.com",
            "invaluement.com"
        ]
        
        for blacklist in blacklists:
            # This is a simplified check - real implementation would use proper APIs
            results["blacklist_status"][blacklist] = "not_checked"
        
        self.console.print("[blue]ℹ️ Reputation checking requires API integrations[/blue]")
        self.console.print("[blue]ℹ️ Configure API keys for comprehensive checks[/blue]")
        
        self.save_result(f"Email Reputation - {email}", results)
        return results
