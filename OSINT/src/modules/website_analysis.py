#!/usr/bin/env python3
"""
Website Analysis Module for KaliOSINT
Provides web technology detection, security analysis, and website intelligence
"""

import requests
import json
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import ssl
import socket
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Prompt, Confirm


class WebsiteAnalysis:
    def __init__(self, console=None, config=None, save_result=None):
        self.console = console or Console()
        self.config = config or {}
        self.save_result = save_result or self._default_save_result
    
    def _default_save_result(self, title, content):
        """Default save result function if none provided"""
        print(f"[SAVE] {title}: {content}")
    
    def website_analysis_menu(self):
        """Website analysis submenu"""
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Website Analysis[/bold cyan]", style="green"))
            
            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")
            
            options = [
                ("1", "Technology Stack Detection"),
                ("2", "SSL Certificate Analysis"),
                ("3", "Website Metadata Extraction"),
                ("4", "Directory/File Discovery"),
                ("5", "Subdomain Enumeration"),
                ("6", "Website Security Headers"),
                ("7", "Social Media Links Discovery"),
                ("0", "Back to Main Menu")
            ]
            
            for opt, tool in options:
                table.add_row(opt, tool)
            
            self.console.print(table)
            choice = Prompt.ask("Choose an option", choices=[opt for opt, _ in options])
            
            if choice == "0":
                break
            elif choice == "1":
                url = Prompt.ask("Enter website URL")
                self.website_tech_stack(url)
            elif choice == "2":
                url = Prompt.ask("Enter website URL")
                self.ssl_certificate_analysis(url)
            elif choice == "3":
                url = Prompt.ask("Enter website URL")
                self.website_metadata_extraction(url)
            elif choice == "4":
                url = Prompt.ask("Enter website URL")
                self.directory_discovery(url)
            elif choice == "5":
                domain = Prompt.ask("Enter domain")
                self.subdomain_enumeration(domain)
            elif choice == "6":
                url = Prompt.ask("Enter website URL")
                self.security_headers_check(url)
            elif choice == "7":
                url = Prompt.ask("Enter website URL")
                self.social_media_links_discovery(url)
            
            if choice != "0":
                Prompt.ask("Press Enter to continue...")
    
    def website_tech_stack(self, url):
        """Detect technologies used by a website"""
        self.console.print(f"[bold green]Analyzing tech stack for: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        results = {
            "url": url,
            "technologies": {},
            "server_info": {},
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            response = requests.get(url, timeout=10)
            results["status_code"] = response.status_code
            results["headers"] = dict(response.headers)
            
            # Server detection
            server = response.headers.get('Server', 'Unknown')
            results["server_info"]["server"] = server
            self.console.print(f"Server: {server}")
            
            # Framework detection patterns
            frameworks = {
                "WordPress": [r'wp-content', r'wp-includes', r'WordPress'],
                "Drupal": [r'Drupal\.settings', r'sites/default/files'],
                "Joomla": [r'option=com_', r'Joomla'],
                "Django": [r'csrfmiddlewaretoken', r'Django'],
                "Laravel": [r'laravel_session', r'Laravel'],
                "React": [r'React', r'react', r'_react'],
                "Angular": [r'ng-', r'angular', r'Angular'],
                "Vue.js": [r'Vue', r'vue', r'v-'],
                "Bootstrap": [r'bootstrap', r'Bootstrap'],
                "jQuery": [r'jquery', r'jQuery']
            }
            
            content = response.text
            detected_frameworks = []
            
            for framework, patterns in frameworks.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        detected_frameworks.append(framework)
                        break
            
            results["technologies"]["frameworks"] = list(set(detected_frameworks))
            
            # JavaScript libraries detection
            js_libs = []
            js_patterns = {
                "Google Analytics": r'google-analytics\.com|gtag\(',
                "Google Tag Manager": r'googletagmanager\.com',
                "Facebook Pixel": r'fbevents\.js|facebook\.net',
                "Hotjar": r'hotjar\.com',
                "Cloudflare": r'cloudflare\.com'
            }
            
            for lib, pattern in js_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    js_libs.append(lib)
            
            results["technologies"]["javascript_libraries"] = js_libs
            
            # Meta tag analysis
            soup = BeautifulSoup(content, 'html.parser')
            meta_generator = soup.find('meta', attrs={'name': 'generator'})
            if meta_generator:
                results["technologies"]["generator"] = meta_generator.get('content', '')
            
            # Display results
            if detected_frameworks:
                self.console.print(f"Frameworks detected: {', '.join(detected_frameworks)}")
            if js_libs:
                self.console.print(f"JavaScript libraries: {', '.join(js_libs)}")
            
        except requests.RequestException as e:
            self.console.print(f"[red]Error analyzing website: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Tech Stack Analysis - {url}", results)
        return results
    
    def ssl_certificate_analysis(self, url):
        """Analyze SSL certificate information"""
        self.console.print(f"[bold green]Analyzing SSL certificate for: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443
        
        results = {
            "hostname": hostname,
            "port": port,
            "certificate_info": {},
            "security_analysis": {},
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            # Get SSL certificate
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    results["certificate_info"] = {
                        "subject": dict(x[0] for x in cert.get('subject', [])),
                        "issuer": dict(x[0] for x in cert.get('issuer', [])),
                        "version": cert.get('version'),
                        "serial_number": cert.get('serialNumber'),
                        "not_before": cert.get('notBefore'),
                        "not_after": cert.get('notAfter'),
                        "alt_names": cert.get('subjectAltName', [])
                    }
                    
                    # Security analysis
                    cipher = ssock.cipher()
                    if cipher:
                        results["security_analysis"]["cipher"] = {
                            "name": cipher[0],
                            "protocol": cipher[1],
                            "bits": cipher[2]
                        }
                    
                    # Display key information
                    subject = results["certificate_info"]["subject"]
                    issuer = results["certificate_info"]["issuer"]
                    
                    self.console.print(f"Subject: {subject.get('commonName', 'Unknown')}")
                    self.console.print(f"Issuer: {issuer.get('organizationName', 'Unknown')}")
                    self.console.print(f"Valid until: {cert.get('notAfter')}")
                    
                    if cipher:
                        self.console.print(f"Cipher: {cipher[0]} ({cipher[2]} bits)")
        
        except Exception as e:
            self.console.print(f"[red]Error analyzing SSL certificate: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"SSL Analysis - {hostname}", results)
        return results
    
    def website_metadata_extraction(self, url):
        """Extract metadata from website"""
        self.console.print(f"[bold green]Extracting metadata from: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        results = {
            "url": url,
            "metadata": {},
            "social_tags": {},
            "links": [],
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic metadata
            title = soup.find('title')
            if title:
                results["metadata"]["title"] = title.get_text().strip()
                self.console.print(f"Title: {results['metadata']['title']}")
            
            # Meta tags
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name') or tag.get('property')
                content = tag.get('content')
                if name and content:
                    results["metadata"][name] = content
            
            # Open Graph tags
            og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
            for tag in og_tags:
                prop = tag.get('property')
                content = tag.get('content')
                if prop and content:
                    results["social_tags"][prop] = content
            
            # Twitter Card tags
            twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
            for tag in twitter_tags:
                name = tag.get('name')
                content = tag.get('content')
                if name and content:
                    results["social_tags"][name] = content
            
            # Extract links
            links = soup.find_all('a', href=True)
            for link in links[:20]:  # Limit to first 20 links
                href = link['href']
                text = link.get_text().strip()
                if href.startswith(('http://', 'https://')):
                    results["links"].append({"url": href, "text": text})
            
            # Display summary
            self.console.print(f"Found {len(results['metadata'])} meta tags")
            self.console.print(f"Found {len(results['social_tags'])} social media tags")
            self.console.print(f"Found {len(results['links'])} external links")
            
        except requests.RequestException as e:
            self.console.print(f"[red]Error extracting metadata: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Metadata Extraction - {url}", results)
        return results
    
    def directory_discovery(self, url):
        """Discover directories and files on website"""
        self.console.print(f"[bold green]Discovering directories for: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Common directories and files to check
        common_paths = [
            'admin', 'administrator', 'wp-admin', 'login', 'dashboard',
            'robots.txt', 'sitemap.xml', '.htaccess', '.env',
            'backup', 'test', 'dev', 'staging', 'api',
            'uploads', 'images', 'css', 'js', 'assets'
        ]
        
        results = {
            "url": url,
            "found_paths": [],
            "total_checked": 0,
            "analysis_date": datetime.now().isoformat()
        }
        
        base_url = url.rstrip('/')
        
        for path in track(common_paths, description="Checking paths..."):
            test_url = f"{base_url}/{path}"
            results["total_checked"] += 1
            
            try:
                response = requests.get(test_url, timeout=5, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    results["found_paths"].append({
                        "path": path,
                        "url": test_url,
                        "status_code": response.status_code,
                        "size": len(response.content)
                    })
                    self.console.print(f"✅ Found: /{path} (Status: {response.status_code})")
                
            except requests.RequestException:
                pass
        
        self.console.print(f"Checked {results['total_checked']} paths")
        self.console.print(f"Found {len(results['found_paths'])} accessible paths")
        
        self.save_result(f"Directory Discovery - {url}", results)
        return results
    
    def subdomain_enumeration(self, domain):
        """Enumerate subdomains for a domain"""
        self.console.print(f"[bold green]Enumerating subdomains for: {domain}[/bold green]")
        
        # Common subdomains to check
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
            'blog', 'shop', 'store', 'm', 'mobile', 'app', 'portal',
            'support', 'help', 'docs', 'wiki', 'forum', 'community'
        ]
        
        results = {
            "domain": domain,
            "found_subdomains": [],
            "total_checked": 0,
            "analysis_date": datetime.now().isoformat()
        }
        
        for subdomain in track(common_subdomains, description="Checking subdomains..."):
            full_domain = f"{subdomain}.{domain}"
            results["total_checked"] += 1
            
            try:
                socket.gethostbyname(full_domain)
                results["found_subdomains"].append(full_domain)
                self.console.print(f"✅ Found: {full_domain}")
                
            except socket.gaierror:
                pass
        
        self.console.print(f"Checked {results['total_checked']} subdomains")
        self.console.print(f"Found {len(results['found_subdomains'])} active subdomains")
        
        self.save_result(f"Subdomain Enumeration - {domain}", results)
        return results
    
    def security_headers_check(self, url):
        """Check website security headers"""
        self.console.print(f"[bold green]Checking security headers for: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Content-Security-Policy',
            'Referrer-Policy',
            'Permissions-Policy'
        ]
        
        results = {
            "url": url,
            "headers_present": {},
            "headers_missing": [],
            "security_score": 0,
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            for header in security_headers:
                if header in headers:
                    results["headers_present"][header] = headers[header]
                    results["security_score"] += 1
                    self.console.print(f"✅ {header}: {headers[header]}")
                else:
                    results["headers_missing"].append(header)
                    self.console.print(f"❌ Missing: {header}")
            
            # Calculate security score as percentage
            results["security_score"] = (results["security_score"] / len(security_headers)) * 100
            
            self.console.print(f"\nSecurity Score: {results['security_score']:.1f}%")
            
            if results["security_score"] < 50:
                self.console.print("[red]⚠️ Poor security headers implementation[/red]")
            elif results["security_score"] < 80:
                self.console.print("[yellow]⚠️ Moderate security headers implementation[/yellow]")
            else:
                self.console.print("[green]✅ Good security headers implementation[/green]")
        
        except requests.RequestException as e:
            self.console.print(f"[red]Error checking headers: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Security Headers - {url}", results)
        return results
    
    def social_media_links_discovery(self, url):
        """Discover social media links on website"""
        self.console.print(f"[bold green]Discovering social media links for: {url}[/bold green]")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        social_domains = [
            'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
            'youtube.com', 'tiktok.com', 'snapchat.com', 'pinterest.com',
            'reddit.com', 'discord.gg', 'telegram.org', 'whatsapp.com'
        ]
        
        results = {
            "url": url,
            "social_links": [],
            "analysis_date": datetime.now().isoformat()
        }
        
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                for domain in social_domains:
                    if domain in href:
                        results["social_links"].append({
                            "platform": domain.split('.')[0].title(),
                            "url": href,
                            "text": link.get_text().strip()
                        })
                        self.console.print(f"✅ Found {domain.split('.')[0].title()}: {href}")
                        break
            
            self.console.print(f"Found {len(results['social_links'])} social media links")
            
        except requests.RequestException as e:
            self.console.print(f"[red]Error discovering social links: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Social Media Discovery - {url}", results)
        return results
