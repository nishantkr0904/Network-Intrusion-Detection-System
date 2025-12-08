import logging
import requests

# Local dictionary of MAC prefixes (first 8 characters)
MAC_MANUFACTURERS = {
    "00:1A:2B": "Cisco Systems",
    "00:1B:63": "Apple, Inc.",
    "F4:5C:89": "Samsung Electronics"
    # Add more mappings relevant to your network devices here.
}

def lookup_manufacturer_local(mac):
    """
    Looks up the manufacturer from a local dictionary using the MAC address prefix.
    """
    if mac == "N/A":
        return "Unknown"
    # Normalize MAC to upper-case and extract the first 8 characters (prefix)
    prefix = mac.upper()[0:8]  # e.g., "00:1A:2B"
    return MAC_MANUFACTURERS.get(prefix, "Unknown")

def lookup_manufacturer_api(mac):
    """
    Uses a free online API to get the manufacturer information for a MAC address.
    """
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unknown"
    except Exception as e:
        logging.error("Manufacturer API lookup failed: %s", e)
        return "Unknown"

def lookup_manufacturer_combined(mac):
    """
    First, tries to find the manufacturer from the local dictionary.
    If not found, falls back to the free API lookup.
    """
    manufacturer = lookup_manufacturer_local(mac)
    if manufacturer == "Unknown":
        manufacturer = lookup_manufacturer_api(mac)
    return manufacturer

# For testing purposes:
if __name__ == "__main__":
    test_macs = [
        "00:1A:2B:12:34:56",  # Expected: "Cisco Systems" from local dictionary
        "F4:5C:89:AB:CD:EF",  # Expected: "Samsung Electronics" from local dictionary
        "12:34:56:78:9A:BC"   # Not in local dictionary; should try API lookup
    ]
    for mac in test_macs:
        manufacturer = lookup_manufacturer_combined(mac)
        print(f"MAC: {mac} --> Manufacturer: {manufacturer}")
