## Automated Network Scanner - Complete Analysis & macOS Setup Guide

I've thoroughly examined all files in your Automated Network Scanner project. Here's a detailed breakdown and step-by-step setup instructions for macOS.

***

## PROJECT OVERVIEW

Your Automated Network Scanner is a Python-based network monitoring application with three main components:

### **Core Architecture:**
1. **1manufacturer_lookup.py** - MAC address manufacturer lookup utility
2. **2scanner.py** - Network scanning engine
3. **3app.py** - Flask web dashboard API
4. **dashboard.html** - Web interface for displaying active devices
5. **config.json** - Configuration file with network settings and alert recipients
6. **Supporting files** - Log file, systemd service file, data storage files

***

## DETAILED FILE ANALYSIS

### **1. 1manufacturer_lookup.py**[1]
**Purpose:** Identifies device manufacturers from MAC addresses

**Key Features:**
- Local MAC prefix dictionary (Cisco, Apple, Samsung)
- Primary function: `lookup_manufacturer_local()` - queries local dictionary
- Secondary function: `lookup_manufacturer_api()` - calls external API (api.macvendors.com)
- Combined function: `lookup_manufacturer_combined()` - tries local first, then API fallback
- Error handling with logging

### **2. 2scanner.py**[1]
**Purpose:** Performs network scanning and detects devices

**Key Components:**
- Imports nmap, scapy (ARP scanning), email/SMTP libraries
- `load_config()` - reads config.json settings
- `scan_network()` - nmap ping scan for device discovery
- `arp_scan()` - scapy-based ARP scanning for MAC/IP address resolution
- `send_email_alert()` - sends email notifications for unauthorized devices
- `send_sms_alert()` - sends SMS alerts via email-to-SMS gateway
- `is_unauthorized()` - checks device against whitelist
- `write_current_devices()` - saves discovered devices to JSON for API
- Main loop: continuous scanning with configurable interval

### **3. 3app.py**[1]
**Purpose:** Flask web server for dashboard visualization

**Endpoints:**
- `GET /` - serves dashboard.html
- `GET /api/devices` - returns current_devices.json as JSON

**Configuration:**
- Runs on 0.0.0.0:5000 (all interfaces, port 5000)
- Debug mode enabled

### **4. config.json**[1]
**Configuration Settings:**
- `target`: "192.168.160.0/24" (network to scan)
- `scan_interval`: 60 seconds
- `whitelist`: MAC addresses of authorized devices
- `default_gateway`: 192.168.160.191 (excluded from alerts)
- `smtp`: Gmail configuration (sender credentials)
- `sms_gateways`: Airtel SMS gateway mapping
- `alert_recipients`: email and SMS recipient info
- `restricted_ports`:  (ports to monitor)

### **5. dashboard.html**[1]
**Purpose:** Real-time device monitoring interface

**Features:**
- HTML5 page with JavaScript
- `fetchDevices()` function - fetches from /api/devices every 5 seconds
- Displays active devices with IP, MAC, and status
- Responsive design with device list display

### **6. Supporting Files**
- **current_devices.json** - Runtime data file storing discovered devices
- **network_scanner.log** - Application logs
- **network_scanner.service** - Systemd service file for Linux deployment
- **Project_Files_Directory** - Binary archive file (806 bytes)
- **Automated Network Scanner.pptx** - Project presentation

***

## STEP-BY-STEP SETUP GUIDE FOR MACOS

### **STEP 1: Prerequisites Installation**

```bash
# Update Homebrew
brew update

# Install Python 3 (if not already installed)
brew install python@3.11

# Verify Python installation
python3 --version

# Install system dependencies for network scanning
brew install nmap

# Verify nmap installation
nmap --version
```

### **STEP 2: Create Project Directory**

```bash
# Create project folder
mkdir -p ~/projects/AutomatedNetworkScanner
cd ~/projects/AutomatedNetworkScanner

# Download your project files from Google Drive to this folder
# Manually place: 1manufacturer_lookup.py, 2scanner.py, 3app.py, 
# config.json, dashboard.html in this directory
```

### **STEP 3: Create Python Virtual Environment**

```bash
# Navigate to project directory
cd ~/projects/AutomatedNetworkScanner

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) prefix in terminal)
```

### **STEP 4: Install Python Dependencies**

Create a `requirements.txt` file with the following content:

```txt
Flask==2.3.3
python-nmap==0.0.1
scapy==2.5.0
requests==2.31.0
```

Then install:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **STEP 5: Create Project Structure**

```bash
# Create templates folder for HTML files
mkdir -p templates
mkdir -p logs

# Move dashboard.html to templates folder
# If you have the file in current directory:
# mv dashboard.html templates/

# Create empty log file
touch logs/network_scanner.log
```

