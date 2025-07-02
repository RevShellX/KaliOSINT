# 🚀 KaliOSINT Quick Start Guide

## Installation & Setup

1. **Download and Setup:**
```bash
git clone https://github.com/your-username/kaliosint.git
cd kaliosint
python3 setup.py
```

2. **Launch the Tool:**
```bash
python3 kaliosint.py
# or use the launcher
chmod +x kaliosint.sh
./kaliosint.sh
```

## 🎯 Common Investigation Scenarios

### 1. Website Investigation
```
Target: example.com

Steps:
1. Main Menu → Domain & IP Investigation
2. WHOIS Lookup → example.com
3. DNS Records Analysis → example.com  
4. Subdomain Enumeration → example.com
5. Website Analysis → Technology Stack
6. Security Headers Check

Results: Complete domain profile with subdomains and tech stack
```

### 2. Email Investigation
```
Target: john.doe@company.com

Steps:
1. Main Menu → Email Investigation
2. Email Validation → john.doe@company.com
3. Breach Data Search → john.doe@company.com
4. Domain Analysis → company.com
5. Social Media Search → john.doe@company.com

Results: Email validity, breach history, social media presence
```

### 3. Social Media Investigation
```
Target: johndoe123

Steps:
1. Main Menu → Social Media Intelligence
2. Username Search → johndoe123
3. Check results across 20+ platforms
4. Analyze found profiles individually

Results: Social media footprint across platforms
```

### 4. Network Reconnaissance
```
Target: 192.168.1.0/24

Steps:
1. Main Menu → Network Scanning
2. Network Discovery → 192.168.1.0/24
3. Quick Port Scan → [discovered IPs]
4. Service Detection → [open ports]

Results: Network topology and service inventory
```

### 5. Phone Number Investigation
```
Target: +1-555-123-4567

Steps:
1. Main Menu → Phone Number Analysis
2. Phone Validation → +1-555-123-4567
3. Carrier Information → +1-555-123-4567
4. Geolocation → +1-555-123-4567
5. Social Media Search → +1-555-123-4567

Results: Phone validation, carrier, location, social presence
```

## 🔧 API Configuration Examples

### Shodan Setup
1. Visit https://shodan.io/ and create account
2. Get API key from account dashboard
3. In KaliOSINT: Configuration → Shodan API Key
4. Test: Search Intelligence → Shodan Search

### Have I Been Pwned Setup
1. Visit https://haveibeenpwned.com/API/Key
2. Purchase API key
3. In KaliOSINT: Configuration → HaveIBeenPwned API Key
4. Test: Email Investigation → Breach Data Search

## 📊 Output Examples

### WHOIS Lookup Results
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                WHOIS Data                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Domain Name      │ example.com                                                │
│ Registrar        │ Example Registrar Inc.                                     │
│ Creation Date    │ 1995-08-14 04:00:00                                        │
│ Expiration Date  │ 2024-08-13 04:00:00                                        │
│ Updated Date     │ 2023-08-12 03:15:22                                        │
│ Status           │ ['clientDeleteProhibited', 'clientTransferProhibited']     │
│ Name Servers     │ ['A.IANA-SERVERS.NET', 'B.IANA-SERVERS.NET']             │
│ Organization     │ Internet Assigned Numbers Authority                        │
│ Country          │ US                                                         │
│ Email            │ ['admin@example.com']                                      │
└──────────────────┴────────────────────────────────────────────────────────────┘
```

### Username Search Results
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        Username Search Results for 'johndoe'                 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Platform     │ URL                               │ Status        │
├──────────────┼───────────────────────────────────┼───────────────┤
│ GitHub       │ https://github.com/johndoe        │ Found         │
│ Twitter      │ https://twitter.com/johndoe       │ Found         │
│ Instagram    │ https://instagram.com/johndoe     │ Not Found     │
│ LinkedIn     │ https://linkedin.com/in/johndoe   │ Found         │
│ Reddit       │ https://reddit.com/user/johndoe   │ Found         │
└──────────────┴───────────────────────────────────┴───────────────┘

Found 4 potential matches out of 20 platforms
```

