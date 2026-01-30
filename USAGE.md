# Usage Guide

This comprehensive guide covers all aspects of using wlfwifi, from basic operations to advanced scenarios. Includes real-world examples, tips, and best practices.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Command Line Interface](#command-line-interface)
  - [All Options](#all-options)
  - [Option Details](#option-details)
- [Basic Usage Examples](#basic-usage-examples)
- [Step-by-Step Workflows](#step-by-step-workflows)
  - [Workflow 1: Discovering Networks](#workflow-1-discovering-networks)
  - [Workflow 2: WPA/WPA2 Handshake Capture](#workflow-2-wpawpa2-handshake-capture)
  - [Workflow 3: WPS PIN Attack](#workflow-3-wps-pin-attack)
  - [Workflow 4: WEP Cracking](#workflow-4-wep-cracking)
- [Advanced Usage](#advanced-usage)
  - [Channel Locking](#channel-locking)
  - [Verbose Mode](#verbose-mode)
  - [Monitor Mode Management](#monitor-mode-management)
- [Working with Capture Files](#working-with-capture-files)
- [Best Practices](#best-practices)
- [Tips and Tricks](#tips-and-tricks)
- [Common Scenarios](#common-scenarios)
- [Interpreting Output](#interpreting-output)
- [Troubleshooting](#troubleshooting)
- [Legal Considerations](#legal-considerations)

---

## Quick Start

```bash
# Basic scan with automatic interface detection
sudo wlfwifi

# Specify interface
sudo wlfwifi -i wlan0

# Specify interface and channel
sudo wlfwifi -i wlan0 -c 6

# Verbose output for debugging
sudo wlfwifi -i wlan0 -v
```

---

## Command Line Interface

### All Options

```
Usage: wlfwifi [-h] [-i INTERFACE] [-c CHANNEL] [-v]

wlfwifi: Automated wireless network auditor

Options:
  -h, --help                    Show help message and exit
  -i, --interface INTERFACE     Wireless interface to use
  -c, --channel CHANNEL         Channel to scan/attack
  -v, --verbose                 Enable verbose output
```

### Option Details

#### `-i, --interface`

Specifies the wireless interface to use for scanning and attacks.

```bash
# Examples
sudo wlfwifi -i wlan0          # Standard interface name
sudo wlfwifi -i wlan0mon       # Interface already in monitor mode
sudo wlfwifi -i wlp2s0         # PCI interface naming
sudo wlfwifi --interface eth0  # Long form (will fail - not wireless)
```

**Finding your interface:**
```bash
# List all network interfaces
ip link show

# List wireless interfaces only
iwconfig 2>/dev/null | grep -E "^[a-z]"

# Detailed wireless info
iw dev
```

#### `-c, --channel`

Locks scanning to a specific channel. Useful when you know your target's channel.

```bash
# 2.4 GHz channels (1-14)
sudo wlfwifi -i wlan0 -c 6

# 5 GHz channels
sudo wlfwifi -i wlan0 -c 36
sudo wlfwifi -i wlan0 -c 149
```

**Channel Reference:**

| Band | Channels | Common Channels |
|------|----------|-----------------|
| 2.4 GHz | 1-14 | 1, 6, 11 (non-overlapping) |
| 5 GHz | 36-64, 100-144, 149-165 | 36, 40, 44, 48, 149, 153, 157, 161 |

#### `-v, --verbose`

Enables detailed logging for debugging and analysis.

```bash
sudo wlfwifi -i wlan0 -v
```

**Verbose output includes:**
- Commands being executed
- Process status and timing
- Detailed error messages
- Network discovery progress
- Attack progress updates

---

## Basic Usage Examples

### Example 1: Simple Network Discovery

```bash
# Start scanning on wlan0
sudo wlfwifi -i wlan0
```

**What happens:**
1. wlfwifi puts wlan0 into monitor mode
2. Scans all channels for wireless networks
3. Displays discovered networks with:
   - ESSID (network name)
   - BSSID (access point MAC)
   - Channel
   - Encryption type
   - Signal strength
   - WPS status

### Example 2: Target Specific Channel

```bash
# Scan only channel 6
sudo wlfwifi -i wlan0 -c 6
```

**Use cases:**
- You already know target's channel
- Reducing scan time
- Avoiding interference on other channels

### Example 3: Debug Mode

```bash
# Full verbose output
sudo wlfwifi -i wlan0 -c 11 -v
```

**Useful for:**
- Troubleshooting issues
- Understanding what commands are running
- Learning how wlfwifi works

### Example 4: Running as Python Module

```bash
# Alternative invocation
sudo python3 -m wlfwifi -i wlan0
```

---

## Step-by-Step Workflows

### Workflow 1: Discovering Networks

**Goal:** Survey wireless networks in your environment

**Steps:**

1. **Identify your wireless interface**
   ```bash
   iwconfig
   # Look for interface like wlan0, wlp2s0, etc.
   ```

2. **Kill interfering processes**
   ```bash
   sudo airmon-ng check kill
   ```

3. **Start wlfwifi**
   ```bash
   sudo wlfwifi -i wlan0
   ```

4. **View discovered networks**
   
   Output shows:
   ```
   NUM  ESSID              BSSID              CH   ENC     PWR   WPS
   ---  -----              -----              --   ---     ---   ---
   1    HomeNetwork        00:11:22:33:44:55  6    WPA2    -45   Yes
   2    OfficeWiFi         11:22:33:44:55:66  11   WPA2    -60   No
   3    GuestNet           22:33:44:55:66:77  1    WPA     -70   Yes
   4    OldRouter          33:44:55:66:77:88  6    WEP     -55   No
   ```

5. **Interpret results**
   - **PWR**: Signal strength (closer to 0 is stronger)
   - **WPS**: Vulnerable to WPS attacks if "Yes"
   - **ENC**: Encryption type (WEP is weakest)

---

### Workflow 2: WPA/WPA2 Handshake Capture

**Goal:** Capture a 4-way handshake for offline cracking

**Prerequisites:**
- Target network with connected clients
- Good signal strength (-70 dBm or better)

**Steps:**

1. **Start wlfwifi targeting the network**
   ```bash
   sudo wlfwifi -i wlan0 -c 6
   ```

2. **Select target network** (when prompted)
   ```
   Select target(s) [1-4, all]: 1
   ```

3. **wlfwifi automatically:**
   - Monitors target network
   - Sends deauthentication to clients
   - Captures handshake when client reconnects
   - Saves capture file

4. **Handshake captured!**
   ```
   [+] Handshake captured: hs/HomeNetwork_001122334455.cap
   ```

5. **Crack offline with wordlist**
   ```bash
   aircrack-ng -w /path/to/wordlist.txt hs/HomeNetwork_*.cap
   ```

**Tips:**
- More clients = faster handshake capture
- Strong signal improves success rate
- Be patient - may take several minutes

---

### Workflow 3: WPS PIN Attack

**Goal:** Exploit WPS vulnerabilities to recover WPA password

**Prerequisites:**
- Target with WPS enabled (shows "Yes" in scan)
- Target not WPS-locked

**Steps:**

1. **Scan for WPS-enabled networks**
   ```bash
   sudo wlfwifi -i wlan0
   ```

2. **Select WPS-enabled target**
   ```
   # Look for "WPS: Yes" in output
   Select target(s): 3  # GuestNet with WPS
   ```

3. **Attack begins automatically**
   ```
   [+] Starting WPS attack on GuestNet
   [+] Trying PIN: 12345670
   [+] Trying PIN: 12345671
   ...
   ```

4. **Success!**
   ```
   [+] WPS PIN found: 12345670
   [+] WPA PSK: MySecretPassword123
   ```

**Timing:**
- Reaver attack: 4-10 hours (brute force all PINs)
- Pixie Dust attack: 1-5 minutes (if vulnerable)

---

### Workflow 4: WEP Cracking

**Goal:** Crack WEP encryption (deprecated, but still found)

**Prerequisites:**
- Target using WEP encryption
- Traffic on the network

**Steps:**

1. **Find WEP network**
   ```bash
   sudo wlfwifi -i wlan0
   ```
   
   Look for `ENC: WEP`

2. **Select WEP target**
   ```
   Select target(s): 4  # OldRouter with WEP
   ```

3. **wlfwifi captures IVs (Initialization Vectors)**
   ```
   [+] Capturing IVs: 10,000 / 50,000
   [+] Capturing IVs: 25,000 / 50,000
   ```

4. **Automatic cracking when enough IVs**
   ```
   [+] IVs captured: 50,000
   [+] Cracking WEP key...
   [+] KEY FOUND: 1A:2B:3C:4D:5E
   ```

**Tips:**
- More traffic = faster IV collection
- ARP replay speeds up the process
- 50,000-100,000 IVs typically needed

---

## Advanced Usage

### Channel Locking

Locking to a specific channel has several benefits:

```bash
# Lock to channel 6
sudo wlfwifi -i wlan0 -c 6
```

**Benefits:**
- Faster target discovery on that channel
- Less interference from other networks
- More stable connection during attacks
- Required for some specific attacks

**When to use:**
- You know target's channel from prior recon
- Targeting specific network
- Experiencing issues with channel hopping

### Verbose Mode

Enable verbose mode for detailed information:

```bash
sudo wlfwifi -i wlan0 -v
```

**Verbose output includes:**

```
[2026-01-28 10:15:32] INFO: [wlfwifi] Starting with interface=wlan0, channel=None, verbose=True
[2026-01-28 10:15:32] DEBUG: Executing: airmon-ng check kill
[2026-01-28 10:15:33] DEBUG: Executing: airmon-ng start wlan0
[2026-01-28 10:15:35] INFO: Monitor mode enabled on wlan0mon
[2026-01-28 10:15:35] DEBUG: Executing: airodump-ng -w scan --output-format csv wlan0mon
```

### Monitor Mode Management

**Enabling monitor mode manually:**
```bash
# Using airmon-ng (recommended)
sudo airmon-ng start wlan0
# Interface becomes wlan0mon

# Using iw
sudo ip link set wlan0 down
sudo iw wlan0 set monitor control
sudo ip link set wlan0 up
```

**Disabling monitor mode:**
```bash
# Using airmon-ng
sudo airmon-ng stop wlan0mon

# Restart NetworkManager
sudo systemctl start NetworkManager
```

---

## Working with Capture Files

### Capture File Locations

wlfwifi saves captures to the current directory:

```
./hs/                           # Handshake captures
./hs/NetworkName_BSSID.cap     # Individual capture files
```

### Viewing Capture Files

```bash
# List captures
ls -la hs/

# View with tshark
tshark -r hs/NetworkName_001122334455.cap

# Check for valid handshake
aircrack-ng hs/NetworkName_001122334455.cap
```

### Cracking Captured Handshakes

**With aircrack-ng:**
```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt hs/capture.cap
```

**With hashcat (faster with GPU):**
```bash
# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 hs/capture.cap

# Crack with hashcat
hashcat -m 22000 hash.hc22000 /path/to/wordlist.txt
```

**With pyrit (GPU-accelerated):**
```bash
pyrit -r hs/capture.cap -i /path/to/wordlist.txt attack_passthrough
```

---

## Best Practices

### Before Starting

1. **Ensure legal authorization**
   - Only test networks you own or have permission to test
   - Document your authorization

2. **Check your hardware**
   ```bash
   # Verify monitor mode support
   iw list | grep -A 10 "Supported interface modes"
   ```

3. **Update tools**
   ```bash
   sudo apt update && sudo apt upgrade aircrack-ng reaver
   ```

### During Scanning

1. **Start with reconnaissance**
   - Survey all networks first
   - Identify your target
   - Note channel and encryption

2. **Minimize interference**
   ```bash
   # Kill processes that might interfere
   sudo airmon-ng check kill
   ```

3. **Position for best signal**
   - Closer to target = better results
   - Avoid physical obstructions
   - External antenna helps

### During Attacks

1. **Be patient**
   - WPA handshakes may take time
   - WPS brute force takes hours

2. **Monitor progress with verbose mode**
   ```bash
   sudo wlfwifi -i wlan0 -v
   ```

3. **Know when to stop**
   - WPS locked out? Wait 60+ seconds
   - No clients? Handshake won't work
   - Weak signal? Move closer

### After Testing

1. **Restore network settings**
   ```bash
   sudo airmon-ng stop wlan0mon
   sudo systemctl start NetworkManager
   ```

2. **Secure your captures**
   - Store captures securely
   - Delete when no longer needed

3. **Document findings**
   - Note vulnerabilities found
   - Prepare remediation recommendations

---

## Tips and Tricks

### Speeding Up WPA Handshake Capture

```bash
# Target specific channel to avoid hopping
sudo wlfwifi -i wlan0 -c 6

# Use stronger signal location
# Wait for peak client activity
```

### Dealing with WPS Rate Limiting

```bash
# Some APs lock after failed attempts
# Wait 60-300 seconds between attempts
# Or try Pixie Dust attack first (much faster)
```

### Improving Scan Results

```bash
# Use external antenna
# Increase TX power (if legal in your region)
sudo iwconfig wlan0 txpower 30

# Scan longer
# Multiple passes across channels
```

### Saving Time

```bash
# If you know the channel
sudo wlfwifi -i wlan0 -c 11

# Skip WPS if not needed
# Focus on one target at a time
```

---

## Common Scenarios

### Scenario 1: Testing Your Home Network

```bash
# 1. Find your network
sudo wlfwifi -i wlan0

# 2. Note the channel
# Example: Your network on channel 6

# 3. Run targeted test
sudo wlfwifi -i wlan0 -c 6

# 4. Select your network when prompted
# 5. Attempt handshake capture or WPS test
```

### Scenario 2: Authorized Penetration Test

```bash
# 1. Get written authorization
# 2. Document scope (which networks)
# 3. Run comprehensive scan
sudo wlfwifi -i wlan0 -v

# 4. Save all output for report
sudo wlfwifi -i wlan0 -v 2>&1 | tee pentest_log.txt

# 5. Test each target methodically
```

### Scenario 3: Security Audit

```bash
# 1. Survey environment
sudo wlfwifi -i wlan0

# 2. Document:
#    - Networks with WEP (critical vulnerability)
#    - Networks with WPS enabled (high risk)
#    - Hidden networks (SSID = "")
#    - Weak signal networks (may be rogue APs)

# 3. Test specific vulnerabilities
# 4. Generate report with findings
```

---

## Interpreting Output

### Network Discovery Output

```
NUM  ESSID              BSSID              CH   ENC     PWR   WPS   CLIENTS
---  -----              -----              --   ---     ---   ---   -------
1    HomeNetwork        00:11:22:33:44:55  6    WPA2    -45   Yes   3
2    OfficeWiFi         11:22:33:44:55:66  11   WPA2    -60   No    0
3    (hidden)           22:33:44:55:66:77  1    WPA2    -70   Yes   1
4    OldRouter          33:44:55:66:77:88  6    WEP     -55   No    2
```

| Column | Meaning |
|--------|---------|
| NUM | Selection number |
| ESSID | Network name (blank = hidden) |
| BSSID | Access point MAC address |
| CH | Channel number |
| ENC | Encryption (WEP, WPA, WPA2, OPN) |
| PWR | Signal strength in dBm (closer to 0 = stronger) |
| WPS | WPS enabled (Yes/No) |
| CLIENTS | Connected client count |

### Signal Strength Guide

| PWR | Quality | Notes |
|-----|---------|-------|
| -30 to -50 | Excellent | Very close, ideal for attacks |
| -50 to -60 | Good | Reliable connection |
| -60 to -70 | Fair | May work, slower attacks |
| -70 to -80 | Weak | Unreliable, move closer |
| -80+ | Poor | Too weak, reposition |

---

## Troubleshooting

### "No networks found"

**Possible causes:**
1. Interface not in monitor mode
2. Wrong interface specified
3. No networks in range
4. Channel specification too narrow

**Solutions:**
```bash
# Check interface
iwconfig

# Verify monitor mode
sudo airmon-ng start wlan0

# Try without channel lock
sudo wlfwifi -i wlan0

# Kill interfering processes
sudo airmon-ng check kill
```

### "Handshake not captured"

**Possible causes:**
1. No clients connected to target
2. Clients not reauthorizing
3. Weak signal
4. Deauth not working

**Solutions:**
```bash
# Move closer to target
# Wait for client activity (peak hours)
# Use verbose mode to debug
sudo wlfwifi -i wlan0 -v

# Try manual deauth with aireplay-ng
```

### "WPS attack not working"

**Possible causes:**
1. WPS locked (too many attempts)
2. WPS not actually enabled
3. AP blocking PIN attempts

**Solutions:**
```bash
# Wait for lockout to clear (5-60 minutes)
# Try Pixie Dust attack (faster)
# Check if WPS really enabled with wash:
wash -i wlan0mon
```

### "Permission denied"

**Solution:**
```bash
# Always run with sudo
sudo wlfwifi -i wlan0

# Check your user is in correct groups
sudo usermod -aG netdev $USER
```

---

## Legal Considerations

### ⚠️ Important Legal Notice

**Unauthorized access to computer networks is illegal in most jurisdictions.**

### Legal Use Cases

✅ **Legal:**
- Testing your own network
- Authorized penetration testing (with written permission)
- Security research on networks you own
- Educational purposes in controlled environments

❌ **Illegal:**
- Accessing networks without authorization
- Intercepting others' network traffic
- Cracking passwords of networks you don't own
- Any activity without explicit permission

### Authorization Requirements

Before testing any network:

1. **Own the network**, or
2. **Have written authorization** from the owner that includes:
   - Specific networks to test
   - Testing methods allowed
   - Timeframe
   - Contact information
   - Signatures

### Penalties

Unauthorized network access can result in:
- Criminal prosecution
- Fines
- Imprisonment
- Civil liability
- Professional consequences

**Always get authorization first. When in doubt, don't.**

---

## Getting Help

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section
2. Use verbose mode: `-v`
3. Search [GitHub Issues](https://github.com/yourusername/wlfwifi/issues)
4. Open new issue with:
   - OS and version
   - Python version
   - Wireless card model
   - Full command used
   - Complete error output

---

## Related Documentation

- [README.md](README.md) - Project overview
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide
