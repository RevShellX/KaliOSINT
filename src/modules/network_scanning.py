#!/usr/bin/env python3
"""
Network Scanning Module for KaliOSINT
Provides network reconnaissance and port scanning capabilities
"""

import socket
import subprocess
import threading
import time
import os
import platform
import re
import ssl
import csv
from datetime import datetime
import ipaddress

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track, Progress
from rich.prompt import Prompt, Confirm


class NetworkScanning:
    def __init__(self, console=None, config=None, save_result=None):
        self.console = console or Console()
        self.config = config or {}
        self.save_result = save_result or self._default_save_result
    
    def _default_save_result(self, title, content):
        """Default save result function if none provided"""
        try:
            # Try to save to a simple text file
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"SCAN RESULT: {title}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"{'='*60}\n")
                f.write(str(content))
                f.write(f"\n{'='*60}\n\n")
            self.console.print(f"[green]Results saved to: {filename}[/green]")
        except Exception as e:
            self.console.print(f"[yellow]Could not save results: {e}[/yellow]")
            # At minimum, print the results to console
            self.console.print(f"[bold cyan]RESULTS - {title}:[/bold cyan]")
            self.console.print(str(content))
    
    def _safe_save_result(self, title, content):
        """Safely save results with error handling"""
        try:
            self.save_result(title, content)
        except Exception as e:
            self.console.print(f"[yellow]Could not save results: {e}[/yellow]")
            # Fallback to default save
            self._default_save_result(title, content)
    
    def network_scanning_menu(self):
        """Network scanning submenu with stop feature"""
        stop_requested = False
        while not stop_requested:
            self.console.clear()
            self.console.print(Panel("[bold cyan]Network Scanning[/bold cyan]", style="green"))

            table = Table()
            table.add_column("Option", style="cyan")
            table.add_column("Tool", style="white")

            options = [
                ("1", "Quick Port Scan"),
                ("2", "Service Detection"),
                ("3", "Network Range Scan"),
                ("4", "Operating System Detection"),
                ("5", "Vulnerability Scan"),
                ("6", "DNS Enumeration"),
                ("7", "WHOIS Lookup"),
                ("8", "Batch WHOIS Lookup"),
                ("9", "Traceroute"),
                ("10", "Subdomain Enumeration"),
                ("11", "Directory Brute Force"),
                ("12", "SSL/TLS Analysis"),
                ("13", "HTTP Headers Analysis"),
                ("14", "Technology Stack Detection"),
                ("15", "Email Harvesting"),
                ("16", "Shodan Search"),
                ("17", "Certificate Transparency"),
                ("18", "DNS Zone Transfer"),
                ("19", "SMB Enumeration"),
                ("20", "SNMP Enumeration"),
                ("21", "DNS Dig Analysis"),
                ("22", "Reverse DNS Lookup"),
                ("23", "DNS Cache Snooping"),
                ("24", "DNS Bruteforce"),
                ("25", "MX Record Analysis"),
                ("stop", "Stop/Exit Scanning Menu"),
                ("0", "Back to Main Menu")
            ]

            for opt, tool in options:
                table.add_row(opt, tool)

            self.console.print(table)
            choice = Prompt.ask("Choose an option", choices=[opt for opt, _ in options])

            if choice == "0":
                break
            if choice == "stop":
                self.console.print("[yellow]Stopping network scanning menu as requested.[/yellow]")
                stop_requested = True
                break
            elif choice == "1":
                target = Prompt.ask("Enter target IP or hostname")
                self.quick_port_scan(target)
            elif choice == "2":
                target = Prompt.ask("Enter target IP or hostname")
                self.service_detection(target)
            elif choice == "3":
                network = Prompt.ask("Enter network range (e.g., 192.168.1.0/24)")
                self.network_range_scan(network)
            elif choice == "4":
                target = Prompt.ask("Enter target IP or hostname")
                self.os_detection(target)
            elif choice == "5":
                target = Prompt.ask("Enter target IP or hostname")
                self.vulnerability_scan(target)
            elif choice == "6":
                domain = Prompt.ask("Enter domain name")
                self.dns_enumeration(domain)
            elif choice == "7":
                target = Prompt.ask("Enter domain or IP")
                self.whois_lookup(target)
            elif choice == "8":
                self.batch_whois_lookup()
            elif choice == "9":
                target = Prompt.ask("Enter target IP or hostname")
                self.traceroute(target)
            elif choice == "10":
                domain = Prompt.ask("Enter domain name")
                self.subdomain_enumeration(domain)
            elif choice == "11":
                target = Prompt.ask("Enter target URL (e.g., http://example.com)")
                self.directory_bruteforce(target)
            elif choice == "12":
                target = Prompt.ask("Enter target hostname")
                self.ssl_analysis(target)
            elif choice == "13":
                target = Prompt.ask("Enter target URL")
                self.http_headers_analysis(target)
            elif choice == "14":
                target = Prompt.ask("Enter target URL")
                self.technology_detection(target)
            elif choice == "15":
                domain = Prompt.ask("Enter domain name")
                self.email_harvesting(domain)
            elif choice == "16":
                query = Prompt.ask("Enter Shodan search query")
                self.shodan_search(query)
            elif choice == "17":
                domain = Prompt.ask("Enter domain name")
                self.certificate_transparency(domain)
            elif choice == "18":
                domain = Prompt.ask("Enter domain name")
                self.dns_zone_transfer(domain)
            elif choice == "19":
                target = Prompt.ask("Enter target IP")
                self.smb_enumeration(target)
            elif choice == "20":
                target = Prompt.ask("Enter target IP")
                self.snmp_enumeration(target)
            elif choice == "21":
                domain = Prompt.ask("Enter domain name")
                self.dns_dig_analysis(domain)
            elif choice == "22":
                ip = Prompt.ask("Enter IP address")
                self.reverse_dns_lookup(ip)
            elif choice == "23":
                dns_server = Prompt.ask("Enter DNS server IP")
                self.dns_cache_snooping(dns_server)
            elif choice == "24":
                domain = Prompt.ask("Enter domain name")
                self.dns_bruteforce(domain)
            elif choice == "25":
                domain = Prompt.ask("Enter domain name")
                self.mx_record_analysis(domain)

            if choice not in ("0", "stop"):
                Prompt.ask("Press Enter to continue...")
    
    def quick_port_scan(self, target):
        """Perform a quick port scan on common ports"""
        self.console.print(f"[bold green]Quick port scan for: {target}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        # Common ports to scan
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 6000, 6001, 8000, 8080, 8443, 8888
        ]
        
        results = {
            "target": target,
            "scan_type": "quick_port_scan",
            "open_ports": [],
            "closed_ports": [],
            "scan_date": datetime.now().isoformat(),
            "total_ports": len(common_ports)
        }
        
        def scan_port(host, port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except OSError:
                            service = "unknown"
                        
                        results["open_ports"].append({
                            "port": port,
                            "service": service,
                            "state": "open"
                        })
                        self.console.print(f"✅ Port {port} ({service}) is open")
                    else:
                        results["closed_ports"].append(port)
            except Exception as e:
                results["closed_ports"].append(port)
        
        # Resolve hostname to IP
        try:
            target_ip = socket.gethostbyname(target)
            results["target_ip"] = target_ip
            if target != target_ip:
                self.console.print(f"Resolved {target} to {target_ip}")
        except socket.gaierror:
            self.console.print(f"[red]Could not resolve {target}[/red]")
            return results
        
        try:
            # Scan ports with progress tracking
            threads = []
            for port in track(common_ports, description="Scanning ports..."):
                thread = threading.Thread(target=scan_port, args=(target_ip, port))
                thread.start()
                threads.append(thread)
                
                # Limit concurrent threads
                if len(threads) >= 50:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Port scan interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self.save_result(f"Port Scan (Interrupted) - {target}", results)
            return results
        
        self.console.print(f"\nScan complete: {len(results['open_ports'])} open ports found")
        
        if results["open_ports"]:
            table = Table()
            table.add_column("Port", style="cyan")
            table.add_column("Service", style="white")
            table.add_column("State", style="green")
            
            for port_info in results["open_ports"]:
                table.add_row(
                    str(port_info["port"]),
                    port_info["service"],
                    port_info["state"]
                )
            
            self.console.print(table)
        
        # Safe save with error handling
        try:
            self.save_result(f"Port Scan - {target}", results)
        except Exception as e:
            self.console.print(f"[yellow]Could not save results: {e}[/yellow]")
        
        return results
    
    def service_detection(self, target):
        """Detect services running on open ports"""
        self.console.print(f"[bold green]Service detection for: {target}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "target": target,
            "scan_type": "service_detection",
            "services": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # First, do a quick port scan to find open ports
            port_scan_results = self.quick_port_scan(target)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Service detection interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self.save_result(f"Service Detection (Interrupted) - {target}", results)
            return results
        
        if not port_scan_results.get("open_ports"):
            self.console.print("[yellow]No open ports found for service detection[/yellow]")
            return results
        
        target_ip = port_scan_results.get("target_ip", target)
        
        try:
            # Try to get more detailed service information
            for port_info in port_scan_results["open_ports"]:
                port = port_info["port"]
                
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(3)
                        sock.connect((target_ip, port))
                        
                        # Try to grab banner
                        banner = ""
                        try:
                            if port in [21, 22, 25, 110, 143]:  # Services that send banners
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port in [80, 8080, 8000]:  # HTTP services
                                sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        except:
                            pass
                        
                        service_info = {
                            "port": port,
                            "service": port_info["service"],
                            "banner": banner,
                            "protocol": "tcp"
                        }
                        
                        results["services"].append(service_info)
                        
                        if banner:
                            self.console.print(f"Port {port}: {banner[:100]}...")
                        else:
                            self.console.print(f"Port {port}: {port_info['service']} (no banner)")
                            
                except Exception as e:
                    self.console.print(f"[red]Error connecting to port {port}: {e}[/red]")
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Service detection interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"Service Detection (Interrupted) - {target}", results)
            return results
        
        self._safe_save_result(f"Service Detection - {target}", results)
        return results
    
    def network_range_scan(self, network):
        """Scan a network range for active hosts"""
        self.console.print(f"[bold green]Network range scan for: {network}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "network": network,
            "scan_type": "network_range_scan",
            "active_hosts": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            hosts = list(network_obj.hosts())
            
            if len(hosts) > 254:
                confirm = Confirm.ask(f"Scanning {len(hosts)} hosts may take a while. Continue?")
                if not confirm:
                    return results
            
            def ping_host(ip):
                try:
                    # Try to connect to port 80 first (faster than ping)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(1)
                        result = sock.connect_ex((str(ip), 80))
                        if result == 0:
                            results["active_hosts"].append({
                                "ip": str(ip),
                                "method": "tcp_80",
                                "hostname": None
                            })
                            self.console.print(f"✅ {ip} is active (TCP/80)")
                            return
                    
                    # If TCP/80 fails, try ping
                    import platform
                    if platform.system().lower() == "windows":
                        cmd = ["ping", "-n", "1", "-w", "1000", str(ip)]
                    else:
                        cmd = ["ping", "-c", "1", "-W", "1", str(ip)]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        # Try to resolve hostname
                        hostname = None
                        try:
                            hostname = socket.gethostbyaddr(str(ip))[0]
                        except:
                            pass
                        
                        results["active_hosts"].append({
                            "ip": str(ip),
                            "method": "ping",
                            "hostname": hostname
                        })
                        self.console.print(f"✅ {ip} is active (ping)")
                        
                except Exception:
                    pass
            
            # Scan hosts with progress tracking
            threads = []
            for ip in track(hosts[:50], description="Scanning hosts..."):  # Limit to first 50
                thread = threading.Thread(target=ping_host, args=(ip,))
                thread.start()
                threads.append(thread)
                
                # Limit concurrent threads
                if len(threads) >= 20:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
            
            self.console.print(f"\nFound {len(results['active_hosts'])} active hosts")
            
        except ValueError as e:
            self.console.print(f"[red]Invalid network format: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Network range scan interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"Network Scan (Interrupted) - {network}", results)
            return results
        
        self._safe_save_result(f"Network Scan - {network}", results)
        return results
    
    def os_detection(self, target):
        """Attempt OS detection using various techniques"""
        self.console.print(f"[bold green]OS detection for: {target}[/bold green]")
        
        results = {
            "target": target,
            "scan_type": "os_detection",
            "os_hints": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            target_ip = socket.gethostbyname(target)
            results["target_ip"] = target_ip
        except socket.gaierror:
            self.console.print(f"[red]Could not resolve {target}[/red]")
            return results
        
        # TTL-based OS detection
        try:
            import platform
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", target_ip]
            else:
                cmd = ["ping", "-c", "1", target_ip]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout
                
                # Extract TTL
                import re
                ttl_match = re.search(r'TTL=(\d+)', output, re.IGNORECASE)
                if ttl_match:
                    ttl = int(ttl_match.group(1))
                    
                    # Common TTL values for OS detection
                    if ttl <= 64:
                        if ttl == 64:
                            os_guess = "Linux/Unix"
                        else:
                            os_guess = "Linux/Unix (through router)"
                    elif ttl <= 128:
                        if ttl == 128:
                            os_guess = "Windows"
                        else:
                            os_guess = "Windows (through router)"
                    else:
                        os_guess = "Unknown/Custom"
                    
                    results["os_hints"].append({
                        "method": "ttl_analysis",
                        "ttl": ttl,
                        "os_guess": os_guess
                    })
                    
                    self.console.print(f"TTL: {ttl} → Likely OS: {os_guess}")
        
        except Exception as e:
            self.console.print(f"[yellow]Could not perform TTL analysis: {e}[/yellow]")
        
        # Port-based OS fingerprinting
        windows_ports = [135, 139, 445, 3389]
        linux_ports = [22, 111]
        
        open_ports = []
        for port in windows_ports + linux_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        open_ports.append(port)
            except:
                pass
        
        if any(port in open_ports for port in windows_ports):
            results["os_hints"].append({
                "method": "port_analysis",
                "evidence": f"Windows-specific ports open: {[p for p in windows_ports if p in open_ports]}",
                "os_guess": "Windows"
            })
            self.console.print("Windows-specific services detected")
        
        if any(port in open_ports for port in linux_ports):
            results["os_hints"].append({
                "method": "port_analysis",
                "evidence": f"Linux-specific ports open: {[p for p in linux_ports if p in open_ports]}",
                "os_guess": "Linux/Unix"
            })
            self.console.print("Linux/Unix-specific services detected")
        
        if not results["os_hints"]:
            self.console.print("[yellow]Could not determine OS with confidence[/yellow]")
        
        self.save_result(f"OS Detection - {target}", results)
        return results
    
    def vulnerability_scan(self, target):
        """Basic vulnerability scanning"""
        self.console.print(f"[bold green]Vulnerability scan for: {target}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "target": target,
            "scan_type": "vulnerability_scan",
            "vulnerabilities": [],
            "scan_date": datetime.now().isoformat()
        }
        
        # This is a basic implementation - real vulnerability scanning requires extensive databases
        self.console.print("[blue]ℹ️ This is a basic vulnerability check[/blue]")
        self.console.print("[blue]ℹ️ For comprehensive scans, use tools like Nessus, OpenVAS, or Nmap scripts[/blue]")
        
        # Check for common vulnerable services
        vulnerable_services = {
            21: "FTP - Check for anonymous access",
            23: "Telnet - Unencrypted protocol",
            53: "DNS - Check for zone transfers",
            135: "RPC - Potential for MS-RPC vulnerabilities",
            139: "NetBIOS - SMB enumeration possible",
            445: "SMB - Check for SMB vulnerabilities"
        }
        
        try:
            target_ip = socket.gethostbyname(target)
            results["target_ip"] = target_ip
        except socket.gaierror:
            self.console.print(f"[red]Could not resolve {target}[/red]")
            return results
        
        try:
            for port, description in vulnerable_services.items():
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(2)
                        result = sock.connect_ex((target_ip, port))
                        if result == 0:
                            results["vulnerabilities"].append({
                                "port": port,
                                "service": socket.getservbyport(port, "tcp"),
                                "description": description,
                                "severity": "info"
                            })
                            self.console.print(f"⚠️ Port {port} open: {description}")
                except:
                    pass
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Vulnerability scan interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"Vulnerability Scan (Interrupted) - {target}", results)
            return results
        
        # Check for common misconfigurations
        if not results["vulnerabilities"]:
            self.console.print("[green]✅ No obvious vulnerabilities detected[/green]")
        else:
            self.console.print(f"[yellow]Found {len(results['vulnerabilities'])} potential issues[/yellow]")
        
        self._safe_save_result(f"Vulnerability Scan - {target}", results)
        return results
    
    def dns_enumeration(self, domain):
        """Enumerate DNS records for a domain"""
        self.console.print(f"[bold green]DNS enumeration for: {domain}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "dns_enumeration",
            "dns_records": {},
            "scan_date": datetime.now().isoformat()
        }
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        try:
            import dns.resolver
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records = [str(answer) for answer in answers]
                    results["dns_records"][record_type] = records
                    
                    self.console.print(f"{record_type} records: {len(records)}")
                    for record in records:
                        self.console.print(f"  → {record}")
                
                except dns.resolver.NXDOMAIN:
                    self.console.print(f"[red]Domain {domain} does not exist[/red]")
                    break
                except dns.resolver.NoAnswer:
                    pass  # No records of this type
                except Exception as e:
                    self.console.print(f"[yellow]Error querying {record_type}: {e}[/yellow]")
        
        except ImportError:
            self.console.print("[yellow]⚠️ dnspython not installed, using basic DNS lookup[/yellow]")
            
            # Basic DNS lookup without dnspython
            try:
                ip = socket.gethostbyname(domain)
                results["dns_records"]["A"] = [ip]
                self.console.print(f"A record: {ip}")
            except socket.gaierror:
                self.console.print(f"[red]Could not resolve {domain}[/red]")
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]DNS enumeration interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"DNS Enumeration (Interrupted) - {domain}", results)
            return results
        
        self._safe_save_result(f"DNS Enumeration - {domain}", results)
        return results
    
    def whois_lookup(self, target):
        """Perform WHOIS lookup"""
        self.console.print(f"[bold green]WHOIS lookup for: {target}[/bold green]")
        
        results = {
            "target": target,
            "scan_type": "whois_lookup",
            "whois_data": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Try to use whois command
            import subprocess
            result = subprocess.run(["whois", target], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                whois_output = result.stdout
                results["whois_data"]["raw"] = whois_output
                
                # Parse some basic information
                lines = whois_output.split('\n')
                for line in lines[:20]:  # Show first 20 lines
                    if line.strip():
                        self.console.print(line)
                
                # Extract key information
                import re
                
                # Find registrar
                registrar_match = re.search(r'Registrar:\s*(.+)', whois_output, re.IGNORECASE)
                if registrar_match:
                    results["whois_data"]["registrar"] = registrar_match.group(1).strip()
                
                # Find creation date
                created_match = re.search(r'Creation Date:\s*(.+)', whois_output, re.IGNORECASE)
                if created_match:
                    results["whois_data"]["created"] = created_match.group(1).strip()
                
                # Find expiration date
                expires_match = re.search(r'Expiration Date:\s*(.+)', whois_output, re.IGNORECASE)
                if expires_match:
                    results["whois_data"]["expires"] = expires_match.group(1).strip()
            
            else:
                self.console.print(f"[red]WHOIS command failed: {result.stderr}[/red]")
        
        except FileNotFoundError:
            self.console.print("[yellow]⚠️ WHOIS command not found[/yellow]")
            self.console.print("[blue]ℹ️ Install whois utility or use online WHOIS services[/blue]")
        except subprocess.TimeoutExpired:
            self.console.print("[red]WHOIS lookup timed out[/red]")
        except Exception as e:
            self.console.print(f"[red]Error performing WHOIS lookup: {e}[/red]")
        
        self.save_result(f"WHOIS Lookup - {target}", results)
        return results
    
    def batch_whois_lookup(self):
        """Perform WHOIS lookup on multiple targets"""
        self.console.print(Panel("[bold cyan]Batch WHOIS Lookup[/bold cyan]", style="green"))
        
        # Input methods
        input_methods = [
            ("1", "Enter targets manually (comma-separated)"),
            ("2", "Load from file"),
            ("3", "Enter targets line by line"),
            ("0", "Back to menu")
        ]
        
        method_table = Table()
        method_table.add_column("Option", style="cyan")
        method_table.add_column("Method", style="white")
        
        for opt, method in input_methods:
            method_table.add_row(opt, method)
        
        self.console.print(method_table)
        method_choice = Prompt.ask("Choose input method", choices=[opt for opt, _ in input_methods])
        
        if method_choice == "0":
            return
        
        targets = []
        
        if method_choice == "1":
            # Manual input, comma-separated
            targets_input = Prompt.ask("Enter domains/IPs separated by commas")
            targets = [target.strip() for target in targets_input.split(",") if target.strip()]
        
        elif method_choice == "2":
            # Load from file
            file_path = Prompt.ask("Enter file path")
            try:
                with open(file_path, 'r') as f:
                    targets = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                self.console.print(f"[green]Loaded {len(targets)} targets from file[/green]")
            except FileNotFoundError:
                self.console.print(f"[red]File not found: {file_path}[/red]")
                return
            except Exception as e:
                self.console.print(f"[red]Error reading file: {e}[/red]")
                return
        
        elif method_choice == "3":
            # Line by line input
            self.console.print("[blue]Enter targets one per line. Press Enter on empty line to finish:[/blue]")
            while True:
                target = Prompt.ask("Domain/IP (or press Enter to finish)", default="")
                if not target:
                    break
                targets.append(target.strip())
        
        if not targets:
            self.console.print("[yellow]No targets provided[/yellow]")
            return
        
        # Confirm batch operation
        self.console.print(f"[blue]Found {len(targets)} targets to analyze:[/blue]")
        for i, target in enumerate(targets[:10], 1):  # Show first 10
            self.console.print(f"  {i}. {target}")
        
        if len(targets) > 10:
            self.console.print(f"  ... and {len(targets) - 10} more")
        
        if not Confirm.ask(f"Proceed with batch WHOIS lookup for {len(targets)} targets?"):
            return
        
        # Perform batch WHOIS lookup
        batch_results = {
            "batch_type": "whois_lookup",
            "total_targets": len(targets),
            "results": [],
            "successful": 0,
            "failed": 0,
            "scan_date": datetime.now().isoformat()
        }
        
        self.console.print(f"[bold green]Starting batch WHOIS lookup for {len(targets)} targets...[/bold green]")
        
        for target in track(targets, description="Processing WHOIS lookups..."):
            try:
                self.console.print(f"\n[cyan]Processing: {target}[/cyan]")
                result = self.whois_lookup_single(target)
                
                if result and result.get("whois_data"):
                    batch_results["successful"] += 1
                    self.console.print(f"[green]✅ {target} - Success[/green]")
                else:
                    batch_results["failed"] += 1
                    self.console.print(f"[red]❌ {target} - Failed[/red]")
                
                batch_results["results"].append({
                    "target": target,
                    "result": result,
                    "status": "success" if result and result.get("whois_data") else "failed"
                })
                
                # Small delay to avoid overwhelming servers
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Batch operation cancelled by user[/yellow]")
                break
            except Exception as e:
                batch_results["failed"] += 1
                batch_results["results"].append({
                    "target": target,
                    "result": None,
                    "status": "error",
                    "error": str(e)
                })
                self.console.print(f"[red]❌ {target} - Error: {e}[/red]")
        
        # Display summary
        self.console.print("\n" + "="*50)
        self.console.print(f"[bold cyan]Batch WHOIS Lookup Summary[/bold cyan]")
        self.console.print(f"Total targets: {batch_results['total_targets']}")
        self.console.print(f"[green]Successful: {batch_results['successful']}[/green]")
        self.console.print(f"[red]Failed: {batch_results['failed']}[/red]")
        
        # Show results table
        if batch_results["results"]:
            results_table = Table()
            results_table.add_column("Target", style="cyan")
            results_table.add_column("Status", style="white")
            results_table.add_column("Registrar", style="yellow")
            results_table.add_column("Created", style="green")
            results_table.add_column("Expires", style="red")
            
            for item in batch_results["results"]:
                target = item["target"]
                status = item["status"]
                
                if status == "success" and item["result"]:
                    whois_data = item["result"].get("whois_data", {})
                    registrar = whois_data.get("registrar", "N/A")[:30]
                    created = whois_data.get("created", "N/A")[:20]
                    expires = whois_data.get("expires", "N/A")[:20]
                    
                    results_table.add_row(
                        target,
                        f"[green]{status}[/green]",
                        registrar,
                        created,
                        expires
                    )
                else:
                    results_table.add_row(
                        target,
                        f"[red]{status}[/red]",
                        "N/A",
                        "N/A", 
                        "N/A"
                    )
            
            self.console.print(results_table)
        
        # Save batch results
        self.save_result("Batch WHOIS Lookup", batch_results)
        
        # Export options
        if Confirm.ask("Export results to CSV file?"):
            self.export_batch_whois_csv(batch_results)
        
        return batch_results
    
    def whois_lookup_single(self, target):
        """Perform single WHOIS lookup without console output for batch processing"""
        results = {
            "target": target,
            "scan_type": "whois_lookup",
            "whois_data": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Try to use whois command
            import subprocess
            result = subprocess.run(["whois", target], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                whois_output = result.stdout
                results["whois_data"]["raw"] = whois_output
                
                # Extract key information
                import re
                
                # Find registrar
                registrar_match = re.search(r'Registrar:\s*(.+)', whois_output, re.IGNORECASE)
                if registrar_match:
                    results["whois_data"]["registrar"] = registrar_match.group(1).strip()
                
                # Find creation date
                created_match = re.search(r'Creation Date:\s*(.+)', whois_output, re.IGNORECASE)
                if created_match:
                    results["whois_data"]["created"] = created_match.group(1).strip()
                
                # Find expiration date
                expires_match = re.search(r'Expiration Date:\s*(.+)', whois_output, re.IGNORECASE)
                if expires_match:
                    results["whois_data"]["expires"] = expires_match.group(1).strip()
                
                # Find updated date
                updated_match = re.search(r'Updated Date:\s*(.+)', whois_output, re.IGNORECASE)
                if updated_match:
                    results["whois_data"]["updated"] = updated_match.group(1).strip()
                
                # Find name servers
                ns_matches = re.findall(r'Name Server:\s*(.+)', whois_output, re.IGNORECASE)
                if ns_matches:
                    results["whois_data"]["name_servers"] = [ns.strip() for ns in ns_matches]
                
                # Find registrant info
                registrant_match = re.search(r'Registrant.*?Organization:\s*(.+)', whois_output, re.IGNORECASE | re.DOTALL)
                if registrant_match:
                    results["whois_data"]["registrant_org"] = registrant_match.group(1).strip()
            
            else:
                results["whois_data"]["error"] = result.stderr
        
        except FileNotFoundError:
            results["whois_data"]["error"] = "WHOIS command not found"
        except subprocess.TimeoutExpired:
            results["whois_data"]["error"] = "WHOIS lookup timed out"
        except Exception as e:
            results["whois_data"]["error"] = str(e)
        
        return results
    
    def export_batch_whois_csv(self, batch_results):
        """Export batch WHOIS results to CSV file"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"batch_whois_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Target', 'Status', 'Registrar', 'Created', 'Updated', 'Expires', 'Name_Servers', 'Registrant_Org', 'Error']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for item in batch_results["results"]:
                    target = item["target"]
                    status = item["status"]
                    
                    row = {'Target': target, 'Status': status}
                    
                    if status == "success" and item["result"]:
                        whois_data = item["result"].get("whois_data", {})
                        row.update({
                            'Registrar': whois_data.get("registrar", ""),
                            'Created': whois_data.get("created", ""),
                            'Updated': whois_data.get("updated", ""),
                            'Expires': whois_data.get("expires", ""),
                            'Name_Servers': "; ".join(whois_data.get("name_servers", [])),
                            'Registrant_Org': whois_data.get("registrant_org", ""),
                            'Error': ""
                        })
                    else:
                        row.update({
                            'Registrar': "",
                            'Created': "",
                            'Updated': "",
                            'Expires': "",
                            'Name_Servers': "",
                            'Registrant_Org': "",
                            'Error': item.get("error", "Unknown error")
                        })
                    
                    writer.writerow(row)
            
            self.console.print(f"[green]✅ Results exported to: {filename}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Error exporting to CSV: {e}[/red]")
    
    def traceroute(self, target):
        """Perform traceroute to target"""
        self.console.print(f"[bold green]Traceroute to: {target}[/bold green]")
        
        results = {
            "target": target,
            "scan_type": "traceroute",
            "hops": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import platform
            
            if platform.system().lower() == "windows":
                cmd = ["tracert", "-h", "15", target]
            else:
                cmd = ["traceroute", "-m", "15", target]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            hop_number = 0
            for line in process.stdout:
                line = line.strip()
                if line:
                    hop_number += 1
                    results["hops"].append({
                        "hop": hop_number,
                        "output": line
                    })
                    self.console.print(f"{hop_number:2d}: {line}")
                    
                    if hop_number >= 15:  # Limit hops
                        break
            
            process.wait()
            
        except FileNotFoundError:
            self.console.print("[yellow]⚠️ Traceroute command not found[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error performing traceroute: {e}[/red]")
        
        self.save_result(f"Traceroute - {target}", results)
        return results
    
    def subdomain_enumeration(self, domain):
        """Enumerate subdomains using various techniques"""
        self.console.print(f"[bold green]Subdomain enumeration for: {domain}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "subdomain_enumeration",
            "subdomains": [],
            "scan_date": datetime.now().isoformat()
        }
        
        # Common subdomain wordlist
        common_subdomains = [
            "www", "mail", "ftp", "admin", "test", "dev", "staging", "api", "blog", "shop",
            "support", "help", "cdn", "img", "static", "assets", "portal", "secure", "vpn",
            "remote", "mx", "ns", "ns1", "ns2", "dns", "email", "smtp", "pop", "imap",
            "webmail", "autoconfig", "autodiscover", "cpanel", "whm", "plesk", "directadmin"
        ]
        
        self.console.print(f"Testing {len(common_subdomains)} common subdomains...")
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(full_domain)
                results["subdomains"].append({
                    "subdomain": full_domain,
                    "ip": ip,
                    "method": "dns_lookup"
                })
                self.console.print(f"✅ {full_domain} → {ip}")
                return True
            except socket.gaierror:
                return False
        
        try:
            # Test subdomains with threading
            threads = []
            for subdomain in track(common_subdomains, description="Checking subdomains..."):
                thread = threading.Thread(target=check_subdomain, args=(subdomain,))
                thread.start()
                threads.append(thread)
                
                # Limit threads
                if len(threads) >= 10:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Subdomain enumeration interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self.save_result(f"Subdomain Enumeration (Interrupted) - {domain}", results)
            return results
        
        # Certificate Transparency lookup
        try:
            import requests
            ct_url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = requests.get(ct_url, timeout=10)
            
            if response.status_code == 200:
                ct_data = response.json()
                ct_subdomains = set()
                
                for cert in ct_data:
                    name = cert.get('name_value', '')
                    if name and domain in name:
                        # Handle wildcard and multi-line certificates
                        names = name.replace('*', '').split('\n')
                        for n in names:
                            n = n.strip()
                            if n.endswith(f".{domain}") and n not in [s['subdomain'] for s in results["subdomains"]]:
                                ct_subdomains.add(n)
                
                self.console.print(f"Found {len(ct_subdomains)} additional subdomains from Certificate Transparency")
                
                for subdomain in ct_subdomains:
                    try:
                        ip = socket.gethostbyname(subdomain)
                        results["subdomains"].append({
                            "subdomain": subdomain,
                            "ip": ip,
                            "method": "certificate_transparency"
                        })
                        self.console.print(f"🔍 {subdomain} → {ip}")
                    except socket.gaierror:
                        results["subdomains"].append({
                            "subdomain": subdomain,
                            "ip": "N/A",
                            "method": "certificate_transparency"
                        })
        
        except Exception as e:
            self.console.print(f"[yellow]Certificate Transparency lookup failed: {e}[/yellow]")
        
        self.console.print(f"\nFound {len(results['subdomains'])} subdomains")
        self.save_result(f"Subdomain Enumeration - {domain}", results)
        return results
    
    def directory_bruteforce(self, target_url):
        """Brute force directories and files"""
        self.console.print(f"[bold green]Directory brute force for: {target_url}[/bold green]")
        self.console.print("[yellow]⚠️ Only use this against systems you own or have permission to test[/yellow]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "target": target_url,
            "scan_type": "directory_bruteforce",
            "found_paths": [],
            "scan_date": datetime.now().isoformat()
        }
        
        # Common directories and files
        common_paths = [
            "admin", "administrator", "login", "wp-admin", "phpmyadmin", "cpanel",
            "backup", "test", "dev", "api", "uploads", "images", "css", "js",
            "robots.txt", "sitemap.xml", ".htaccess", "web.config", "config.php",
            "database.sql", "backup.zip", "install.php", "readme.txt", "changelog.txt"
        ]
        
        if not Confirm.ask("This will send multiple requests to the target. Continue?"):
            return results
        
        import requests
        from urllib.parse import urljoin
        
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        def check_path(path):
            try:
                url = urljoin(target_url, path)
                response = session.get(url, timeout=5, allow_redirects=False)
                
                if response.status_code in [200, 301, 302, 403]:
                    results["found_paths"].append({
                        "path": path,
                        "url": url,
                        "status_code": response.status_code,
                        "content_length": len(response.content),
                        "content_type": response.headers.get('content-type', 'N/A')
                    })
                    
                    status_color = "green" if response.status_code == 200 else "yellow"
                    self.console.print(f"[{status_color}]{response.status_code}[/{status_color}] {url} ({len(response.content)} bytes)")
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                pass
        
        try:
            # Check paths with threading
            threads = []
            for path in track(common_paths, description="Checking paths..."):
                thread = threading.Thread(target=check_path, args=(path,))
                thread.start()
                threads.append(thread)
                
                # Limit threads to avoid overwhelming target
                if len(threads) >= 5:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Directory brute force interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self.save_result(f"Directory Brute Force (Interrupted) - {target_url}", results)
            return results
        
        self.console.print(f"\nFound {len(results['found_paths'])} accessible paths")
        self.save_result(f"Directory Brute Force - {target_url}", results)
        return results
    
    def ssl_analysis(self, hostname):
        """Analyze SSL/TLS configuration"""
        self.console.print(f"[bold green]SSL/TLS analysis for: {hostname}[/bold green]")
        
        results = {
            "hostname": hostname,
            "scan_type": "ssl_analysis",
            "ssl_info": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import ssl
            import socket
            from datetime import datetime
            
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Connect and get certificate
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    results["ssl_info"] = {
                        "subject": dict(x[0] for x in cert.get('subject', [])),
                        "issuer": dict(x[0] for x in cert.get('issuer', [])),
                        "version": cert.get('version'),
                        "serial_number": cert.get('serialNumber'),
                        "not_before": cert.get('notBefore'),
                        "not_after": cert.get('notAfter'),
                        "subject_alt_names": [x[1] for x in cert.get('subjectAltName', [])],
                        "cipher_suite": cipher,
                        "ssl_version": version
                    }
                    
                    # Display results
                    self.console.print(f"Subject: {results['ssl_info']['subject'].get('commonName', 'N/A')}")
                    self.console.print(f"Issuer: {results['ssl_info']['issuer'].get('organizationName', 'N/A')}")
                    self.console.print(f"Valid from: {results['ssl_info']['not_before']}")
                    self.console.print(f"Valid until: {results['ssl_info']['not_after']}")
                    self.console.print(f"SSL Version: {version}")
                    self.console.print(f"Cipher: {cipher[0]} ({cipher[1]}-bit)")
                    
                    if results['ssl_info']['subject_alt_names']:
                        self.console.print(f"Alt Names: {', '.join(results['ssl_info']['subject_alt_names'][:5])}")
        
        except Exception as e:
            self.console.print(f"[red]SSL analysis failed: {e}[/red]")
            results["ssl_info"]["error"] = str(e)
        
        self.save_result(f"SSL Analysis - {hostname}", results)
        return results
    
    def http_headers_analysis(self, url):
        """Analyze HTTP headers for security and information"""
        self.console.print(f"[bold green]HTTP headers analysis for: {url}[/bold green]")
        
        results = {
            "url": url,
            "scan_type": "http_headers_analysis",
            "headers": {},
            "security_headers": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import requests
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            results["headers"] = dict(response.headers)
            results["status_code"] = response.status_code
            
            # Security headers to check
            security_headers = {
                "Strict-Transport-Security": "HSTS",
                "Content-Security-Policy": "CSP",
                "X-Frame-Options": "Clickjacking Protection",
                "X-Content-Type-Options": "MIME Type Sniffing Protection",
                "X-XSS-Protection": "XSS Protection",
                "Referrer-Policy": "Referrer Policy",
                "Permissions-Policy": "Permissions Policy"
            }
            
            # Check security headers
            for header, description in security_headers.items():
                if header in response.headers:
                    results["security_headers"][header] = {
                        "present": True,
                        "value": response.headers[header],
                        "description": description
                    }
                    self.console.print(f"✅ {header}: {response.headers[header]}")
                else:
                    results["security_headers"][header] = {
                        "present": False,
                        "description": description
                    }
                    self.console.print(f"❌ {header}: Missing")
            
            # Interesting headers
            interesting_headers = ["Server", "X-Powered-By", "X-AspNet-Version", "X-Generator"]
            for header in interesting_headers:
                if header in response.headers:
                    self.console.print(f"🔍 {header}: {response.headers[header]}")
        
        except Exception as e:
            self.console.print(f"[red]HTTP headers analysis failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"HTTP Headers Analysis - {url}", results)
        return results
    
    def technology_detection(self, url):
        """Detect web technologies using various techniques"""
        self.console.print(f"[bold green]Technology detection for: {url}[/bold green]")
        
        results = {
            "url": url,
            "scan_type": "technology_detection",
            "technologies": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import requests
            import re
            
            response = requests.get(url, timeout=10)
            content = response.text.lower()
            headers = response.headers
            
            # Technology signatures
            tech_signatures = {
                "WordPress": [r"wp-content", r"wp-includes", r"/wp-json/"],
                "Drupal": [r"drupal", r"sites/default/files"],
                "Joomla": [r"joomla", r"administrator/index.php"],
                "PHP": [r"php", r"\.php"],
                "ASP.NET": [r"aspnet", r"\.aspx", r"viewstate"],
                "Apache": [r"apache"],
                "Nginx": [r"nginx"],
                "jQuery": [r"jquery"],
                "Bootstrap": [r"bootstrap"],
                "React": [r"react", r"_react"],
                "Angular": [r"angular", r"ng-"],
                "Vue.js": [r"vue\.js", r"__vue__"]
            }
            
            # Check content for signatures
            for tech, patterns in tech_signatures.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        results["technologies"].append({
                            "name": tech,
                            "detection_method": "content_analysis",
                            "pattern": pattern
                        })
                        self.console.print(f"🔍 Detected: {tech}")
                        break
            
            # Check headers
            if "server" in headers:
                server = headers["server"]
                results["technologies"].append({
                    "name": f"Web Server: {server}",
                    "detection_method": "http_headers",
                    "value": server
                })
                self.console.print(f"🌐 Server: {server}")
            
            if "x-powered-by" in headers:
                powered_by = headers["x-powered-by"]
                results["technologies"].append({
                    "name": f"Powered by: {powered_by}",
                    "detection_method": "http_headers",
                    "value": powered_by
                })
                self.console.print(f"⚡ Powered by: {powered_by}")
        
        except Exception as e:
            self.console.print(f"[red]Technology detection failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Technology Detection - {url}", results)
        return results
    
    def email_harvesting(self, domain):
        """Harvest email addresses from various sources"""
        self.console.print(f"[bold green]Email harvesting for: {domain}[/bold green]")
        self.console.print("[yellow]⚠️ Only use this for legitimate purposes and with proper authorization[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "email_harvesting",
            "emails": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import requests
            import re
            
            # Common email patterns
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            # Search engines and sources (simplified for demonstration)
            sources = [
                f"https://www.google.com/search?q=site:{domain}+%40{domain}",
                f"https://www.bing.com/search?q=site:{domain}+%40{domain}"
            ]
            
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            
            # Note: This is a simplified implementation
            # Real email harvesting would use specialized tools and APIs
            
            self.console.print("[blue]ℹ️ This is a basic implementation[/blue]")
            self.console.print("[blue]ℹ️ For comprehensive email harvesting, use tools like theHarvester[/blue]")
            
            # Generate common email patterns
            common_patterns = [
                f"admin@{domain}",
                f"info@{domain}",
                f"contact@{domain}",
                f"support@{domain}",
                f"sales@{domain}",
                f"webmaster@{domain}"
            ]
            
            for email in common_patterns:
                results["emails"].append({
                    "email": email,
                    "source": "common_patterns",
                    "verified": False
                })
                self.console.print(f"📧 {email} (pattern-based)")
        
        except Exception as e:
            self.console.print(f"[red]Email harvesting failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Email Harvesting - {domain}", results)
        return results
    
    def shodan_search(self, query):
        """Search Shodan for information"""
        self.console.print(f"[bold green]Shodan search for: {query}[/bold green]")
        
        results = {
            "query": query,
            "scan_type": "shodan_search",
            "results": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Note: This requires a Shodan API key
            self.console.print("[blue]ℹ️ Shodan API key required[/blue]")
            self.console.print("[blue]ℹ️ Set SHODAN_API_KEY environment variable or add to config[/blue]")
            
            api_key = self.config.get('shodan_api_key') or os.environ.get('SHODAN_API_KEY')
            
            if not api_key:
                self.console.print("[yellow]No Shodan API key found[/yellow]")
                return results
            
            import requests
            
            url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results["results"] = data.get("matches", [])
                
                self.console.print(f"Found {len(results['results'])} results")
                
                # Display first few results
                for i, result in enumerate(results["results"][:5]):
                    self.console.print(f"\n{i+1}. {result.get('ip_str', 'N/A')}:{result.get('port', 'N/A')}")
                    self.console.print(f"   Organization: {result.get('org', 'N/A')}")
                    self.console.print(f"   Location: {result.get('location', {}).get('city', 'N/A')}, {result.get('location', {}).get('country_name', 'N/A')}")
                    self.console.print(f"   Product: {result.get('product', 'N/A')}")
            else:
                self.console.print(f"[red]Shodan API error: {response.status_code}[/red]")
        
        except Exception as e:
            self.console.print(f"[red]Shodan search failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Shodan Search - {query}", results)
        return results
    
    def certificate_transparency(self, domain):
        """Search Certificate Transparency logs"""
        self.console.print(f"[bold green]Certificate Transparency search for: {domain}[/bold green]")
        
        results = {
            "domain": domain,
            "scan_type": "certificate_transparency",
            "certificates": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import requests
            
            # crt.sh API
            url = f"https://crt.sh/?q={domain}&output=json"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                certificates = response.json()
                results["certificates"] = certificates[:50]  # Limit results
                
                self.console.print(f"Found {len(certificates)} certificates")
                
                # Display summary
                cert_table = Table()
                cert_table.add_column("ID", style="cyan")
                cert_table.add_column("Common Name", style="white")
                cert_table.add_column("Issuer", style="yellow")
                cert_table.add_column("Not After", style="green")
                
                for cert in certificates[:10]:  # Show first 10
                    cert_table.add_row(
                        str(cert.get('id', 'N/A')),
                        cert.get('common_name', 'N/A')[:30],
                        cert.get('issuer_name', 'N/A')[:30],
                        cert.get('not_after', 'N/A')[:10]
                    )
                
                self.console.print(cert_table)
            else:
                self.console.print(f"[red]Certificate Transparency search failed: {response.status_code}[/red]")
        
        except Exception as e:
            self.console.print(f"[red]Certificate Transparency search failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"Certificate Transparency - {domain}", results)
        return results
    
    def dns_zone_transfer(self, domain):
        """Attempt DNS zone transfer"""
        self.console.print(f"[bold green]DNS zone transfer attempt for: {domain}[/bold green]")
        self.console.print("[yellow]⚠️ Zone transfers are usually restricted to authorized servers[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "dns_zone_transfer",
            "transfers": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            import dns.resolver
            import dns.zone
            import dns.query
            
            # Get NS records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                name_servers = [str(ns) for ns in ns_records]
                
                self.console.print(f"Found {len(name_servers)} name servers")
                
                for ns in name_servers:
                    self.console.print(f"Trying zone transfer from {ns}")
                    
                    try:
                        # Attempt zone transfer
                        zone = dns.zone.from_xfr(dns.query.xfr(ns, domain))
                        
                        # If successful, extract records
                        records = []
                        for name, node in zone.nodes.items():
                            for rdataset in node.rdatasets:
                                for rdata in rdataset:
                                    records.append({
                                        "name": str(name),
                                        "type": dns.rdatatype.to_text(rdataset.rdtype),
                                        "value": str(rdata)
                                    })
                        
                        results["transfers"].append({
                            "name_server": ns,
                            "success": True,
                            "records": records
                        })
                        
                        self.console.print(f"✅ Zone transfer successful from {ns}!")
                        self.console.print(f"   Retrieved {len(records)} records")
                        
                        # Display first few records
                        for record in records[:10]:
                            self.console.print(f"   {record['name']} {record['type']} {record['value']}")
                    
                    except Exception as e:
                        results["transfers"].append({
                            "name_server": ns,
                            "success": False,
                            "error": str(e)
                        })
                        self.console.print(f"❌ Zone transfer failed from {ns}: {e}")
            
            except dns.resolver.NXDOMAIN:
                self.console.print(f"[red]Domain {domain} does not exist[/red]")
            except Exception as e:
                self.console.print(f"[red]Error getting NS records: {e}[/red]")
        
        except ImportError:
            self.console.print("[yellow]⚠️ dnspython not installed[/yellow]")
            results["error"] = "dnspython not installed"
        except Exception as e:
            self.console.print(f"[red]DNS zone transfer failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"DNS Zone Transfer - {domain}", results)
        return results
    
    def smb_enumeration(self, target):
        """Enumerate SMB shares and information"""
        self.console.print(f"[bold green]SMB enumeration for: {target}[/bold green]")
        self.console.print("[yellow]⚠️ Only use this against systems you own or have permission to test[/yellow]")
        
        results = {
            "target": target,
            "scan_type": "smb_enumeration",
            "shares": [],
            "info": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Check if SMB port is open
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                smb_result = sock.connect_ex((target, 445))
                
                if smb_result != 0:
                    self.console.print("[red]SMB port 445 is not accessible[/red]")
                    return results
            
            self.console.print("SMB port 445 is open")
            
            # Try to get SMB information using smbclient (if available)
            try:
                # List shares
                cmd = ["smbclient", "-L", target, "-N"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    output = result.stdout
                    
                    # Parse shares
                    lines = output.split('\n')
                    in_shares_section = False
                    
                    for line in lines:
                        if "Sharename" in line and "Type" in line:
                            in_shares_section = True
                            continue
                        
                        if in_shares_section and line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                share_name = parts[0]
                                share_type = parts[1] if len(parts) > 1 else "Unknown"
                                
                                results["shares"].append({
                                    "name": share_name,
                                    "type": share_type,
                                    "accessible": None  # Would need authentication to test
                                })
                                
                                self.console.print(f"📁 Share: {share_name} ({share_type})")
                else:
                    self.console.print(f"[yellow]smbclient command failed: {result.stderr}[/yellow]")
            
            except FileNotFoundError:
                self.console.print("[yellow]⚠️ smbclient not found[/yellow]")
                self.console.print("[blue]ℹ️ Install samba-client for full SMB enumeration[/blue]")
            
            # Basic SMB information gathering
            results["info"]["port_445_open"] = True
            results["info"]["os_detection"] = "SMB service detected"
        
        except Exception as e:
            self.console.print(f"[red]SMB enumeration failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"SMB Enumeration - {target}", results)
        return results
    
    def snmp_enumeration(self, target):
        """Enumerate SNMP information"""
        self.console.print(f"[bold green]SNMP enumeration for: {target}[/bold green]")
        self.console.print("[yellow]⚠️ Only use this against systems you own or have permission to test[/yellow]")
        
        results = {
            "target": target,
            "scan_type": "snmp_enumeration",
            "communities": [],
            "oids": {},
            "scan_date": datetime.now().isoformat()
        }
        
        # Common SNMP community strings
        common_communities = ["public", "private", "community", "manager", "admin"]
        
        try:
            # Check if SNMP port is open
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                try:
                    sock.connect((target, 161))
                    self.console.print("SNMP port 161 is accessible")
                except:
                    self.console.print("[red]SNMP port 161 is not accessible[/red]")
                    return results
            
            # Try to use snmpwalk (if available)  
            for community in common_communities:
                try:
                    cmd = ["snmpwalk", "-v2c", "-c", community, target, "1.3.6.1.2.1.1.1.0"]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        results["communities"].append({
                            "community": community,
                            "access": "read",
                            "response": result.stdout.strip()
                        })
                        
                        self.console.print(f"✅ Community '{community}' - Access granted")
                        self.console.print(f"   System Description: {result.stdout.strip()}")
                        
                        # Try to get more information
                        oids_to_check = {
                            "1.3.6.1.2.1.1.1.0": "System Description",
                            "1.3.6.1.2.1.1.4.0": "System Contact",
                            "1.3.6.1.2.1.1.5.0": "System Name",
                            "1.3.6.1.2.1.1.6.0": "System Location"
                        }
                        
                        for oid, description in oids_to_check.items():
                            try:
                                cmd = ["snmpget", "-v2c", "-c", community, target, oid]
                                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                                
                                if result.returncode == 0:
                                    results["oids"][oid] = {
                                        "description": description,
                                        "value": result.stdout.strip()
                                    }
                                    self.console.print(f"   {description}: {result.stdout.strip()}")
                            except:
                                pass
                    else:
                        self.console.print(f"❌ Community '{community}' - Access denied")
                
                except FileNotFoundError:
                    self.console.print("[yellow]⚠️ SNMP tools not found[/yellow]")
                    self.console.print("[blue]ℹ️ Install snmp-utils for full SNMP enumeration[/blue]")
                    break
                except Exception as e:
                    self.console.print(f"[yellow]Error testing community '{community}': {e}[/yellow]")
        
        except Exception as e:
            self.console.print(f"[red]SNMP enumeration failed: {e}[/red]")
            results["error"] = str(e)
        
        self.save_result(f"SNMP Enumeration - {target}", results)
        return results
    
    def dns_dig_analysis(self, domain):
        """Perform DNS dig analysis"""
        self.console.print(f"[bold green]DNS dig analysis for: {domain}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "dns_dig_analysis",
            "dig_results": {},
            "scan_date": datetime.now().isoformat()
        }
        
        # Common dig queries
        dig_queries = {
            "A": "IPv4 addresses",
            "AAAA": "IPv6 addresses", 
            "MX": "Mail exchange records",
            "NS": "Name servers",
            "TXT": "Text records",
            "CNAME": "Canonical name records",
            "SOA": "Start of authority",
            "ANY": "All available records"
        }
        
        try:
            for record_type, description in dig_queries.items():
                try:
                    # Try using dig command if available
                    cmd = ["dig", "+short", record_type, domain]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        records = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                        results["dig_results"][record_type] = {
                            "description": description,
                            "records": records
                        }
                        
                        self.console.print(f"[cyan]{record_type} ({description}):[/cyan]")
                        for record in records:
                            self.console.print(f"  → {record}")
                    
                except FileNotFoundError:
                    self.console.print("[yellow]⚠️ dig command not found, using basic DNS lookup[/yellow]")
                    # Fall back to basic DNS resolution
                    try:
                        if record_type == "A":
                            ip = socket.gethostbyname(domain)
                            results["dig_results"]["A"] = {
                                "description": "IPv4 addresses",
                                "records": [ip]
                            }
                            self.console.print(f"A (IPv4 addresses): {ip}")
                    except socket.gaierror:
                        pass
                    break
                except subprocess.TimeoutExpired:
                    self.console.print(f"[yellow]Timeout querying {record_type} records[/yellow]")
                except Exception as e:
                    self.console.print(f"[yellow]Error querying {record_type}: {e}[/yellow]")
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]DNS dig analysis interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"DNS Dig Analysis (Interrupted) - {domain}", results)
            return results
        
        self._safe_save_result(f"DNS Dig Analysis - {domain}", results)
        return results
    
    def reverse_dns_lookup(self, ip):
        """Perform reverse DNS lookup"""
        self.console.print(f"[bold green]Reverse DNS lookup for: {ip}[/bold green]")
        
        results = {
            "ip": ip,
            "scan_type": "reverse_dns_lookup",
            "hostnames": [],
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Standard reverse DNS lookup
            try:
                hostname = socket.gethostbyaddr(ip)
                results["hostnames"].append({
                    "hostname": hostname[0],
                    "aliases": hostname[1],
                    "method": "gethostbyaddr"
                })
                self.console.print(f"Hostname: {hostname[0]}")
                if hostname[1]:
                    self.console.print(f"Aliases: {', '.join(hostname[1])}")
            except socket.herror:
                self.console.print("[yellow]No reverse DNS record found[/yellow]")
            
            # Try using dig for PTR records if available
            try:
                # Create PTR record format
                ip_parts = ip.split('.')
                if len(ip_parts) == 4:
                    ptr_domain = f"{ip_parts[3]}.{ip_parts[2]}.{ip_parts[1]}.{ip_parts[0]}.in-addr.arpa"
                    
                    cmd = ["dig", "+short", "PTR", ptr_domain]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        ptr_records = [line.strip().rstrip('.') for line in result.stdout.strip().split('\n') if line.strip()]
                        for ptr in ptr_records:
                            if ptr not in [h["hostname"] for h in results["hostnames"]]:
                                results["hostnames"].append({
                                   
                                    "hostname": ptr,
                                    "aliases": [],
                                    "method": "dig_ptr"
                                })
                                self.console.print(f"PTR Record: {ptr}")
            
            except FileNotFoundError:
                pass  # dig not available
            except Exception as e:
                self.console.print(f"[yellow]PTR lookup error: {e}[/yellow]")
        
        except Exception as e:
            self.console.print(f"[red]Reverse DNS lookup failed: {e}[/red]")
            results["error"] = str(e)
        
        self._safe_save_result(f"Reverse DNS - {ip}", results)
        return results
    
    def dns_cache_snooping(self, dns_server):
        """Perform DNS cache snooping"""
        self.console.print(f"[bold green]DNS cache snooping on: {dns_server}[/bold green]")
        self.console.print("[yellow]⚠️ Only use this against systems you own or have permission to test[/yellow]")
        
        results = {
            "dns_server": dns_server,
            "scan_type": "dns_cache_snooping",
            "cached_domains": [],
            "scan_date": datetime.now().isoformat()
        }
        
        # Common domains to check
        test_domains = [
            "google.com", "facebook.com", "youtube.com", "twitter.com", "amazon.com",
            "microsoft.com", "apple.com", "netflix.com", "linkedin.com", "github.com"
        ]
        
        self.console.print("[blue]ℹ️ This is a basic cache snooping implementation[/blue]")
        self.console.print("[blue]ℹ️ For advanced DNS security testing, use specialized tools[/blue]")
        
        try:
            for domain in test_domains:
                try:
                    # Query the DNS server directly
                    cmd = ["nslookup", domain, dns_server]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                    
                    if result.returncode == 0:
                        # Check response time (cached responses are typically faster)
                        if "Non-authoritative answer" in result.stdout:
                            results["cached_domains"].append({
                                "domain": domain,
                                "status": "potentially_cached",
                                "response": result.stdout
                            })
                            self.console.print(f"[yellow]Potentially cached: {domain}[/yellow]")
                        else:
                            self.console.print(f"[green]Fresh lookup: {domain}[/green]")
                
                except subprocess.TimeoutExpired:
                    self.console.print(f"[red]Timeout querying {domain}[/red]")
                except Exception as e:
                    self.console.print(f"[yellow]Error querying {domain}: {e}[/yellow]")
        
        except FileNotFoundError:
            self.console.print("[yellow]⚠️ nslookup command not found[/yellow]")
        except Exception as e:
            self.console.print(f"[red]DNS cache snooping failed: {e}[/red]")
            results["error"] = str(e)
        
        self._safe_save_result(f"DNS Cache Snooping - {dns_server}", results)
        return results
    
    def dns_bruteforce(self, domain):
        """Brute force DNS subdomains"""
        self.console.print(f"[bold green]DNS brute force for: {domain}[/bold green]")
        self.console.print("[yellow]Press Ctrl+C to stop the scan at any time[/yellow]")
        
        results = {
            "domain": domain,
            "scan_type": "dns_bruteforce",
            "found_subdomains": [],
            "scan_date": datetime.now().isoformat()
        }
        
        # Extended subdomain wordlist for brute forcing
        subdomain_wordlist = [
            "www", "mail", "ftp", "admin", "test", "dev", "staging", "api", "blog", "shop",
            "support", "help", "cdn", "img", "static", "assets", "portal", "secure", "vpn",
            "remote", "mx", "ns", "ns1", "ns2", "dns", "email", "smtp", "pop", "imap",
            "webmail", "autoconfig", "autodiscover", "cpanel", "whm", "plesk", "directadmin",
            "m", "mobile", "wap", "mail2", "pop3", "secure", "ssl", "web", "www2", "news",
            "forum", "forums", "beta", "alpha", "demo", "preview", "app", "apps", "old",
            "new", "v1", "v2", "api2", "api-v1", "api-v2", "test2", "dev2", "staging2"
        ]
        
        self.console.print(f"Brute forcing {len(subdomain_wordlist)} subdomain combinations...")
        
        def check_subdomain_dns(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(full_domain)
                results["found_subdomains"].append({
                    "subdomain": full_domain,
                    "ip": ip,
                    "method": "dns_bruteforce"
                })
                self.console.print(f"✅ {full_domain} → {ip}")
                return True
            except socket.gaierror:
                return False
        
        try:
            # Brute force with threading
            threads = []
            for subdomain in track(subdomain_wordlist, description="Brute forcing subdomains..."):
                thread = threading.Thread(target=check_subdomain_dns, args=(subdomain,))
                thread.start()
                threads.append(thread)
                
                # Limit threads
                if len(threads) >= 15:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]DNS brute force interrupted by user[/yellow]")
            if Confirm.ask("Do you want to save partial results?"):
                self._safe_save_result(f"DNS Brute Force (Interrupted) - {domain}", results)
            return results
        
        self.console.print(f"\nBrute force complete: Found {len(results['found_subdomains'])} subdomains")
        self._safe_save_result(f"DNS Brute Force - {domain}", results)
        return results
    
    def mx_record_analysis(self, domain):
        """Analyze MX records for a domain"""
        self.console.print(f"[bold green]MX record analysis for: {domain}[/bold green]")
        
        results = {
            "domain": domain,
            "scan_type": "mx_record_analysis",
            "mx_records": [],
            "analysis": {},
            "scan_date": datetime.now().isoformat()
        }
        
        try:
            # Try using dig for MX records
            try:
                cmd = ["dig", "+short", "MX", domain]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    mx_lines = result.stdout.strip().split('\n')
                    for line in mx_lines:
                        if line.strip():
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                priority = parts[0]
                                server = parts[1].rstrip('.')
                                
                                # Get IP for MX server
                                try:
                                    ip = socket.gethostbyname(server)
                                    results["mx_records"].append({
                                        "priority": int(priority),
                                        "server": server,
                                        "ip": ip
                                    })
                                    self.console.print(f"Priority {priority}: {server} ({ip})")
                                except socket.gaierror:
                                    results["mx_records"].append({
                                        "priority": int(priority),
                                        "server": server,
                                        "ip": "N/A"
                                    })
                                    self.console.print(f"Priority {priority}: {server} (IP not resolved)")
            
            except FileNotFoundError:
                self.console.print("[yellow]⚠️ dig command not found, using basic lookup[/yellow]")
                # Fallback to basic MX lookup using socket
                try:
                    import dns.resolver
                    answers = dns.resolver.resolve(domain, 'MX')
                    for answer in answers:
                        server = str(answer.exchange).rstrip('.')
                        priority = answer.preference
                        try:
                            ip = socket.gethostbyname(server)
                            results["mx_records"].append({
                                "priority": priority,
                                "server": server,
                                "ip": ip
                            })
                            self.console.print(f"Priority {priority}: {server} ({ip})")
                        except socket.gaierror:
                            results["mx_records"].append({
                                "priority": priority,
                                "server": server,
                                "ip": "N/A"
                            })
                            self.console.print(f"Priority {priority}: {server} (IP not resolved)")
                
                except ImportError:
                    self.console.print("[yellow]⚠️ DNS tools not available for MX lookup[/yellow]")
            
            # Analyze MX records
            if results["mx_records"]:
                # Sort by priority
                results["mx_records"].sort(key=lambda x: x["priority"])
                
                # Analysis
                results["analysis"]["total_mx_servers"] = len(results["mx_records"])
                results["analysis"]["primary_mx"] = results["mx_records"][0]["server"]
                results["analysis"]["backup_mx_count"] = len(results["mx_records"]) - 1
                
                # Check for common mail providers
                common_providers = {
                    "google": ["gmail", "googlemail", "aspmx"],
                    "microsoft": ["outlook", "hotmail", "live", "office365"],
                    "yahoo": ["yahoo", "yahoodns"],
                    "cloudflare": ["cloudflare"],
                    "protonmail": ["protonmail"]
                }
                
                detected_providers = []
                for mx in results["mx_records"]:
                    server_lower = mx["server"].lower()
                    for provider, keywords in common_providers.items():
                        if any(keyword in server_lower for keyword in keywords):
                            if provider not in detected_providers:
                                detected_providers.append(provider)
                
                results["analysis"]["detected_providers"] = detected_providers
                
                # Display analysis
                self.console.print(f"\n[bold cyan]MX Analysis:[/bold cyan]")
                self.console.print(f"Total MX servers: {results['analysis']['total_mx_servers']}")
                self.console.print(f"Primary MX: {results['analysis']['primary_mx']}")
                if detected_providers:
                    self.console.print(f"Detected providers: {', '.join(detected_providers)}")
            
            else:
                self.console.print("[yellow]No MX records found[/yellow]")
        
        except Exception as e:
            self.console.print(f"[red]MX record analysis failed: {e}[/red]")
            results["error"] = str(e)
        
        self._safe_save_result(f"MX Record Analysis - {domain}", results)
        return results
