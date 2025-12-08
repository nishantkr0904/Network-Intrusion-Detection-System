# scanner.py

# Step 3.1: Import Libraries and Load Configuration
import nmap
import time
import json
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from manufacturer_lookup import lookup_manufacturer_combined
import os

# Optionally, import scapy if deeper packet analysis is needed
# from scapy.all import ARP, Ether, srp

def load_config(config_file="config.json"):
    with open(config_file) as f:
        return json.load(f)

# Step 3.2: Set Up Logging
logging.basicConfig(
    filename='network_scanner.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Step 3.3: Create a Basic Network Scanner Function
def scan_network(target='192.168.160.0/24'):
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-sn')  # Ping scan only
    devices = []
    for host in nm.all_hosts():
        device = {
            'ip': host,
            'status': nm[host].state(),
            'mac': nm[host]['addresses'].get('mac', 'N/A')
        }
        devices.append(device)
    return devices

from scapy.all import ARP, Ether, srp

def arp_scan(target):
    """
    Uses scapy to perform an ARP scan on the target network.
    Returns a list of devices with their IP and MAC addresses.
    """
    # Create ARP packet to ask for devices in the target subnet
    arp = ARP(pdst=target)
    # Create Ether broadcast packet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the packets
    packet = ether / arp
    # Send the packet and capture responses (timeout=3 sec)
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'status': 'up'
        })
    return devices

# Step 3.5: Define Alert Triggering Functions
def send_email_alert(subject, body, config):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config["smtp"]["username"]
    msg['To'] = config["alert_recipients"]["email"]

    try:
        server = smtplib.SMTP(config["smtp"]["server"], config["smtp"]["port"])
        server.starttls()
        server.login(config["smtp"]["username"], config["smtp"]["password"])
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()
        logging.info("Alert email sent successfully.")
    except Exception as e:
        logging.error("Failed to send alert email: %s", e)

def send_sms_alert(message, config):
    sms_address = config["sms_gateways"].get(config["alert_recipients"]["sms"], None)
    if not sms_address:
        logging.error("No SMS gateway configured for the given carrier.")
        return

    msg = MIMEText(message)
    msg['Subject'] = "Network Alert"
    msg['From'] = config["smtp"]["username"]
    msg['To'] = sms_address

    try:
        server = smtplib.SMTP(config["smtp"]["server"], config["smtp"]["port"])
        server.starttls()
        server.login(config["smtp"]["username"], config["smtp"]["password"])
        server.sendmail(msg['From'], [sms_address], msg.as_string())
        server.quit()
        logging.info("Alert SMS sent successfully.")
    except Exception as e:
        logging.error("Failed to send alert SMS: %s", e)

# Step 3.6: Check for Unauthorized Devices
def is_unauthorized(device, config):
    default_gateway = config.get("default_gateway", "192.168.160.191")
    if device['ip'] == default_gateway:
        return False
    return device['mac'] not in config.get("whitelist", [])

# NEW: Write Current Devices to JSON File
def write_current_devices(devices, output_file="current_devices.json"):
    with open(output_file, "w") as f:
        json.dump(devices, f, indent=4)

# Step 3.7: Main Loop
if __name__ == "__main__":
    config = load_config()
    target = config.get("target", "192.168.160.0/24")
    while True:
        # First, use nmap ping scan
        devices = scan_network(target)
        
        # If no devices detected by nmap, try ARP scan using scapy
        if not devices:
            devices = arp_scan(target)
        
        # Add manufacturer lookup to each device
        for device in devices:
            manufacturer = lookup_manufacturer_combined(device['mac'])
            device['manufacturer'] = manufacturer

            logging.info("IP: %s, MAC: %s, Manufacturer: %s, Status: %s",
                         device['ip'], device['mac'], manufacturer, device['status'])
            
            if is_unauthorized(device, config):
                alert_subject = "Unauthorized Device Detected"
                alert_body = (f"Device {device['ip']} with MAC {device['mac']} "
                              f"({manufacturer}) is not whitelisted.")
                send_email_alert(alert_subject, alert_body, config)
                send_sms_alert(alert_body, config)

        # Write current devices to JSON for the Flask API
        write_current_devices(devices)
        print("Devices found:", devices)
        time.sleep(config.get("scan_interval", 60))