### Port Scan Results
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            Open Ports on 192.168.1.1                        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Port │ Protocol │ State │ Service │ Version           │
├──────┼──────────┼───────┼─────────┼───────────────────┤
│ 22   │ tcp      │ open  │ ssh     │ OpenSSH 8.2       │
│ 80   │ tcp      │ open  │ http    │ Apache 2.4.41     │
│ 443  │ tcp      │ open  │ https   │ Apache 2.4.41     │
│ 8080 │ tcp      │ open  │ http    │ Jetty 9.4.39      │
└──────┴──────────┴───────┴─────────┴───────────────────┘
```

## 🔍 Advanced Search Techniques

### Google Dorking Examples
```
# Find specific file types
site:example.com filetype:pdf
site:example.com filetype:doc OR filetype:docx

# Find login pages
site:example.com inurl:login
site:example.com intitle:"login"

# Find configuration files
site:example.com filetype:xml OR filetype:conf
site:example.com inurl:config

# Find employee information
site:linkedin.com "works at Example Company"
site:example.com "@example.com"

# Find exposed data
site:pastebin.com "example.com"
site:github.com "example.com" password
```

### Shodan Search Queries
```
# Find devices by organization
org:"Example Corp"

# Find specific services
product:"Apache httpd"
port:22 country:US

# Find vulnerable systems
vuln:CVE-2021-44228
ssl.cert.subject.cn:"example.com"

# IoT devices
product:"webcam"
"default password"
```

## 📁 File Structure After Installation

```
kaliosint/
├── kaliosint.py              # Main application
├── osint_modules.py          # Extended functionality
├── social_media_osint.py     # Social media tools
├── setup.py                  # Installation script
├── kaliosint.sh              # Launcher script
├── requirements.txt          # Python dependencies
├── config.json               # Default configuration
├── README.md                 # Documentation
└── examples.md               # This file

~/.kaliosint/                 # User configuration
├── config.json               # User settings
├── results/                  # Investigation results
│   ├── whois_example_com_*.json
│   ├── dns_example_com_*.json
│   └── ...
└── logs/                     # Application logs
    └── kaliosint.log
```

## 🚨 Ethical Guidelines Reminder

### ✅ Acceptable Use
- Testing your own systems
- Authorized penetration testing
- Security research with permission
- Educational purposes
- OSINT on publicly available information

### ❌ Prohibited Use
- Unauthorized system access
- Privacy invasion
- Malicious activities
- Harassment or stalking
- Illegal data collection

### 🛡️ Best Practices
- Always get written permission
- Document your methodology
- Respect rate limits and ToS
- Use VPN for sensitive research
- Keep API keys secure
- Regular tool updates

## 🔧 Troubleshooting Common Issues

### Dependencies Issues
```bash
# Fix missing packages
pip3 install --upgrade -r requirements.txt

# Install system tools (Kali Linux)
sudo apt install nmap whois dnsutils
```

### Permission Errors
```bash
# Fix script permissions
chmod +x kaliosint.sh
chmod +x kaliosint.py

# Create config directory
mkdir -p ~/.kaliosint/results ~/.kaliosint/logs
```

### API Errors
- Check API key validity
- Verify internet connection
- Check rate limits
- Review API documentation

### Network Issues
- Check firewall settings
- Verify target accessibility
- Use different DNS servers
- Try different user agents

## 📞 Getting Help

### Documentation
- README.md - Complete feature overview
- This file - Quick start and examples
- Code comments - Implementation details

### Community Support
- GitHub Issues - Bug reports and feature requests
- Wiki Pages - Detailed guides and tutorials
- Discussions - Community Q&A

### Professional Use
- Consider commercial OSINT platforms for enterprise use
- Implement proper logging and audit trails
- Follow organizational security policies
- Regular security assessments

---

**Happy Investigating! 🕵️‍♂️**

Remember: With great power comes great responsibility. Use KaliOSINT ethically and legally.
