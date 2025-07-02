# KaliOSINT Installation Guide

This guide will help you install and set up KaliOSINT on your system.

## 📋 System Requirements

### Supported Operating Systems

- **Kali Linux** (Recommended)
- **Ubuntu 20.04+**
- **Debian 10+**
- **macOS 10.15+**
- **Windows 10+** (Limited support)

### Hardware Requirements

- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space
- **CPU**: Any modern x64 processor
- **Network**: Internet connection for API calls

### Software Requirements

- **Python**: 3.8 or higher
- **pip**: Latest version
- **git**: For cloning the repository

## 🚀 Quick Installation

### Method 1: Automated Installer (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint

# Run the automated installer
python scripts/install.py
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint

# Install Python dependencies
pip install -r requirements.txt

# Set up configuration
cp config/api_keys.json.template ~/.kaliosint/config/api_keys.json

# Run KaliOSINT
python main.py
```

### Method 3: Docker Installation

```bash
# Build the Docker image
docker build -t kaliosint .

# Run the container
docker run -it --rm kaliosint

# With persistent data
docker run -it --rm -v ~/.kaliosint:/root/.kaliosint kaliosint
```

## 🔧 Detailed Installation Steps

### Step 1: Check Prerequisites

```bash
# Check Python version (must be 3.8+)
python --version

# Check pip version
pip --version

# Update pip if needed
pip install --upgrade pip
```

### Step 2: Clone Repository

```bash
# Using HTTPS
git clone https://github.com/yourusername/kaliosint.git

# Using SSH
git clone git@github.com:yourusername/kaliosint.git

# Navigate to directory
cd kaliosint
```

### Step 3: Create Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import rich, requests, phonenumbers; print('Dependencies installed successfully')"
```

### Step 5: Configure KaliOSINT

```bash
# Create configuration directory
mkdir -p ~/.kaliosint/config

# Copy configuration templates
cp config/default_config.json ~/.kaliosint/config/config.json
cp config/api_keys.json.template ~/.kaliosint/config/api_keys.json

# Edit API keys (see API Configuration section)
nano ~/.kaliosint/config/api_keys.json
```

### Step 6: Verify Installation

```bash
# Run KaliOSINT
python main.py

# Should display the main menu
```

## 🔑 API Configuration

### Required APIs (Optional but Recommended)

1. **Shodan** - Internet-connected device search
   - Get API key: https://account.shodan.io/
   - Free tier: 100 queries/month

2. **Censys** - Internet scanning
   - Get API credentials: https://censys.io/register
   - Free tier: 250 queries/month

3. **NumVerify** - Phone number validation
   - Get API key: https://numverify.com/signup
   - Free tier: 1000 requests/month

4. **HaveIBeenPwned** - Breach data
   - Get API key: https://haveibeenpwned.com/API/Key
   - Paid service

### API Configuration File

Edit `~/.kaliosint/config/api_keys.json`:

```json
{
  "shodan_api": "your_shodan_api_key_here",
  "censys_api_id": "your_censys_id_here",
  "censys_api_secret": "your_censys_secret_here",
  "numverify_api": "your_numverify_key_here",
  "hibp_api": "your_hibp_key_here"
}
```

## 🐧 Kali Linux Specific Setup

### Installing on Kali Linux

```bash
# Update package list
sudo apt update

# Install Python and pip (if not already installed)
sudo apt install python3 python3-pip python3-venv git

# Install additional tools
sudo apt install nmap whois dnsutils

# Clone and install KaliOSINT
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint
python scripts/install.py
```

### Adding to PATH (Optional)

```bash
# Add KaliOSINT to PATH
echo 'export PATH="$PATH:$(pwd)"' >> ~/.bashrc
source ~/.bashrc

# Now you can run from anywhere
kaliosint
```

## 🪟 Windows Installation

### Prerequisites

1. **Install Python 3.8+** from https://python.org
2. **Install Git** from https://git-scm.com
3. **Open PowerShell** as Administrator

### Installation Steps

```powershell
# Clone repository
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint

# Install dependencies
pip install -r requirements.txt

# Run installer
python scripts/install.py

# Run KaliOSINT
python main.py
```

### Windows Subsystem for Linux (WSL)

For better compatibility, consider using WSL:

```bash
# Install WSL2 and Ubuntu
wsl --install -d Ubuntu

# Follow Linux installation steps in WSL
```

## 🐳 Docker Installation

### Using Pre-built Image

```bash
# Pull the image
docker pull kaliosint/kaliosint:latest

# Run the container
docker run -it --rm kaliosint/kaliosint:latest
```

### Building from Source

```bash
# Clone repository
git clone https://github.com/yourusername/kaliosint.git
cd kaliosint

# Build image
docker build -t kaliosint .

# Run container
docker run -it --rm kaliosint

# With volume mounting for persistent data
docker run -it --rm -v ~/.kaliosint:/root/.kaliosint kaliosint
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  kaliosint:
    build: .
    volumes:
      - ~/.kaliosint:/root/.kaliosint
    stdin_open: true
    tty: true
```

```bash
# Run with docker-compose
docker-compose up
```

## 🔧 Troubleshooting

### Common Issues

#### Python Version Error

```bash
# Error: Python 3.8+ required
# Solution: Update Python
sudo apt install python3.9 python3.9-pip
python3.9 main.py
```

#### Permission Denied

```bash
# Error: Permission denied
# Solution: Check file permissions
chmod +x kaliosint
ls -la kaliosint
```

#### Module Not Found

```bash
# Error: ModuleNotFoundError
# Solution: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### API Key Issues

```bash
# Error: Invalid API key
# Solution: Check API key configuration
cat ~/.kaliosint/config/api_keys.json
```

### Debug Mode

```bash
# Run in debug mode for verbose output
python main.py --debug

# Check logs
tail -f ~/.kaliosint/logs/kaliosint.log
```

### Getting Help

If you encounter issues:

1. **Check logs**: `~/.kaliosint/logs/`
2. **Run in debug mode**: `python main.py --debug`
3. **Check GitHub issues**: https://github.com/yourusername/kaliosint/issues
4. **Create new issue** with error details

## 📊 Verification

### Test Installation

```bash
# Run basic tests
python -m pytest tests/ -v

# Test specific module
python -c "from src.core.main import KaliOSINT; print('Installation successful')"

# Check configuration
python main.py --check-config
```

### Performance Test

```bash
# Run performance tests
python scripts/benchmark.py

# Monitor resource usage
htop  # Linux
Task Manager  # Windows
```

## 🔄 Updating

### Update KaliOSINT

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run update script
python scripts/update.py
```

### Backup Configuration

```bash
# Backup your configuration before updating
cp -r ~/.kaliosint ~/.kaliosint.backup

# Restore if needed
cp -r ~/.kaliosint.backup ~/.kaliosint
```

## 📚 Next Steps

After installation:

1. **Configure API keys** for enhanced functionality
2. **Read the usage guide**: `docs/usage.md`
3. **Explore examples**: `docs/examples/`
4. **Join the community**: GitHub Discussions
5. **Start investigating** responsibly!

---

**Need help? Check our [GitHub Issues](https://github.com/yourusername/kaliosint/issues) or [Discussions](https://github.com/yourusername/kaliosint/discussions)**
