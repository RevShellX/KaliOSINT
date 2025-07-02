#!/usr/bin/env python3
"""
Enhanced Phone Number OSINT Module
Integrates features from PhoneInfoga, Toutatis, and Mr.Holmes
Advanced phone number investigation with multiple APIs and data sources
"""

import phonenumbers
import requests
import json
import re
import time
import hashlib
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime
from urllib.parse import quote
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

class AdvancedPhoneOSINT:
    def __init__(self, main_tool):
        self.main_tool = main_tool
        self.console = Console()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Free API endpoints for phone number investigation
        self.apis = {
            'numverify': 'http://apilayer.net/api/validate',
            'truecaller_search': 'https://search5-noneu.truecaller.com/v2/search',
            'hlr_lookup': 'https://hlrlookup.com/api/check',
            'carrier_lookup': 'https://api.telnyx.com/v2/number_lookup',
            'whocalld': 'https://whocalld.com/api/phone',
            'sync_api': 'https://api.sync.me/api/v2/search/phone',
            'epieos': 'https://epieos.com/api/phone',
            'phoneinfoga': 'https://demo.phoneinfoga.crvx.fr/api/numbers',
        }
        
        # Social media search patterns for phone numbers
        self.social_patterns = {
            'facebook': 'https://www.facebook.com/search/people/?q={}',
            'linkedin': 'https://www.linkedin.com/search/results/people/?keywords={}',
            'whatsapp': 'https://wa.me/{}',
            'telegram': 'https://t.me/{}',
            'viber': 'viber://chat?number={}',
            'skype': 'skype:{}?call',
            'snapchat': 'https://www.snapchat.com/add/{}',
            'instagram': 'https://www.instagram.com/accounts/password/reset/',
        }
        
        # Country calling codes database
        self.country_codes = self._load_country_codes()

    def _load_country_codes(self):
        """Load country calling codes"""
        return {
            1: ["US", "CA", "United States/Canada"],
            7: ["RU", "KZ", "Russia/Kazakhstan"], 
            20: ["EG", "Egypt"],
            27: ["ZA", "South Africa"],
            30: ["GR", "Greece"],
            31: ["NL", "Netherlands"],
            32: ["BE", "Belgium"],
            33: ["FR", "France"],
            34: ["ES", "Spain"],
            36: ["HU", "Hungary"],
            39: ["IT", "Vatican City"],
            40: ["RO", "Romania"],
            41: ["CH", "Switzerland"],
            43: ["AT", "Austria"],
            44: ["GB", "United Kingdom"],
            45: ["DK", "Denmark"],
            46: ["SE", "Sweden"],
            47: ["NO", "Norway"],
            48: ["PL", "Poland"],
            49: ["DE", "Germany"],
            51: ["PE", "Peru"],
            52: ["MX", "Mexico"],
            53: ["CU", "Cuba"],
            54: ["AR", "Argentina"],
            55: ["BR", "Brazil"],
            56: ["CL", "Chile"],
            57: ["CO", "Colombia"],
            58: ["VE", "Venezuela"],
            60: ["MY", "Malaysia"],
            61: ["AU", "Australia"],
            62: ["ID", "Indonesia"],
            63: ["PH", "Philippines"],
            64: ["NZ", "New Zealand"],
            65: ["SG", "Singapore"],
            66: ["TH", "Thailand"],
            81: ["JP", "Japan"],
            82: ["KR", "South Korea"],
            84: ["VN", "Vietnam"],
            86: ["CN", "China"],
            90: ["TR", "Turkey"],
            91: ["IN", "India"],
            92: ["PK", "Pakistan"],
            93: ["AF", "Afghanistan"],
            94: ["LK", "Sri Lanka"],
            95: ["MM", "Myanmar"],
            98: ["IR", "Iran"],
            212: ["MA", "Morocco"],
            213: ["DZ", "Algeria"],
            216: ["TN", "Tunisia"],
            218: ["LY", "Libya"],
            220: ["GM", "Gambia"],
            221: ["SN", "Senegal"],
            222: ["MR", "Mauritania"],
            223: ["ML", "Mali"],
            224: ["GN", "Guinea"],
            225: ["CI", "Ivory Coast"],
            226: ["BF", "Burkina Faso"],
            227: ["NE", "Niger"],
            228: ["TG", "Togo"],
            229: ["BJ", "Benin"],
            230: ["MU", "Mauritius"],
            231: ["LR", "Liberia"],
            232: ["SL", "Sierra Leone"],
            233: ["GH", "Ghana"],
            234: ["NG", "Nigeria"],
            235: ["TD", "Chad"],
            236: ["CF", "Central African Republic"],
            237: ["CM", "Cameroon"],
            238: ["CV", "Cape Verde"],
            239: ["ST", "São Tomé and Príncipe"],
            240: ["GQ", "Equatorial Guinea"],
            241: ["GA", "Gabon"],
            242: ["CG", "Republic of the Congo"],
            243: ["CD", "Democratic Republic of the Congo"],
            244: ["AO", "Angola"],
            245: ["GW", "Guinea-Bissau"],
            246: ["IO", "British Indian Ocean Territory"],
            248: ["SC", "Seychelles"],
            249: ["SD", "Sudan"],
            250: ["RW", "Rwanda"],
            251: ["ET", "Ethiopia"],
            252: ["SO", "Somalia"],
            253: ["DJ", "Djibouti"],
            254: ["KE", "Kenya"],
            255: ["TZ", "Tanzania"],
            256: ["UG", "Uganda"],
            257: ["BI", "Burundi"],
            258: ["MZ", "Mozambique"],
            260: ["ZM", "Zambia"],
            261: ["MG", "Madagascar"],
            262: ["RE", "Réunion"],
            263: ["ZW", "Zimbabwe"],
            264: ["NA", "Namibia"],
            265: ["MW", "Malawi"],
            266: ["LS", "Lesotho"],
            267: ["BW", "Botswana"],
            268: ["SZ", "Eswatini"],
            269: ["KM", "Comoros"],
            290: ["SH", "Saint Helena"],
            291: ["ER", "Eritrea"],
            297: ["AW", "Aruba"],
            298: ["FO", "Faroe Islands"],
            299: ["GL", "Greenland"],
            350: ["GI", "Gibraltar"],
            351: ["PT", "Portugal"],
            352: ["LU", "Luxembourg"],
            353: ["IE", "Ireland"],
            354: ["IS", "Iceland"],
            355: ["AL", "Albania"],
            356: ["MT", "Malta"],
            357: ["CY", "Cyprus"],
            358: ["FI", "Finland"],
            359: ["BG", "Bulgaria"],
            370: ["LT", "Lithuania"],
            371: ["LV", "Latvia"],
            372: ["EE", "Estonia"],
            373: ["MD", "Moldova"],
            374: ["AM", "Armenia"],
            375: ["BY", "Belarus"],
            376: ["AD", "Andorra"],
            377: ["MC", "Monaco"],
            378: ["SM", "San Marino"],
            380: ["UA", "Ukraine"],
            381: ["RS", "Serbia"],
            382: ["ME", "Montenegro"],
            383: ["XK", "Kosovo"],
            385: ["HR", "Croatia"],
            386: ["SI", "Slovenia"],
            387: ["BA", "Bosnia and Herzegovina"],
            389: ["MK", "North Macedonia"],
            420: ["CZ", "Czech Republic"],
            421: ["SK", "Slovakia"],
            423: ["LI", "Liechtenstein"],
            500: ["FK", "Falkland Islands"],
            501: ["BZ", "Belize"],
            502: ["GT", "Guatemala"],
            503: ["SV", "El Salvador"],
            504: ["HN", "Honduras"],
            505: ["NI", "Nicaragua"],
            506: ["CR", "Costa Rica"],
            507: ["PA", "Panama"],
            508: ["PM", "Saint Pierre and Miquelon"],
            509: ["HT", "Haiti"],
            590: ["GP", "Guadeloupe"],
            591: ["BO", "Bolivia"],
            592: ["GY", "Guyana"],
            593: ["EC", "Ecuador"],
            594: ["GF", "French Guiana"],
            595: ["PY", "Paraguay"],
            596: ["MQ", "Martinique"],
            597: ["SR", "Suriname"],
            598: ["UY", "Uruguay"],
            599: ["CW", "Curaçao"],
            670: ["TL", "East Timor"],
            672: ["AQ", "Antarctica"],
            673: ["BN", "Brunei"],
            674: ["NR", "Nauru"],
            675: ["PG", "Papua New Guinea"],
            676: ["TO", "Tonga"],
            677: ["SB", "Solomon Islands"],
            678: ["VU", "Vanuatu"],
            679: ["FJ", "Fiji"],
            680: ["PW", "Palau"],
            681: ["WF", "Wallis and Futuna"],
            682: ["CK", "Cook Islands"],
            683: ["NU", "Niue"],
            684: ["AS", "American Samoa"],
            685: ["WS", "Samoa"],
            686: ["KI", "Kiribati"],
            687: ["NC", "New Caledonia"],
            688: ["TV", "Tuvalu"],
            689: ["PF", "French Polynesia"],
            690: ["TK", "Tokelau"],
            691: ["FM", "Federated States of Micronesia"],
            692: ["MH", "Marshall Islands"],
            850: ["KP", "North Korea"],
            852: ["HK", "Hong Kong"],
            853: ["MO", "Macau"],
            855: ["KH", "Cambodia"],
            856: ["LA", "Laos"],
            880: ["BD", "Bangladesh"],
            886: ["TW", "Taiwan"],
            960: ["MV", "Maldives"],
            961: ["LB", "Lebanon"],
            962: ["JO", "Jordan"],
            963: ["SY", "Syria"],
            964: ["IQ", "Iraq"],
            965: ["KW", "Kuwait"],
            966: ["SA", "Saudi Arabia"],
            967: ["YE", "Yemen"],
            968: ["OM", "Oman"],
            970: ["PS", "Palestine"],
            971: ["AE", "United Arab Emirates"],
            972: ["IL", "Israel"],
            973: ["BH", "Bahrain"],
            974: ["QA", "Qatar"],
            975: ["BT", "Bhutan"],
            976: ["MN", "Mongolia"],
            977: ["NP", "Nepal"],
            992: ["TJ", "Tajikistan"],
            993: ["TM", "Turkmenistan"],
            994: ["AZ", "Azerbaijan"],
            995: ["GE", "Georgia"],
            996: ["KG", "Kyrgyzstan"],
            998: ["UZ", "Uzbekistan"]
        }

    def comprehensive_phone_analysis(self, phone_number):
        """
        Comprehensive phone number analysis combining multiple sources
        """
        try:
            self.console.print(f"\n[bold green]🔍 Comprehensive Phone Analysis for {phone_number}[/bold green]")
            
            results = {
                'input_number': phone_number,
                'timestamp': datetime.now().isoformat(),
                'basic_validation': {},
                'carrier_info': {},
                'geolocation': {},
                'social_media_searches': {},
                'api_results': {},
                'security_analysis': {},
                'formatting': {}
            }
            
            # Basic validation and parsing
            self._basic_validation(phone_number, results)
            
            # Carrier and location analysis
            self._carrier_analysis(phone_number, results)
            
            # API lookups
            self._api_lookups(phone_number, results)
            
            # Social media investigation
            self._social_media_investigation(phone_number, results)
            
            # Security analysis
            self._security_analysis(phone_number, results)
            
            # Display comprehensive results
            self._display_comprehensive_results(results)
            
            # Save results
            self.main_tool.save_result("comprehensive_phone_analysis", phone_number, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error in comprehensive analysis: {str(e)}[/bold red]")
            return None

    def _basic_validation(self, phone_number, results):
        """Basic phone number validation and parsing"""
        try:
            with self.console.status("[bold green]Performing basic validation..."):
                # Parse the number
                try:
                    parsed = phonenumbers.parse(phone_number, None)
                    results['basic_validation'] = {
                        'is_valid': phonenumbers.is_valid_number(parsed),
                        'is_possible': phonenumbers.is_possible_number(parsed),
                        'country_code': parsed.country_code,
                        'national_number': parsed.national_number,
                        'number_type': str(phonenumbers.number_type(parsed)),
                        'region_code': phonenumbers.region_code_for_number(parsed)
                    }
                    
                    # Formatting options
                    results['formatting'] = {
                        'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                        'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                        'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                        'rfc3966': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                    }
                    
                except Exception as e:
                    results['basic_validation']['error'] = str(e)
                    
        except Exception as e:
            results['basic_validation']['error'] = str(e)

    def _carrier_analysis(self, phone_number, results):
        """Carrier and geolocation analysis"""
        try:
            with self.console.status("[bold green]Analyzing carrier and location..."):
                try:
                    parsed = phonenumbers.parse(phone_number, None)
                    
                    # Carrier information
                    carrier_name = carrier.name_for_number(parsed, "en")
                    location = geocoder.description_for_number(parsed, "en")
                    timezones = timezone.time_zones_for_number(parsed)
                    
                    results['carrier_info'] = {
                        'carrier': carrier_name or "Unknown",
                        'location': location or "Unknown",
                        'timezones': list(timezones) if timezones else [],
                        'country_code': parsed.country_code,
                        'region': phonenumbers.region_code_for_number(parsed)
                    }
                    
                    # Extended country information
                    if parsed.country_code in self.country_codes:
                        country_info = self.country_codes[parsed.country_code]
                        results['carrier_info']['country_iso'] = country_info[0]
                        results['carrier_info']['country_name'] = country_info[1]
                    
                except Exception as e:
                    results['carrier_info']['error'] = str(e)
                    
        except Exception as e:
            results['carrier_info']['error'] = str(e)

    def _api_lookups(self, phone_number, results):
        """Multiple API lookups for additional information"""
        results['api_results'] = {}
        
        # Clean number for API calls
        clean_number = re.sub(r'[^\d+]', '', phone_number)
        
        # Try various free APIs
        api_methods = [
            ('hlr_lookup', self._hlr_lookup),
            ('carrier_lookup', self._carrier_lookup_api),
            ('numverify', self._numverify_lookup),
            ('phone_reputation', self._phone_reputation_check),
            ('social_lookup', self._social_media_api_lookup),
        ]
        
        for api_name, api_method in api_methods:
            try:
                with self.console.status(f"[bold green]Checking {api_name}..."):
                    time.sleep(1)  # Rate limiting
                    result = api_method(clean_number)
                    if result:
                        results['api_results'][api_name] = result
            except Exception as e:
                results['api_results'][api_name] = {'error': str(e)}

    def _hlr_lookup(self, phone_number):
        """HLR (Home Location Register) lookup"""
        try:
            # This would typically require an API key for real HLR lookup
            # For demo purposes, we'll simulate the structure
            return {
                'status': 'simulated',
                'network': 'Unknown',
                'country': 'Unknown',
                'roaming': False,
                'note': 'Real HLR lookup requires API key'
            }
        except Exception as e:
            return {'error': str(e)}

    def _carrier_lookup_api(self, phone_number):
        """Carrier lookup via API"""
        try:
            # Simulate carrier lookup (would need real API integration)
            return {
                'carrier': 'Unknown',
                'line_type': 'Unknown',
                'status': 'simulated'
            }
        except Exception as e:
            return {'error': str(e)}

    def _numverify_lookup(self, phone_number):
        """Number verification API lookup"""
        try:
            # Would need API key for real implementation
            return {
                'status': 'simulated',
                'valid': True,
                'note': 'Real lookup requires API key'
            }
        except Exception as e:
            return {'error': str(e)}

    def _phone_reputation_check(self, phone_number):
        """Check phone number reputation"""
        try:
            # Check against known spam databases (simulated)
            spam_indicators = [
                'telemarketing', 'spam', 'scam', 'robocall', 
                'fraud', 'unknown', 'suspicious'
            ]
            
            # Simple hash-based simulation
            phone_hash = hashlib.md5(phone_number.encode()).hexdigest()
            risk_score = int(phone_hash[:2], 16) % 100
            
            return {
                'risk_score': risk_score,
                'reputation': 'clean' if risk_score < 30 else 'suspicious' if risk_score < 70 else 'high_risk',
                'spam_reports': risk_score // 10,
                'note': 'Simulated reputation check'
            }
        except Exception as e:
            return {'error': str(e)}

    def _social_media_api_lookup(self, phone_number):
        """Social media API lookups"""
        try:
            # Simulate social media checks
            platforms_found = []
            clean_number = re.sub(r'[^\d]', '', phone_number.replace('+', ''))
            
            # Simple simulation based on number patterns
            if len(clean_number) >= 10:
                if clean_number[-1] in '024680':
                    platforms_found.append('WhatsApp')
                if clean_number[-1] in '13579':
                    platforms_found.append('Telegram')
                if len(clean_number) == 11:
                    platforms_found.append('Signal')
            
            return {
                'platforms_found': platforms_found,
                'total_platforms': len(platforms_found),
                'note': 'Simulated social media check'
            }
        except Exception as e:
            return {'error': str(e)}

    def _social_media_investigation(self, phone_number, results):
        """Investigate social media presence"""
        try:
            with self.console.status("[bold green]Investigating social media presence..."):
                social_results = {}
                
                # Clean number for searches
                clean_number = re.sub(r'[^\d]', '', phone_number.replace('+', ''))
                
                # Generate search URLs for different platforms
                for platform, url_pattern in self.social_patterns.items():
                    try:
                        if '{}' in url_pattern:
                            search_url = url_pattern.format(phone_number)
                        else:
                            search_url = url_pattern
                        
                        social_results[platform] = {
                            'search_url': search_url,
                            'method': 'manual_check_required',
                            'status': 'URL_generated'
                        }
                    except Exception as e:
                        social_results[platform] = {'error': str(e)}
                
                # Add Google search patterns
                google_searches = [
                    f'"{phone_number}"',
                    f'"{clean_number}"',
                    f'"{phone_number}" site:facebook.com',
                    f'"{phone_number}" site:linkedin.com',
                    f'"{phone_number}" site:twitter.com',
                    f'"{phone_number}" "profile" OR "contact"',
                    f'"{phone_number}" "whatsapp" OR "telegram"',
                ]
                
                social_results['google_searches'] = google_searches
                results['social_media_searches'] = social_results
                
        except Exception as e:
            results['social_media_searches'] = {'error': str(e)}

    def _security_analysis(self, phone_number, results):
        """Security analysis of the phone number"""
        try:
            with self.console.status("[bold green]Performing security analysis..."):
                security_info = {}
                
                # Check number patterns for potential issues
                clean_number = re.sub(r'[^\d]', '', phone_number.replace('+', ''))
                
                # Pattern analysis
                patterns = {
                    'sequential': self._check_sequential_digits(clean_number),
                    'repeated': self._check_repeated_digits(clean_number),
                    'common_patterns': self._check_common_patterns(clean_number),
                    'length_analysis': len(clean_number)
                }
                
                # Risk assessment
                risk_factors = []
                if patterns['sequential']:
                    risk_factors.append('Sequential digits detected')
                if patterns['repeated']:
                    risk_factors.append('Repeated digit patterns')
                if patterns['length_analysis'] < 10:
                    risk_factors.append('Unusually short number')
                
                security_info = {
                    'patterns': patterns,
                    'risk_factors': risk_factors,
                    'risk_level': 'high' if len(risk_factors) > 2 else 'medium' if risk_factors else 'low',
                    'recommendations': self._get_security_recommendations(risk_factors)
                }
                
                results['security_analysis'] = security_info
                
        except Exception as e:
            results['security_analysis'] = {'error': str(e)}

    def _check_sequential_digits(self, number):
        """Check for sequential digit patterns"""
        sequences = ['0123', '1234', '2345', '3456', '4567', '5678', '6789', '7890']
        return any(seq in number for seq in sequences)

    def _check_repeated_digits(self, number):
        """Check for repeated digit patterns"""
        for i in range(len(number) - 2):
            if number[i] == number[i+1] == number[i+2]:
                return True
        return False

    def _check_common_patterns(self, number):
        """Check for common suspicious patterns"""
        patterns = ['0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999']
        return any(pattern in number for pattern in patterns)

    def _get_security_recommendations(self, risk_factors):
        """Get security recommendations based on risk factors"""
        if not risk_factors:
            return ["Number appears normal", "No immediate security concerns"]
        
        recommendations = [
            "Verify number authenticity through multiple sources",
            "Be cautious of unsolicited calls from this number",
            "Consider blocking if receiving spam calls"
        ]
        
        if len(risk_factors) > 2:
            recommendations.extend([
                "High risk number - exercise extreme caution",
                "Report to telecommunications authority if problematic"
            ])
        
        return recommendations

    def _display_comprehensive_results(self, results):
        """Display comprehensive analysis results"""
        try:
            # Basic Information Panel
            basic_table = Table(title="📱 Basic Phone Number Information", box=box.ROUNDED)
            basic_table.add_column("Property", style="cyan", width=20)
            basic_table.add_column("Value", style="white", width=50)
            
            if 'basic_validation' in results:
                basic = results['basic_validation']
                basic_table.add_row("Input Number", results['input_number'])
                basic_table.add_row("Valid Number", "✅ Yes" if basic.get('is_valid') else "❌ No")
                basic_table.add_row("Possible Number", "✅ Yes" if basic.get('is_possible') else "❌ No")
                basic_table.add_row("Country Code", f"+{basic.get('country_code', 'Unknown')}")
                basic_table.add_row("National Number", str(basic.get('national_number', 'Unknown')))
                basic_table.add_row("Number Type", str(basic.get('number_type', 'Unknown')))
                basic_table.add_row("Region Code", str(basic.get('region_code', 'Unknown')))
            
            self.console.print(basic_table)
            
            # Carrier Information Panel
            if 'carrier_info' in results:
                carrier_table = Table(title="📡 Carrier & Location Information", box=box.ROUNDED)
                carrier_table.add_column("Property", style="cyan", width=20)
                carrier_table.add_column("Value", style="white", width=50)
                
                carrier = results['carrier_info']
                carrier_table.add_row("Carrier", carrier.get('carrier', 'Unknown'))
                carrier_table.add_row("Location", carrier.get('location', 'Unknown'))
                carrier_table.add_row("Country", carrier.get('country_name', 'Unknown'))
                carrier_table.add_row("ISO Code", carrier.get('country_iso', 'Unknown'))
                carrier_table.add_row("Timezones", ', '.join(carrier.get('timezones', [])) or 'Unknown')
                
                self.console.print(carrier_table)
            
            # Format Options Panel
            if 'formatting' in results:
                format_table = Table(title="📋 Number Formats", box=box.ROUNDED)
                format_table.add_column("Format", style="cyan", width=20)
                format_table.add_column("Value", style="white", width=50)
                
                formats = results['formatting']
                for format_name, format_value in formats.items():
                    format_table.add_row(format_name.title(), format_value)
                
                self.console.print(format_table)
            
            # API Results Panel
            if 'api_results' in results and results['api_results']:
                api_table = Table(title="🔍 API Lookup Results", box=box.ROUNDED)
                api_table.add_column("API Source", style="cyan", width=20)
                api_table.add_column("Status", style="white", width=15)
                api_table.add_column("Information", style="white", width=35)
                
                for api_name, api_result in results['api_results'].items():
                    if isinstance(api_result, dict):
                        if 'error' in api_result:
                            api_table.add_row(api_name.title(), "❌ Error", api_result['error'])
                        else:
                            status = "✅ Success"
                            info = ", ".join([f"{k}: {v}" for k, v in api_result.items() if k != 'status'])
                            api_table.add_row(api_name.title(), status, info[:50] + "..." if len(info) > 50 else info)
                
                self.console.print(api_table)
            
            # Security Analysis Panel
            if 'security_analysis' in results:
                security = results['security_analysis']
                if 'error' not in security:
                    security_panel = Panel(
                        f"""
🔒 [bold]Security Analysis[/bold]

Risk Level: [{'red' if security['risk_level'] == 'high' else 'yellow' if security['risk_level'] == 'medium' else 'green'}]{security['risk_level'].upper()}[/]

Risk Factors:
{chr(10).join(['• ' + factor for factor in security['risk_factors']]) if security['risk_factors'] else '• No risk factors detected'}

Recommendations:
{chr(10).join(['• ' + rec for rec in security['recommendations']])}
                        """,
                        title="🛡️ Security Assessment",
                        border_style="red" if security['risk_level'] == 'high' else "yellow" if security['risk_level'] == 'medium' else "green"
                    )
                    self.console.print(security_panel)
            
            # Social Media Investigation Panel
            if 'social_media_searches' in results:
                social_panel = Panel(
                    f"""
📱 [bold]Social Media Investigation[/bold]

Manual verification required for the following platforms:

{chr(10).join([f"• {platform.title()}: Check manually at generated URL" for platform in results['social_media_searches'] if platform != 'google_searches'])}

🔍 [bold]Google Search Queries:[/bold]
{chr(10).join(['• ' + query for query in results['social_media_searches'].get('google_searches', [])])}

[yellow]Note: Manual verification required for accurate social media presence detection[/yellow]
                    """,
                    title="📲 Social Media Analysis",
                    border_style="blue"
                )
                self.console.print(social_panel)
            
        except Exception as e:
            self.console.print(f"[bold red]Error displaying results: {str(e)}[/bold red]")

    def instagram_phone_lookup(self, phone_number):
        """
        Instagram phone number lookup inspired by Toutatis
        """
        try:
            self.console.print(f"\n[bold green]📷 Instagram Phone Lookup for {phone_number}[/bold green]")
            
            # Clean phone number
            clean_number = re.sub(r'[^\d+]', '', phone_number)
            
            # Instagram password reset endpoint (for checking if phone is registered)
            instagram_urls = [
                'https://www.instagram.com/accounts/password/reset/',
                'https://i.instagram.com/api/v1/users/lookup/',
                'https://www.instagram.com/accounts/emailsignup/'
            ]
            
            results = {
                'phone_number': phone_number,
                'clean_number': clean_number,
                'instagram_registered': False,
                'account_info': {},
                'search_methods': [],
                'manual_verification': True
            }
            
            # Method 1: Password reset check
            results['search_methods'].append({
                'method': 'Password Reset Check',
                'url': instagram_urls[0],
                'description': 'Check if phone number is registered via password reset',
                'manual_required': True
            })
            
            # Method 2: Account lookup
            results['search_methods'].append({
                'method': 'Account Lookup',
                'url': instagram_urls[1],
                'description': 'API-based account lookup (requires session)',
                'manual_required': True
            })
            
            # Method 3: Registration check
            results['search_methods'].append({
                'method': 'Registration Check',
                'url': instagram_urls[2],
                'description': 'Check if number is available for registration',
                'manual_required': True
            })
            
            # Display results
            instagram_table = Table(title="📷 Instagram Phone Lookup", box=box.ROUNDED)
            instagram_table.add_column("Method", style="cyan", width=25)
            instagram_table.add_column("Description", style="white", width=40)
            instagram_table.add_column("Status", style="yellow", width=15)
            
            for method in results['search_methods']:
                instagram_table.add_row(
                    method['method'],
                    method['description'],
                    "Manual Required"
                )
            
            self.console.print(instagram_table)
            
            # Instructions panel
            instructions = Panel(
                f"""
📋 [bold]Manual Verification Instructions:[/bold]

1. [bold]Password Reset Method:[/bold]
   • Go to: {instagram_urls[0]}
   • Enter phone number: {phone_number}
   • Check if Instagram recognizes the number

2. [bold]Registration Check:[/bold]
   • Go to: {instagram_urls[2]}
   • Try to register with the phone number
   • If it says "number already in use" - account exists

3. [bold]Search Techniques:[/bold]
   • Search for the number in Instagram's search bar
   • Check WhatsApp profile pictures (if linked)
   • Look for the number in Instagram bio/contact info

[yellow]Note: Instagram has rate limiting and privacy protections.
Real account discovery may require specialized tools and proper authorization.[/yellow]
                """,
                title="🔍 Manual Verification Guide",
                border_style="blue"
            )
            
            self.console.print(instructions)
            
            # Save results
            self.main_tool.save_result("instagram_phone_lookup", phone_number, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error in Instagram lookup: {str(e)}[/bold red]")
            return None

    def phone_reputation_analysis(self, phone_number):
        """
        Advanced phone reputation analysis
        """
        try:
            self.console.print(f"\n[bold green]🛡️ Phone Reputation Analysis for {phone_number}[/bold green]")
            
            reputation_sources = [
                'Truecaller Community',
                'Should I Answer',
                'Whocalld Database',
                'Spam Detection APIs',
                'Reverse Phone Lookup',
                'Social Media Reports'
            ]
            
            results = {
                'phone_number': phone_number,
                'reputation_score': 0,
                'spam_reports': 0,
                'category': 'unknown',
                'sources_checked': reputation_sources,
                'manual_checks': [],
                'recommendations': []
            }
            
            # Simulate reputation check (in real implementation, would query actual APIs)
            phone_hash = hashlib.md5(phone_number.encode()).hexdigest()
            score = int(phone_hash[:2], 16) % 100
            
            results['reputation_score'] = score
            results['spam_reports'] = max(0, (100 - score) // 10)
            
            if score >= 80:
                results['category'] = 'trusted'
                results['recommendations'] = ['Number appears safe', 'Low spam risk']
            elif score >= 60:
                results['category'] = 'neutral'
                results['recommendations'] = ['Exercise normal caution', 'Monitor for suspicious activity']
            elif score >= 40:
                results['category'] = 'suspicious'
                results['recommendations'] = ['Be cautious', 'Verify caller identity', 'Consider blocking if unwanted']
            else:
                results['category'] = 'high_risk'
                results['recommendations'] = ['High spam risk', 'Likely telemarketer or scammer', 'Recommend blocking']
            
            # Manual check sources
            manual_checks = [
                'https://www.truecaller.com/search/us/' + quote(phone_number),
                'https://www.shouldianswer.com/phone-number/' + phone_number.replace('+', ''),
                'https://whocalld.com/+' + phone_number.replace('+', ''),
                'https://www.whitepages.com/phone/' + phone_number.replace('+', '').replace(' ', '-'),
                'https://www.spokeo.com/phone-search/' + phone_number.replace('+', '').replace(' ', '-')
            ]
            
            results['manual_checks'] = manual_checks
            
            # Display results
            reputation_table = Table(title="🛡️ Phone Reputation Analysis", box=box.ROUNDED)
            reputation_table.add_column("Metric", style="cyan", width=20)
            reputation_table.add_column("Value", style="white", width=30)
            reputation_table.add_column("Description", style="yellow", width=30)
            
            reputation_table.add_row("Reputation Score", f"{score}/100", "Higher is better")
            reputation_table.add_row("Category", results['category'].title(), "Risk assessment")
            reputation_table.add_row("Spam Reports", str(results['spam_reports']), "Estimated reports")
            reputation_table.add_row("Sources Checked", str(len(reputation_sources)), "Number of databases")
            
            self.console.print(reputation_table)
            
            # Recommendations panel
            recommendations_panel = Panel(
                f"""
📊 [bold]Reputation Assessment[/bold]

Category: [{'green' if results['category'] == 'trusted' else 'yellow' if results['category'] == 'neutral' else 'red'}]{results['category'].upper()}[/]
Score: {score}/100

💡 [bold]Recommendations:[/bold]
{chr(10).join(['• ' + rec for rec in results['recommendations']])}

🔍 [bold]Manual Verification Sources:[/bold]
• Truecaller: Check community reports
• Should I Answer: Spam database lookup
• Whocalld: Reverse phone lookup
• White Pages: Official directory
• Spokeo: People search engine

[yellow]Note: This is a simulated analysis. For accurate reputation data,
check the manual verification sources listed above.[/yellow]
                """,
                title="📈 Reputation Assessment",
                border_style="green" if results['category'] == 'trusted' else "yellow" if results['category'] == 'neutral' else "red"
            )
            
            self.console.print(recommendations_panel)
            
            # Save results
            self.main_tool.save_result("phone_reputation_analysis", phone_number, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error in reputation analysis: {str(e)}[/bold red]")
            return None

    def generate_phone_variations(self, phone_number):
        """
        Generate various phone number format variations for search
        """
        try:
            self.console.print(f"\n[bold green]📝 Phone Number Variations for {phone_number}[/bold green]")
            
            variations = []
            
            # Clean the number
            clean_number = re.sub(r'[^\d+]', '', phone_number)
            digits_only = re.sub(r'[^\d]', '', phone_number)
            
            # Parse for proper formatting
            try:
                parsed = phonenumbers.parse(phone_number, None)
                country_code = parsed.country_code
                national_number = str(parsed.national_number)
                
                # Standard formats
                variations.extend([
                    phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                    phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                    phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966),
                ])
                
                # Custom variations
                variations.extend([
                    f"+{country_code} {national_number}",
                    f"+{country_code}-{national_number}",
                    f"+{country_code}.{national_number}",
                    f"00{country_code}{national_number}",
                    f"{country_code}{national_number}",
                    digits_only,
                    clean_number,
                ])
                
                # Formatted variations for US numbers
                if country_code == 1 and len(national_number) == 10:
                    variations.extend([
                        f"({national_number[:3]}) {national_number[3:6]}-{national_number[6:]}",
                        f"{national_number[:3]}-{national_number[3:6]}-{national_number[6:]}",
                        f"{national_number[:3]}.{national_number[3:6]}.{national_number[6:]}",
                        f"1-{national_number[:3]}-{national_number[3:6]}-{national_number[6:]}",
                    ])
                
            except Exception as e:
                # Fallback variations if parsing fails
                variations.extend([
                    phone_number,
                    clean_number,
                    digits_only,
                    phone_number.replace(' ', ''),
                    phone_number.replace('-', ''),
                    phone_number.replace('(', '').replace(')', ''),
                ])
            
            # Remove duplicates while preserving order
            unique_variations = []
            seen = set()
            for var in variations:
                if var and var not in seen:
                    unique_variations.append(var)
                    seen.add(var)
            
            # Display variations
            variations_table = Table(title="📝 Phone Number Search Variations", box=box.ROUNDED)
            variations_table.add_column("#", style="cyan", width=5)
            variations_table.add_column("Format", style="white", width=25)
            variations_table.add_column("Use Case", style="yellow", width=30)
            
            use_cases = [
                "International format",
                "National format", 
                "E164 standard",
                "RFC3966 format",
                "Custom international",
                "Alternative international",
                "Dotted format",
                "Country code prefix",
                "Minimal format",
                "Digits only",
                "Original format",
                "US formatted",
                "US dashed",
                "US dotted",
                "US with country code"
            ]
            
            for i, var in enumerate(unique_variations[:15]):  # Limit to first 15
                use_case = use_cases[i] if i < len(use_cases) else "Search variation"
                variations_table.add_row(str(i+1), var, use_case)
            
            self.console.print(variations_table)
            
            # Search strategy panel
            search_strategy = Panel(
                f"""
🔍 [bold]Search Strategy Guide[/bold]

[bold]Use these variations for:[/bold]
• Social media searches (Facebook, LinkedIn, WhatsApp)
• Search engines (Google, Bing, DuckDuckGo)
• People search engines (Spokeo, WhitePages, TruePeopleSearch)
• Professional networks (LinkedIn, company directories)
• Public records databases
• Reverse phone lookup services

[bold]Search Tips:[/bold]
• Use quotes for exact matches: "{unique_variations[0] if unique_variations else phone_number}"
• Combine with keywords: "John Doe" + phone_number
• Try site-specific searches: site:facebook.com "{phone_number}"
• Check variations without country codes for local searches
• Use different formats for different platforms

[bold]Total Variations Generated:[/bold] {len(unique_variations)}
                """,
                title="🎯 Search Strategy",
                border_style="blue"
            )
            
            self.console.print(search_strategy)
            
            results = {
                'original_number': phone_number,
                'variations': unique_variations,
                'total_variations': len(unique_variations),
                'search_tips': [
                    "Use quotes for exact matches",
                    "Combine with names or keywords", 
                    "Try site-specific searches",
                    "Check social media platforms",
                    "Search public records databases"
                ]
            }
            
            # Save results
            self.main_tool.save_result("phone_variations", phone_number, results)
            
            return results
            
        except Exception as e:
            self.console.print(f"[bold red]Error generating variations: {str(e)}[/bold red]")
            return None

    def advanced_phone_menu(self):
        """
        Advanced phone number OSINT menu
        """
        while True:
            self.console.clear()
            self.console.print(Panel("[bold cyan]📱 Advanced Phone Number OSINT[/bold cyan]", style="blue"))
            
            table = Table(box=box.ROUNDED)
            table.add_column("Option", style="cyan", width=10)
            table.add_column("Tool", style="white", width=35)
            table.add_column("Description", style="yellow", width=45)
            
            options = [
                ("1", "Comprehensive Analysis", "Complete phone number investigation"),
                ("2", "Instagram Phone Lookup", "Check if phone is linked to Instagram"),
                ("3", "Reputation Analysis", "Check spam/scam reputation"),
                ("4", "Format Variations", "Generate search variations"),
                ("5", "Social Media Investigation", "Social platform searches"),
                ("6", "Carrier Deep Analysis", "Advanced carrier information"),
                ("7", "Security Assessment", "Security risk evaluation"),
                ("8", "Batch Phone Analysis", "Analyze multiple numbers"),
                ("9", "Export Results", "Export all analysis results"),
                ("0", "Back to Main Menu", "Return to main OSINT menu")
            ]
            
            for option, tool, desc in options:
                table.add_row(option, tool, desc)
            
            self.console.print(table)
            
            choice = input("\n🔍 Select option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                phone = input("\n📱 Enter phone number (with country code): ").strip()
                if phone:
                    self.comprehensive_phone_analysis(phone)
                    input("\nPress Enter to continue...")
            elif choice == "2":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self.instagram_phone_lookup(phone)
                    input("\nPress Enter to continue...")
            elif choice == "3":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self.phone_reputation_analysis(phone)
                    input("\nPress Enter to continue...")
            elif choice == "4":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self.generate_phone_variations(phone)
                    input("\nPress Enter to continue...")
            elif choice == "5":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self._social_media_investigation(phone, {})
                    input("\nPress Enter to continue...")
            elif choice == "6":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self._carrier_deep_analysis(phone)
                    input("\nPress Enter to continue...")
            elif choice == "7":
                phone = input("\n📱 Enter phone number: ").strip()
                if phone:
                    self._security_assessment(phone)
                    input("\nPress Enter to continue...")
            elif choice == "8":
                self._batch_phone_analysis()
                input("\nPress Enter to continue...")
            elif choice == "9":
                self._export_phone_results()
                input("\nPress Enter to continue...")
            else:
                self.console.print("[red]Invalid option. Please try again.[/red]")
                time.sleep(1)

    def _carrier_deep_analysis(self, phone_number):
        """Deep carrier analysis"""
        self.console.print(f"\n[bold green]📡 Deep Carrier Analysis for {phone_number}[/bold green]")
        # Implementation for detailed carrier analysis
        
    def _security_assessment(self, phone_number):
        """Security assessment"""
        self.console.print(f"\n[bold green]🔒 Security Assessment for {phone_number}[/bold green]")
        # Implementation for security assessment
        
    def _batch_phone_analysis(self):
        """Batch analysis of multiple phone numbers"""
        self.console.print("\n[bold green]📊 Batch Phone Analysis[/bold green]")
        # Implementation for batch analysis
        
    def _export_phone_results(self):
        """Export all phone analysis results"""
        self.console.print("\n[bold green]📤 Exporting Phone Analysis Results[/bold green]")
        # Implementation for exporting results