### **STEP 6: Configure the Application**

Edit `config.json` with your network details:

```json
{
    "target": "192.168.1.0/24",  // Change to YOUR network
    "scan_interval": 60,
    "whitelist": [
        "AC:2B:6E:37:8C:8C",
        "c8:9f:0c:7e:a3:b3"
    ],
    "default_gateway": "192.168.1.1",  // Change to YOUR gateway
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587,
        "username": "your-email@gmail.com",
        "password": "your-app-password"  // Use Gmail App Password
    },
    "sms_gateways": {
        "Airtel": "your-number@airtelmail.com"
    },
    "alert_recipients": {
        "email": "your-email@gmail.com",
        "sms": "Airtel"
    },
    "restricted_ports": [22, 23, 3389]
}
```

### **STEP 7: Configure Gmail for SMTP (Important)**

1. Enable 2-Factor Authentication on your Google Account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the generated 16-character password in config.json

### **STEP 8: Find Your Network Information**

```bash
# Find your local IP and network
ifconfig | grep inet

# Find your default gateway
netstat -nr | grep default

# Find connected devices and their MAC addresses
arp -a
```

### **STEP 9: Update MAC Address Whitelist**

```bash
# Get your device's MAC address
ifconfig en0 | grep ether

# Add all trusted device MAC addresses to config.json whitelist
```

### **STEP 10: Test Individual Components**

#### Test manufacturer lookup:
```bash
python3 1manufacturer_lookup.py
```

#### Test Flask app:
```bash
python3 3app.py
# Visit: http://localhost:5000
# The dashboard should load with an empty device list
```

### **STEP 11: Test Network Scanner (requires sudo)**

```bash
# Test basic network scan with nmap
sudo nmap -sn 192.168.1.0/24

# Test ARP scan capability
sudo python3 -c "from scapy.all import ARP, Ether, srp; print('Scapy is working')"

# Run scanner (requires root privileges)
sudo python3 2scanner.py
```

### **STEP 12: Run the Application**

#### Terminal 1 - Run Scanner (requires sudo):
```bash
source venv/bin/activate
sudo python3 2scanner.py
```

#### Terminal 2 - Run Flask Server:
```bash
source venv/bin/activate
python3 3app.py
```

#### Terminal 3 - Access Dashboard:
```bash
open http://localhost:5000
```

### **STEP 13: Grant Required Permissions**

For full functionality without repeatedly entering password:

```bash
# Create sudoers entry for nmap (optional, for advanced users)
sudo visudo
# Add line: %admin ALL=(ALL) NOPASSWD: /usr/local/bin/nmap
```

### **STEP 14: Create a Run Script** (Optional)

Create `run.sh`:

```bash
#!/bin/bash
source venv/bin/activate
echo "Starting Network Scanner..."
echo "Terminal 1: Scanner (sudo required)"
sudo python3 2scanner.py &
SCANNER_PID=$!
echo "Terminal 2: Flask App"
sleep 2
python3 3app.py &
APP_PID=$!
echo "Opening Dashboard..."
sleep 2
open http://localhost:5000
echo "Press Ctrl+C to stop"
wait
```

Make it executable:
```bash
chmod +x run.sh
./run.sh
```

***

## IMPORTANT NOTES FOR MACOS

1. **Network Scanning**: Network scanning requires elevated privileges. You may be prompted for your password when running 2scanner.py.

2. **Firewall**: macOS may ask for permission to access the network. Click "Allow" when prompted.

3. **Python Path**: Ensure you're using `python3` not `python` to avoid Python 2 compatibility issues.

4. **Flask Port**: Port 5000 is default. If blocked, change in 3app.py:
   ```python
   app.run(host='0.0.0.0', port=8080, debug=True)
   ```

5. **Email Alerts**: You MUST use Gmail App Passwords, not your regular password.

6. **Network Range**: Adjust "target" in config.json to your actual network CIDR notation.

***

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "nmap not found" | `brew install nmap` |
| "Permission denied" | Run with `sudo python3 2scanner.py` |
| "Module not found" | Ensure venv is activated: `source venv/bin/activate` |
| "Port 5000 already in use" | Change port in 3app.py or kill process: `lsof -ti:5000 \| xargs kill` |
| "Email alerts not sending" | Use Gmail App Password, enable 2FA |
| "No devices detected" | Check network range in config.json matches your subnet |

***

This comprehensive setup ensures your Automated Network Scanner runs smoothly on macOS with all scanning, alerting, and visualization capabilities fully functional.

[1](https://drive.google.com/drive/u/1/folders/1oSTjpmnO5ZQC4_NYFoaY_-1pbDAbcIOD)