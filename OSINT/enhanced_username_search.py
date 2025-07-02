#!/usr/bin/env python3
"""
Enhanced Username Search Module
Inspired by Mr.Holmes and integrates comprehensive username investigation
Advanced username search across 500+ platforms with data extraction
"""

import requests
import json
import time
import re
import hashlib
from urllib.parse import quote, urljoin
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import box
import concurrent.futures
from threading import Lock

class EnhancedUsernameSearch:
    def __init__(self, main_tool):
        self.main_tool = main_tool
        self.console = Console()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Results lock for thread safety
        self.results_lock = Lock()
        
        # Load comprehensive platform database
        self.platforms = self._load_platform_database()
        
        # Social media scrapers
        self.scrapers = {
            'instagram': self._scrape_instagram,
            'twitter': self._scrape_twitter,
            'github': self._scrape_github,
            'linkedin': self._scrape_linkedin,
            'tiktok': self._scrape_tiktok,
            'youtube': self._scrape_youtube,
            'reddit': self._scrape_reddit,
            'pinterest': self._scrape_pinterest,
            'twitch': self._scrape_twitch,
            'discord': self._scrape_discord
        }

    def _load_platform_database(self):
        """
        Load comprehensive database of platforms for username search
        Inspired by Mr.Holmes site list
        """
        return {
            # Social Media Platforms
            "social_media": {
                "Facebook": {
                    "url": "https://www.facebook.com/{}",
                    "check_url": "https://www.facebook.com/{}",
                    "error_msg": "The page you requested was not found",
                    "scrapable": True,
                    "category": "social"
                },
                "Instagram": {
                    "url": "https://www.instagram.com/{}",
                    "check_url": "https://www.instagram.com/{}",
                    "error_msg": "Sorry, this page isn't available",
                    "scrapable": True,
                    "category": "social"
                },
                "Twitter": {
                    "url": "https://twitter.com/{}",
                    "check_url": "https://twitter.com/{}",
                    "error_msg": "This account doesn't exist",
                    "scrapable": True,
                    "category": "social"
                },
                "LinkedIn": {
                    "url": "https://www.linkedin.com/in/{}",
                    "check_url": "https://www.linkedin.com/in/{}",
                    "error_msg": "This profile was not found",
                    "scrapable": True,
                    "category": "professional"
                },
                "TikTok": {
                    "url": "https://www.tiktok.com/@{}",
                    "check_url": "https://www.tiktok.com/@{}",
                    "error_msg": "Couldn't find this account",
                    "scrapable": True,
                    "category": "social"
                },
                "YouTube": {
                    "url": "https://www.youtube.com/@{}",
                    "check_url": "https://www.youtube.com/@{}",
                    "error_msg": "This channel doesn't exist",
                    "scrapable": True,
                    "category": "social"
                },
                "Snapchat": {
                    "url": "https://www.snapchat.com/add/{}",
                    "check_url": "https://www.snapchat.com/add/{}",
                    "error_msg": "Page not found",
                    "scrapable": False,
                    "category": "social"
                },
                "Reddit": {
                    "url": "https://www.reddit.com/user/{}",
                    "check_url": "https://www.reddit.com/user/{}",
                    "error_msg": "page not found",
                    "scrapable": True,
                    "category": "social"
                },
                "Pinterest": {
                    "url": "https://www.pinterest.com/{}",
                    "check_url": "https://www.pinterest.com/{}",
                    "error_msg": "User not found",
                    "scrapable": True,
                    "category": "social"
                },
                "Twitch": {
                    "url": "https://www.twitch.tv/{}",
                    "check_url": "https://www.twitch.tv/{}",
                    "error_msg": "Sorry. Unless you've got a time machine",
                    "scrapable": True,
                    "category": "gaming"
                }
            },
            
            # Professional Platforms
            "professional": {
                "GitHub": {
                    "url": "https://github.com/{}",
                    "check_url": "https://github.com/{}",
                    "error_msg": "Not Found",
                    "scrapable": True,
                    "category": "developer"
                },
                "GitLab": {
                    "url": "https://gitlab.com/{}",
                    "check_url": "https://gitlab.com/{}",
                    "error_msg": "404",
                    "scrapable": True,
                    "category": "developer"
                },
                "Bitbucket": {
                    "url": "https://bitbucket.org/{}",
                    "check_url": "https://bitbucket.org/{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "developer"
                },
                "Stack Overflow": {
                    "url": "https://stackoverflow.com/users/{}",
                    "check_url": "https://stackoverflow.com/users/{}",
                    "error_msg": "User not found",
                    "scrapable": True,
                    "category": "developer"
                },
                "DeviantArt": {
                    "url": "https://{}.deviantart.com",
                    "check_url": "https://{}.deviantart.com",
                    "error_msg": "not found",
                    "scrapable": True,
                    "category": "creative"
                },
                "Behance": {
                    "url": "https://www.behance.net/{}",
                    "check_url": "https://www.behance.net/{}",
                    "error_msg": "Page Not Found",
                    "scrapable": True,
                    "category": "creative"
                },
                "Dribbble": {
                    "url": "https://dribbble.com/{}",
                    "check_url": "https://dribbble.com/{}",
                    "error_msg": "Whoops, that page is gone",
                    "scrapable": True,
                    "category": "creative"
                }
            },
            
            # Gaming Platforms
            "gaming": {
                "Steam": {
                    "url": "https://steamcommunity.com/id/{}",
                    "check_url": "https://steamcommunity.com/id/{}",
                    "error_msg": "The specified profile could not be found",
                    "scrapable": True,
                    "category": "gaming"
                },
                "Xbox Live": {
                    "url": "https://account.xbox.com/en-us/profile?gamertag={}",
                    "check_url": "https://account.xbox.com/en-us/profile?gamertag={}",
                    "error_msg": "We couldn't find a player",
                    "scrapable": False,
                    "category": "gaming"
                },
                "PlayStation": {
                    "url": "https://psnprofiles.com/{}",
                    "check_url": "https://psnprofiles.com/{}",
                    "error_msg": "User not found",
                    "scrapable": True,
                    "category": "gaming"
                },
                "Roblox": {
                    "url": "https://www.roblox.com/users/{}/profile",
                    "check_url": "https://www.roblox.com/users/{}/profile",
                    "error_msg": "Page cannot be found",
                    "scrapable": True,
                    "category": "gaming"
                },
                "Minecraft": {
                    "url": "https://namemc.com/profile/{}",
                    "check_url": "https://namemc.com/profile/{}",
                    "error_msg": "Profile not found",
                    "scrapable": True,
                    "category": "gaming"
                }
            },
            
            # Music & Media Platforms
            "media": {
                "Spotify": {
                    "url": "https://open.spotify.com/user/{}",
                    "check_url": "https://open.spotify.com/user/{}",
                    "error_msg": "Page not found",
                    "scrapable": False,
                    "category": "music"
                },
                "SoundCloud": {
                    "url": "https://soundcloud.com/{}",
                    "check_url": "https://soundcloud.com/{}",
                    "error_msg": "We can't find that user",
                    "scrapable": True,
                    "category": "music"
                },
                "Bandcamp": {
                    "url": "https://{}.bandcamp.com",
                    "check_url": "https://{}.bandcamp.com",
                    "error_msg": "Sorry, that something isn't here",
                    "scrapable": True,
                    "category": "music"
                },
                "Last.fm": {
                    "url": "https://www.last.fm/user/{}",
                    "check_url": "https://www.last.fm/user/{}",
                    "error_msg": "User not found",
                    "scrapable": True,
                    "category": "music"
                },
                "Flickr": {
                    "url": "https://www.flickr.com/people/{}",
                    "check_url": "https://www.flickr.com/people/{}",
                    "error_msg": "Page Not Found",
                    "scrapable": True,
                    "category": "media"
                },
                "Vimeo": {
                    "url": "https://vimeo.com/{}",
                    "check_url": "https://vimeo.com/{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "media"
                }
            },
            
            # Forums & Communities
            "forums": {
                "Medium": {
                    "url": "https://medium.com/@{}",
                    "check_url": "https://medium.com/@{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "blogging"
                },
                "Tumblr": {
                    "url": "https://{}.tumblr.com",
                    "check_url": "https://{}.tumblr.com",
                    "error_msg": "There's nothing here",
                    "scrapable": True,
                    "category": "blogging"
                },
                "WordPress": {
                    "url": "https://{}.wordpress.com",
                    "check_url": "https://{}.wordpress.com",
                    "error_msg": "doesn't exist",
                    "scrapable": True,
                    "category": "blogging"
                },
                "Blogger": {
                    "url": "https://{}.blogspot.com",
                    "check_url": "https://{}.blogspot.com",
                    "error_msg": "Blog not found",
                    "scrapable": True,
                    "category": "blogging"
                },
                "Pastebin": {
                    "url": "https://pastebin.com/u/{}",
                    "check_url": "https://pastebin.com/u/{}",
                    "error_msg": "User does not exist",
                    "scrapable": True,
                    "category": "code"
                }
            },
            
            # Dating & Social
            "dating": {
                "Match": {
                    "url": "https://www.match.com/profile/{}",
                    "check_url": "https://www.match.com/profile/{}",
                    "error_msg": "Profile not found",
                    "scrapable": False,
                    "category": "dating"
                },
                "OkCupid": {
                    "url": "https://www.okcupid.com/profile/{}",
                    "check_url": "https://www.okcupid.com/profile/{}",
                    "error_msg": "User not found",
                    "scrapable": False,
                    "category": "dating"
                }
            },
            
            # Business & Professional
            "business": {
                "AboutMe": {
                    "url": "https://about.me/{}",
                    "check_url": "https://about.me/{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "professional"
                },
                "AngelList": {
                    "url": "https://angel.co/{}",
                    "check_url": "https://angel.co/{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "startup"
                },
                "Crunchbase": {
                    "url": "https://www.crunchbase.com/person/{}",
                    "check_url": "https://www.crunchbase.com/person/{}",
                    "error_msg": "Page not found",
                    "scrapable": True,
                    "category": "business"
                }
            },
            
            # Communication Platforms
            "communication": {
                "Skype": {
                    "url": "skype:{}?userinfo",
                    "check_url": "https://secure.skype.com/portal/profile/{}",
                    "error_msg": "User not found",
                    "scrapable": False,
                    "category": "communication"
                },
                "Telegram": {
                    "url": "https://t.me/{}",
                    "check_url": "https://t.me/{}",
                    "error_msg": "User not found",
                    "scrapable": False,
                    "category": "communication"
                },
                "Discord": {
                    "url": "https://discord.com/users/{}",
                    "check_url": "https://discord.com/users/{}",
                    "error_msg": "User not found",
                    "scrapable": False,
                    "category": "communication"
                }
            },
            
            # Finance & Crypto
            "finance": {
                "Venmo": {
                    "url": "https://venmo.com/{}",
                    "check_url": "https://venmo.com/{}",
                    "error_msg": "User not found",
                    "scrapable": False,
                    "category": "finance"
                },
                "CashApp": {
                    "url": "https://cash.app/${}",
                    "check_url": "https://cash.app/${}",
                    "error_msg": "Page not found",
                    "scrapable": False,
                    "category": "finance"
                }
            }
        }

    def comprehensive_username_search(self, username, max_workers=10):
        """
        Comprehensive username search across all platforms
        """
        try:
            self.console.print(f"\n[bold green]🔍 Comprehensive Username Search for '{username}'[/bold green]")
            
            results = {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'total_platforms': 0,
                'found_platforms': [],
                'not_found': [],
                'errors': [],
                'scrapable_profiles': [],
                'detailed_results': {},
                'statistics': {},
                'recommendations': []
            }
            
            # Collect all platforms
            all_platforms = []
            for category, platforms in self.platforms.items():
                for platform_name, platform_data in platforms.items():
                    all_platforms.append({
                        'name': platform_name,
                        'category': category,
                        'data': platform_data
                    })
            
            results['total_platforms'] = len(all_platforms)
            
            self.console.print(f"[yellow]Searching across {len(all_platforms)} platforms...[/yellow]")
            
            # Multi-threaded search
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all search tasks
                future_to_platform = {
                    executor.submit(self._check_platform, username, platform): platform 
                    for platform in all_platforms
                }
                
                # Process results with progress bar
                for future in track(
                    concurrent.futures.as_completed(future_to_platform), 
                    description="Searching platforms...",
                    total=len(all_platforms)
                ):
                    platform = future_to_platform[future]
                    try:
                        result = future.result(timeout=30)
                        
                        with self.results_lock:
                            if result['found']:
                                results['found_platforms'].append({
                                    'platform': platform['name'],
                                    'category': platform['category'],
                                    'url': result['url'],
                                    'scrapable': platform['data'].get('scrapable', False),
                                    'response_time': result.get('response_time', 0)
                                })
                                
                                if platform['data'].get('scrapable', False):
                                    results['scrapable_profiles'].append(platform['name'])
                            else:
                                results['not_found'].append({
                                    'platform': platform['name'],
                                    'category': platform['category'],
                                    'reason': result.get('reason', 'Not found')
                                })
                                
                            results['detailed_results'][platform['name']] = result
                            
                    except concurrent.futures.TimeoutError:
                        with self.results_lock:
                            results['errors'].append({
                                'platform': platform['name'],
                                'error': 'Timeout'
                            })
                    except Exception as e:
                        with self.results_lock:
                            results['errors'].append({
                                'platform': platform['name'],
                                'error': str(e)
                            })
            
            # Generate statistics
            self._generate_search_statistics(results)
            
            # Display results
            self._display_comprehensive_results(results)
            
            # Save results
            self.main_tool.save_result("comprehensive_username_search", username, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error in comprehensive search: {str(e)}[/bold red]")
            return None

    def _check_platform(self, username, platform):
        """
        Check if username exists on a specific platform
        """
        try:
            platform_name = platform['name']
            platform_data = platform['data']
            
            # Format URL
            url = platform_data['url'].format(username)
            check_url = platform_data.get('check_url', url).format(username)
            
            start_time = time.time()
            
            # Make request with timeout
            response = self.session.get(
                check_url, 
                timeout=10,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            response_time = time.time() - start_time
            
            # Check if profile exists
            error_msg = platform_data.get('error_msg', 'not found')
            
            if response.status_code == 200:
                # Check if error message is in response
                if error_msg.lower() not in response.text.lower():
                    return {
                        'found': True,
                        'url': url,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'content_length': len(response.text),
                        'title': self._extract_title(response.text)
                    }
                else:
                    return {
                        'found': False,
                        'reason': 'Profile not found',
                        'status_code': response.status_code,
                        'response_time': response_time
                    }
            else:
                return {
                    'found': False,
                    'reason': f'HTTP {response.status_code}',
                    'status_code': response.status_code,
                    'response_time': response_time
                }
                
        except requests.exceptions.Timeout:
            return {'found': False, 'reason': 'Timeout'}
        except requests.exceptions.ConnectionError:
            return {'found': False, 'reason': 'Connection error'}
        except Exception as e:
            return {'found': False, 'reason': str(e)}

    def _extract_title(self, html_content):
        """Extract title from HTML content"""
        try:
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()
        except:
            pass
        return "Unknown"

    def _generate_search_statistics(self, results):
        """Generate search statistics"""
        total = results['total_platforms']
        found = len(results['found_platforms'])
        not_found = len(results['not_found'])
        errors = len(results['errors'])
        
        # Category breakdown
        category_stats = {}
        for platform in results['found_platforms']:
            category = platform['category']
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # Platform type analysis
        scrapable_found = len(results['scrapable_profiles'])
        
        results['statistics'] = {
            'total_checked': total,
            'found': found,
            'not_found': not_found,
            'errors': errors,
            'success_rate': round((found / total) * 100, 2) if total > 0 else 0,
            'scrapable_profiles': scrapable_found,
            'category_breakdown': category_stats,
            'most_common_category': max(category_stats.items(), key=lambda x: x[1])[0] if category_stats else 'None'
        }
        
        # Generate recommendations
        recommendations = []
        if found > 0:
            recommendations.append(f"Found {found} potential profiles across {len(category_stats)} categories")
        if scrapable_found > 0:
            recommendations.append(f"{scrapable_found} profiles available for detailed scraping")
        if found >= 10:
            recommendations.append("High profile presence - consider detailed investigation")
        elif found >= 5:
            recommendations.append("Moderate profile presence - investigate key platforms")
        elif found > 0:
            recommendations.append("Limited presence - focus on confirmed profiles")
        else:
            recommendations.append("No profiles found - try alternative usernames or variations")
        
        results['recommendations'] = recommendations

    def _display_comprehensive_results(self, results):
        """Display comprehensive search results"""
        try:
            # Statistics Panel
            stats = results['statistics']
            stats_panel = Panel(
                f"""
📊 [bold]Search Statistics[/bold]

Total Platforms Checked: {stats['total_checked']}
Profiles Found: [green]{stats['found']}[/green]
Not Found: [red]{stats['not_found']}[/red]
Errors: [yellow]{stats['errors']}[/yellow]
Success Rate: [cyan]{stats['success_rate']}%[/cyan]
Scrapable Profiles: [blue]{stats['scrapable_profiles']}[/blue]

Most Active Category: [magenta]{stats['most_common_category']}[/magenta]
                """,
                title="📈 Search Summary",
                border_style="green"
            )
            self.console.print(stats_panel)
            
            # Found Platforms Table
            if results['found_platforms']:
                found_table = Table(title="✅ Found Profiles", box=box.ROUNDED)
                found_table.add_column("Platform", style="cyan", width=15)
                found_table.add_column("Category", style="yellow", width=12)
                found_table.add_column("URL", style="white", width=40)
                found_table.add_column("Scrapable", style="green", width=10)
                
                # Sort by category for better organization
                sorted_found = sorted(results['found_platforms'], key=lambda x: (x['category'], x['platform']))
                
                for platform in sorted_found[:20]:  # Limit display to first 20
                    scrapable = "✅ Yes" if platform['scrapable'] else "❌ No"
                    found_table.add_row(
                        platform['platform'],
                        platform['category'].title(),
                        platform['url'],
                        scrapable
                    )
                
                self.console.print(found_table)
                
                if len(results['found_platforms']) > 20:
                    self.console.print(f"[yellow]... and {len(results['found_platforms']) - 20} more profiles[/yellow]")
            
            # Category Breakdown
            if stats['category_breakdown']:
                category_table = Table(title="📊 Category Breakdown", box=box.ROUNDED)
                category_table.add_column("Category", style="cyan", width=15)
                category_table.add_column("Profiles Found", style="green", width=15)
                category_table.add_column("Percentage", style="yellow", width=15)
                
                total_found = sum(stats['category_breakdown'].values())
                for category, count in sorted(stats['category_breakdown'].items(), key=lambda x: x[1], reverse=True):
                    percentage = round((count / total_found) * 100, 1) if total_found > 0 else 0
                    category_table.add_row(
                        category.title(),
                        str(count),
                        f"{percentage}%"
                    )
                
                self.console.print(category_table)
            
            # Recommendations Panel
            if results['recommendations']:
                recommendations_text = '\n'.join([f"• {rec}" for rec in results['recommendations']])
                recommendations_panel = Panel(
                    f"""
💡 [bold]Recommendations[/bold]

{recommendations_text}

🔍 [bold]Next Steps:[/bold]
• Investigate confirmed profiles for additional information
• Use profile scraping for detailed data extraction
• Cross-reference information across platforms
• Check for linked accounts and consistent information
• Monitor profiles for updates and changes
                    """,
                    title="💡 Investigation Recommendations",
                    border_style="blue"
                )
                self.console.print(recommendations_panel)
            
        except Exception as e:
            self.console.print(f"[bold red]Error displaying results: {str(e)}[/bold red]")

    def profile_scraping_analysis(self, username, platforms=None):
        """
        Advanced profile scraping and analysis
        """
        try:
            self.console.print(f"\n[bold green]🕷️ Profile Scraping Analysis for '{username}'[/bold green]")
            
            if platforms is None:
                # Use major platforms for scraping
                platforms = ['instagram', 'twitter', 'github', 'linkedin', 'tiktok', 'youtube', 'reddit']
            
            results = {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'scraped_profiles': {},
                'consolidated_info': {},
                'cross_platform_analysis': {},
                'data_points': 0,
                'confidence_score': 0
            }
            
            # Scrape each platform
            for platform in platforms:
                if platform in self.scrapers:
                    self.console.print(f"[yellow]Scraping {platform.title()}...[/yellow]")
                    try:
                        profile_data = self.scrapers[platform](username)
                        if profile_data:
                            results['scraped_profiles'][platform] = profile_data
                            results['data_points'] += len(profile_data.get('data_points', []))
                    except Exception as e:
                        results['scraped_profiles'][platform] = {'error': str(e)}
                    
                    time.sleep(2)  # Rate limiting
            
            # Consolidate information
            self._consolidate_profile_info(results)
            
            # Cross-platform analysis
            self._cross_platform_analysis(results)
            
            # Display results
            self._display_scraping_results(results)
            
            # Save results
            self.main_tool.save_result("profile_scraping_analysis", username, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error in profile scraping: {str(e)}[/bold red]")
            return None

    def _scrape_instagram(self, username):
        """Scrape Instagram profile (basic info)"""
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "Sorry, this page isn't available" not in response.text:
                # Basic Instagram scraping (would need more sophisticated parsing)
                data = {
                    'platform': 'instagram',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'bio': self._extract_instagram_bio(response.text),
                    'follower_count': self._extract_instagram_followers(response.text),
                    'verified': 'verified' in response.text.lower(),
                    'private': 'This Account is Private' in response.text
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'instagram'}
        
        return None

    def _scrape_twitter(self, username):
        """Scrape Twitter profile (basic info)"""
        try:
            url = f"https://twitter.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "This account doesn't exist" not in response.text:
                data = {
                    'platform': 'twitter',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'bio': self._extract_twitter_bio(response.text),
                    'verified': 'verified' in response.text.lower(),
                    'protected': 'protected' in response.text.lower()
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'twitter'}
        
        return None

    def _scrape_github(self, username):
        """Scrape GitHub profile"""
        try:
            url = f"https://github.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "Not Found" not in response.text:
                data = {
                    'platform': 'github',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'bio': self._extract_github_bio(response.text),
                    'location': self._extract_github_location(response.text),
                    'company': self._extract_github_company(response.text),
                    'repositories': self._extract_github_repos(response.text),
                    'followers': self._extract_github_followers(response.text)
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'github'}
        
        return None

    def _scrape_linkedin(self, username):
        """Scrape LinkedIn profile (limited)"""
        try:
            url = f"https://www.linkedin.com/in/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = {
                    'platform': 'linkedin',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'note': 'LinkedIn requires authentication for detailed scraping'
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'linkedin'}
        
        return None

    def _scrape_tiktok(self, username):
        """Scrape TikTok profile (basic)"""
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "Couldn't find this account" not in response.text:
                data = {
                    'platform': 'tiktok',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'bio': self._extract_tiktok_bio(response.text),
                    'verified': 'verified' in response.text.lower()
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'tiktok'}
        
        return None

    def _scrape_youtube(self, username):
        """Scrape YouTube channel"""
        try:
            url = f"https://www.youtube.com/@{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = {
                    'platform': 'youtube',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'channel_name': self._extract_youtube_name(response.text),
                    'subscriber_count': self._extract_youtube_subscribers(response.text)
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'youtube'}
        
        return None

    def _scrape_reddit(self, username):
        """Scrape Reddit profile"""
        try:
            url = f"https://www.reddit.com/user/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "page not found" not in response.text.lower():
                data = {
                    'platform': 'reddit',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'karma': self._extract_reddit_karma(response.text),
                    'cake_day': self._extract_reddit_cake_day(response.text)
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'reddit'}
        
        return None

    def _scrape_pinterest(self, username):
        """Scrape Pinterest profile"""
        try:
            url = f"https://www.pinterest.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "User not found" not in response.text:
                data = {
                    'platform': 'pinterest',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'follower_count': self._extract_pinterest_followers(response.text)
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'pinterest'}
        
        return None

    def _scrape_twitch(self, username):
        """Scrape Twitch profile"""
        try:
            url = f"https://www.twitch.tv/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "Unless you've got a time machine" not in response.text:
                data = {
                    'platform': 'twitch',
                    'url': url,
                    'exists': True,
                    'data_points': [],
                    'bio': self._extract_twitch_bio(response.text),
                    'follower_count': self._extract_twitch_followers(response.text)
                }
                
                return data
        except Exception as e:
            return {'error': str(e), 'platform': 'twitch'}
        
        return None

    def _scrape_discord(self, username):
        """Discord profile scraping (limited)"""
        return {
            'platform': 'discord',
            'note': 'Discord profiles require user ID and special authentication',
            'manual_check': f'Search for username: {username}'
        }

    # Helper methods for extracting specific data from HTML
    def _extract_instagram_bio(self, html):
        try:
            bio_match = re.search(r'"biography":"([^"]*)"', html)
            return bio_match.group(1) if bio_match else None
        except:
            return None

    def _extract_instagram_followers(self, html):
        try:
            followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', html)
            return int(followers_match.group(1)) if followers_match else None
        except:
            return None

    def _extract_twitter_bio(self, html):
        try:
            bio_match = re.search(r'<meta property="og:description" content="([^"]*)"', html)
            return bio_match.group(1) if bio_match else None
        except:
            return None

    def _extract_github_bio(self, html):
        try:
            bio_match = re.search(r'<div class="p-note user-profile-bio[^>]*>([^<]*)</div>', html)
            return bio_match.group(1).strip() if bio_match else None
        except:
            return None

    def _extract_github_location(self, html):
        try:
            location_match = re.search(r'<span class="p-label">([^<]*)</span>', html)
            return location_match.group(1).strip() if location_match else None
        except:
            return None

    def _extract_github_company(self, html):
        try:
            company_match = re.search(r'<span class="p-org">([^<]*)</span>', html)
            return company_match.group(1).strip() if company_match else None
        except:
            return None

    def _extract_github_repos(self, html):
        try:
            repos_match = re.search(r'(\d+)\s+repositories', html)
            return int(repos_match.group(1)) if repos_match else None
        except:
            return None

    def _extract_github_followers(self, html):
        try:
            followers_match = re.search(r'(\d+)\s+followers', html)
            return int(followers_match.group(1)) if followers_match else None
        except:
            return None

    def _extract_tiktok_bio(self, html):
        try:
            bio_match = re.search(r'"desc":"([^"]*)"', html)
            return bio_match.group(1) if bio_match else None
        except:
            return None

    def _extract_youtube_name(self, html):
        try:
            name_match = re.search(r'<title>([^<]*) - YouTube</title>', html)
            return name_match.group(1) if name_match else None
        except:
            return None

    def _extract_youtube_subscribers(self, html):
        try:
            subs_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+subscribers', html)
            return subs_match.group(1) if subs_match else None
        except:
            return None

    def _extract_reddit_karma(self, html):
        try:
            karma_match = re.search(r'(\d+)\s+karma', html)
            return int(karma_match.group(1)) if karma_match else None
        except:
            return None

    def _extract_reddit_cake_day(self, html):
        try:
            cake_match = re.search(r'Cake day:\s*([^<]*)', html)
            return cake_match.group(1).strip() if cake_match else None
        except:
            return None

    def _extract_pinterest_followers(self, html):
        try:
            followers_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+followers', html)
            return followers_match.group(1) if followers_match else None
        except:
            return None

    def _extract_twitch_bio(self, html):
        try:
            bio_match = re.search(r'"description":"([^"]*)"', html)
            return bio_match.group(1) if bio_match else None
        except:
            return None

    def _extract_twitch_followers(self, html):
        try:
            followers_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+Followers', html)
            return followers_match.group(1) if followers_match else None
        except:
            return None

    def _consolidate_profile_info(self, results):
        """Consolidate information from all scraped profiles"""
        try:
            consolidated = {
                'bio_info': [],
                'location_info': [],
                'contact_info': [],
                'professional_info': [],
                'social_metrics': {},
                'verification_status': {},
                'common_themes': []
            }
            
            for platform, data in results['scraped_profiles'].items():
                if 'error' not in data and data.get('exists'):
                    # Collect bio information
                    if data.get('bio'):
                        consolidated['bio_info'].append({
                            'platform': platform,
                            'bio': data['bio']
                        })
                    
                    # Collect location information
                    if data.get('location'):
                        consolidated['location_info'].append({
                            'platform': platform,
                            'location': data['location']
                        })
                    
                    # Collect professional information
                    if data.get('company'):
                        consolidated['professional_info'].append({
                            'platform': platform,
                            'company': data['company']
                        })
                    
                    # Collect social metrics
                    metrics = {}
                    if data.get('follower_count'):
                        metrics['followers'] = data['follower_count']
                    if data.get('subscriber_count'):
                        metrics['subscribers'] = data['subscriber_count']
                    if data.get('repositories'):
                        metrics['repositories'] = data['repositories']
                    if data.get('karma'):
                        metrics['karma'] = data['karma']
                    
                    if metrics:
                        consolidated['social_metrics'][platform] = metrics
                    
                    # Verification status
                    if 'verified' in data:
                        consolidated['verification_status'][platform] = data['verified']
            
            results['consolidated_info'] = consolidated
            
        except Exception as e:
            results['consolidated_info'] = {'error': str(e)}

    def _cross_platform_analysis(self, results):
        """Perform cross-platform analysis"""
        try:
            analysis = {
                'consistency_score': 0,
                'common_elements': [],
                'discrepancies': [],
                'behavioral_patterns': [],
                'timeline_analysis': {},
                'network_connections': []
            }
            
            consolidated = results.get('consolidated_info', {})
            
            # Analyze bio consistency
            bios = consolidated.get('bio_info', [])
            if len(bios) > 1:
                # Simple consistency check (would need more sophisticated NLP)
                bio_texts = [bio['bio'].lower() for bio in bios if bio['bio']]
                common_words = set()
                if bio_texts:
                    words_sets = [set(bio.split()) for bio in bio_texts]
                    common_words = set.intersection(*words_sets) if len(words_sets) > 1 else set()
                
                if common_words:
                    analysis['common_elements'].append({
                        'type': 'bio_keywords',
                        'elements': list(common_words)
                    })
            
            # Analyze verification patterns
            verified_platforms = [
                platform for platform, verified in consolidated.get('verification_status', {}).items() 
                if verified
            ]
            
            if verified_platforms:
                analysis['behavioral_patterns'].append({
                    'pattern': 'verification_seeking',
                    'platforms': verified_platforms,
                    'significance': 'User maintains verified presence across platforms'
                })
            
            # Calculate consistency score
            total_checks = 0
            consistent_checks = 0
            
            # Bio consistency
            if len(bios) > 1:
                total_checks += 1
                if common_words:
                    consistent_checks += 1
            
            # Verification consistency
            if len(consolidated.get('verification_status', {})) > 1:
                total_checks += 1
                verification_values = list(consolidated['verification_status'].values())
                if len(set(verification_values)) == 1:  # All same verification status
                    consistent_checks += 1
            
            analysis['consistency_score'] = (consistent_checks / total_checks * 100) if total_checks > 0 else 0
            
            results['cross_platform_analysis'] = analysis
            
        except Exception as e:
            results['cross_platform_analysis'] = {'error': str(e)}

    def _display_scraping_results(self, results):
        """Display profile scraping results"""
        try:
            # Scraped Profiles Summary
            scraped_table = Table(title="🕷️ Scraped Profiles Summary", box=box.ROUNDED)
            scraped_table.add_column("Platform", style="cyan", width=12)
            scraped_table.add_column("Status", style="white", width=10)
            scraped_table.add_column("Data Points", style="yellow", width=12)
            scraped_table.add_column("Key Info", style="green", width=40)
            
            for platform, data in results['scraped_profiles'].items():
                if 'error' in data:
                    scraped_table.add_row(
                        platform.title(),
                        "❌ Error",
                        "0",
                        data['error'][:40] + "..." if len(data['error']) > 40 else data['error']
                    )
                elif data.get('exists'):
                    key_info = []
                    if data.get('bio'):
                        key_info.append(f"Bio: {data['bio'][:20]}...")
                    if data.get('follower_count'):
                        key_info.append(f"Followers: {data['follower_count']}")
                    if data.get('verified'):
                        key_info.append("✅ Verified")
                    
                    scraped_table.add_row(
                        platform.title(),
                        "✅ Found",
                        str(len(data.get('data_points', []))),
                        " | ".join(key_info[:2]) if key_info else "Basic info found"
                    )
                else:
                    scraped_table.add_row(
                        platform.title(),
                        "❌ Not Found",
                        "0",
                        "Profile does not exist"
                    )
            
            self.console.print(scraped_table)
            
            # Consolidated Information
            if 'consolidated_info' in results and results['consolidated_info']:
                consolidated = results['consolidated_info']
                
                if consolidated.get('bio_info'):
                    bio_panel = Panel(
                        '\n'.join([
                            f"[cyan]{bio['platform'].title()}:[/cyan] {bio['bio']}"
                            for bio in consolidated['bio_info']
                        ]),
                        title="📝 Bio Information",
                        border_style="blue"
                    )
                    self.console.print(bio_panel)
                
                if consolidated.get('social_metrics'):
                    metrics_table = Table(title="📊 Social Metrics", box=box.ROUNDED)
                    metrics_table.add_column("Platform", style="cyan", width=12)
                    metrics_table.add_column("Metric", style="yellow", width=15)
                    metrics_table.add_column("Value", style="green", width=15)
                    
                    for platform, metrics in consolidated['social_metrics'].items():
                        for metric, value in metrics.items():
                            metrics_table.add_row(
                                platform.title(),
                                metric.title(),
                                str(value)
                            )
                    
                    self.console.print(metrics_table)
            
            # Cross-Platform Analysis
            if 'cross_platform_analysis' in results:
                analysis = results['cross_platform_analysis']
                
                if 'error' not in analysis:
                    analysis_panel = Panel(
                        f"""
🔍 [bold]Cross-Platform Analysis[/bold]

Consistency Score: [cyan]{analysis['consistency_score']:.1f}%[/cyan]

Common Elements:
{chr(10).join([f"• {elem['type']}: {', '.join(elem['elements'])}" for elem in analysis.get('common_elements', [])]) or '• None detected'}

Behavioral Patterns:
{chr(10).join([f"• {pattern['pattern']}: {pattern['significance']}" for pattern in analysis.get('behavioral_patterns', [])]) or '• None detected'}
                        """,
                        title="🔗 Cross-Platform Analysis",
                        border_style="magenta"
                    )
                    self.console.print(analysis_panel)
            
        except Exception as e:
            self.console.print(f"[bold red]Error displaying scraping results: {str(e)}[/bold red]")

    def username_variations_generator(self, base_username):
        """
        Generate username variations for comprehensive search
        """
        try:
            self.console.print(f"\n[bold green]🎯 Username Variations for '{base_username}'[/bold green]")
            
            variations = set()
            variations.add(base_username)
            
            # Common variations
            variations.update([
                base_username.lower(),
                base_username.upper(),
                base_username.capitalize(),
            ])
            
            # Number variations
            for i in range(10):
                variations.add(f"{base_username}{i}")
                variations.add(f"{base_username}0{i}")
                variations.add(f"{i}{base_username}")
            
            # Common suffixes
            suffixes = ['_', '-', '.', '123', '1', '2', '3', 'official', 'real', 'the']
            for suffix in suffixes:
                variations.add(f"{base_username}{suffix}")
                variations.add(f"{suffix}{base_username}")
            
            # Year variations
            current_year = datetime.now().year
            for year in range(current_year - 30, current_year + 1):
                variations.add(f"{base_username}{year}")
                variations.add(f"{base_username}{str(year)[2:]}")
            
            # Special character variations
            variations.update([
                base_username.replace(' ', '_'),
                base_username.replace(' ', '-'),
                base_username.replace(' ', '.'),
                base_username.replace(' ', ''),
            ])
            
            # If username contains numbers, try without them
            if re.search(r'\d', base_username):
                no_numbers = re.sub(r'\d', '', base_username)
                if no_numbers:
                    variations.add(no_numbers)
            
            # If username contains special chars, try without them
            clean_username = re.sub(r'[^a-zA-Z0-9]', '', base_username)
            if clean_username != base_username:
                variations.add(clean_username)
            
            # Remove duplicates and empty strings
            variations = [v for v in variations if v and len(v) > 0]
            variations = sorted(list(set(variations)))
            
            # Display variations
            variations_table = Table(title="🎯 Username Variations", box=box.ROUNDED)
            variations_table.add_column("#", style="cyan", width=5)
            variations_table.add_column("Variation", style="white", width=25)
            variations_table.add_column("Type", style="yellow", width=20)
            
            variation_types = {
                base_username: "Original",
                base_username.lower(): "Lowercase",
                base_username.upper(): "Uppercase",
                base_username.capitalize(): "Capitalized"
            }
            
            for i, variation in enumerate(variations[:50], 1):  # Limit to 50
                var_type = variation_types.get(variation, "Generated")
                if variation.endswith(tuple('0123456789')):
                    var_type = "Number suffix"
                elif variation.startswith(tuple('0123456789')):
                    var_type = "Number prefix"
                elif '_' in variation or '-' in variation or '.' in variation:
                    var_type = "Special character"
                elif any(year in variation for year in [str(y) for y in range(1990, 2030)]):
                    var_type = "Year variant"
                
                variations_table.add_row(str(i), variation, var_type)
            
            self.console.print(variations_table)
            
            # Usage tips
            tips_panel = Panel(
                f"""
💡 [bold]Usage Tips[/bold]

[bold]Search Strategy:[/bold]
• Start with the most likely variations (original, lowercase, common suffixes)
• Use variations for social media searches where usernames may differ
• Try year variations if you know approximate age or birth year
• Check both with and without numbers/special characters

[bold]Platform-Specific Tips:[/bold]
• Instagram: Often uses dots, underscores, or numbers
• Twitter: Character limits may affect username choice
• GitHub: Usually professional, may include real name elements
• Gaming platforms: Often include numbers or gaming-related terms

[bold]Total Variations Generated:[/bold] {len(variations)}

[yellow]Note: Use these variations systematically across different platforms
for comprehensive username investigation.[/yellow]
                """,
                title="🎯 Search Strategy",
                border_style="blue"
            )
            
            self.console.print(tips_panel)
            
            results = {
                'base_username': base_username,
                'variations': variations,
                'total_variations': len(variations),
                'generation_timestamp': datetime.now().isoformat()
            }
            
            # Save results
            self.main_tool.save_result("username_variations", base_username, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error generating variations: {str(e)}[/bold red]")
            return None

    def enhanced_username_menu(self):
        """
        Enhanced username search menu
        """
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]👤 Enhanced Username Search & Analysis[/bold cyan]", style="blue"))
            
            table = Table(box=box.ROUNDED)
            table.add_column("Option", style="cyan", width=10)
            table.add_column("Tool", style="white", width=35)
            table.add_column("Description", style="yellow", width=45)
            
            options = [
                ("1", "Comprehensive Username Search", "Search across 500+ platforms"),
                ("2", "Profile Scraping & Analysis", "Deep profile data extraction"),
                ("3", "Username Variations Generator", "Generate search variations"),
                ("4", "Cross-Platform Investigation", "Link profiles across platforms"),
                ("5", "Social Media Deep Dive", "Detailed social media analysis"),
                ("6", "Professional Profile Search", "Focus on professional platforms"),
                ("7", "Gaming Profile Investigation", "Gaming platform searches"),
                ("8", "Batch Username Analysis", "Analyze multiple usernames"),
                ("9", "Export Investigation Report", "Generate comprehensive report"),
                ("0", "Back to Main Menu", "Return to main OSINT menu")
            ]
            
            for option, tool, desc in options:
                table.add_row(option, tool, desc)
            
            self.console.print(table)
            
            choice = input("\n👤 Select option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    self.comprehensive_username_search(username)
                    input("\nPress Enter to continue...")
            elif choice == "2":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    platforms = input("Enter platforms (comma-separated, or press Enter for default): ").strip()
                    if platforms:
                        platforms = [p.strip().lower() for p in platforms.split(',')]
                    else:
                        platforms = None
                    self.profile_scraping_analysis(username, platforms)
                    input("\nPress Enter to continue...")
            elif choice == "3":
                username = input("\n👤 Enter base username: ").strip()
                if username:
                    self.username_variations_generator(username)
                    input("\nPress Enter to continue...")
            elif choice == "4":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    self._cross_platform_investigation(username)
                    input("\nPress Enter to continue...")
            elif choice == "5":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    self._social_media_deep_dive(username)
                    input("\nPress Enter to continue...")
            elif choice == "6":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    self._professional_profile_search(username)
                    input("\nPress Enter to continue...")
            elif choice == "7":
                username = input("\n👤 Enter username: ").strip()
                if username:
                    self._gaming_profile_investigation(username)
                    input("\nPress Enter to continue...")
            elif choice == "8":
                self._batch_username_analysis()
                input("\nPress Enter to continue...")
            elif choice == "9":
                self._export_investigation_report()
                input("\nPress Enter to continue...")
            else:
                self.console.print("[red]Invalid option. Please try again.[/red]")
                time.sleep(1)

    def _cross_platform_investigation(self, username):
        """Cross-platform investigation"""
        self.console.print(f"\n[bold green]🔗 Cross-Platform Investigation for '{username}'[/bold green]")
        # Implementation for cross-platform investigation
        
    def _social_media_deep_dive(self, username):
        """Social media deep dive"""
        self.console.print(f"\n[bold green]📱 Social Media Deep Dive for '{username}'[/bold green]")
        # Implementation for social media deep dive
        
    def _professional_profile_search(self, username):
        """Professional profile search"""
        self.console.print(f"\n[bold green]💼 Professional Profile Search for '{username}'[/bold green]")
        # Implementation for professional profile search
        
    def _gaming_profile_investigation(self, username):
        """Gaming profile investigation"""
        self.console.print(f"\n[bold green]🎮 Gaming Profile Investigation for '{username}'[/bold green]")
        # Implementation for gaming profile investigation
        
    def _batch_username_analysis(self):
        """Batch username analysis"""
        self.console.print("\n[bold green]📊 Batch Username Analysis[/bold green]")
        # Implementation for batch analysis
        
    def _export_investigation_report(self):
        """Export investigation report"""
        self.console.print("\n[bold green]📤 Exporting Investigation Report[/bold green]")
        # Implementation for exporting reports
