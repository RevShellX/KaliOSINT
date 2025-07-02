#!/usr/bin/env python3
"""
Extended OSINT functionalities for KaliOSINT
Social Media Intelligence, Web Analysis, and more
"""

import requests
import json
import time
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import nmap
import ssl
import socket
from datetime import datetime
import subprocess
import os

# Rich imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.prompt import Prompt, Confirm

class ExtendedOSINT:
    def __init__(self, parent):
        self.parent = parent
        self.console = parent.console
        self.config = parent.config
        self.save_result = parent.save_result
    
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
        """Social media intelligence menu"""
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
                ("9", "Discord Investigation", "Discord user analysis"),
                ("10", "Telegram Analysis", "Telegram channel/user analysis"),
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
                self.twitter_analysis(username)
            elif choice == "3":
                username = Prompt.ask("Enter Instagram username")
                self.instagram_analysis(username)
            # Add more social media analysis methods...
    
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
            elif choice == "3":
                target = Prompt.ask("Enter target (IP/domain)")
                self.vulnerability_scan(target)
            elif choice == "8":
                network = Prompt.ask("Enter network range (e.g., 192.168.1.0/24)")
                self.network_discovery(network)
    
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
                    import dns.resolver
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
                 "✅" if mx_valid else "❌"),
                ("Disposable Email", "Checking...", "⏳")
            ]
            
            for check, result, status in checks:
                email_table.add_row(check, result, status)
            
            self.console.print(email_table)
            
            # Additional checks
            if domain:
                self.console.print(f"\n[bold yellow]Domain Information for {domain}:[/bold yellow]")
                # You can add more domain analysis here
            
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
                for platform, url in track(platforms.items(), description="Searching platforms..."):
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

# Additional utility functions can be added here
