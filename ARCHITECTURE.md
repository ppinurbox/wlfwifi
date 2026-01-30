# Architecture Guide

This document provides a comprehensive technical overview of wlfwifi's architecture for developers, contributors, and security researchers who want to understand, extend, or integrate with the codebase.

---

## Table of Contents

- [Overview](#overview)
- [Design Principles](#design-principles)
- [Project Structure](#project-structure)
- [Module Deep Dive](#module-deep-dive)
  - [config.py - Configuration Management](#configpy---configuration-management)
  - [models.py - Data Models](#modelspy---data-models)
  - [utils.py - Utility Functions](#utilspy---utility-functions)
  - [attacks.py - Attack Logic](#attackspy---attack-logic)
  - [core.py - Core Engine](#corepy---core-engine)
- [Data Flow](#data-flow)
- [Class Diagrams](#class-diagrams)
- [Extending wlfwifi](#extending-wlfwifi)
  - [Adding a New Attack](#adding-a-new-attack)
  - [Adding CLI Options](#adding-cli-options)
  - [Adding Utility Functions](#adding-utility-functions)
- [Testing Architecture](#testing-architecture)
- [External Tool Integration](#external-tool-integration)
- [Error Handling Strategy](#error-handling-strategy)
- [Logging System](#logging-system)
- [Future Considerations](#future-considerations)

---

## Overview

wlfwifi is designed as a modular, extensible wireless security auditing framework. The architecture emphasizes:

- **Separation of concerns**: Each module handles a specific responsibility
- **Testability**: All components are unit-testable with mock support
- **Extensibility**: New attacks and features can be added easily
- **Type safety**: Full type hints throughout the codebase

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                            │
│                    (wlfwifi.py / __main__.py)                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         config.py                                │
│              (Argument Parsing & Configuration)                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          core.py                                 │
│            (Main Engine & Workflow Orchestration)                │
└─────────────────────────────────────────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│    models.py     │ │   attacks.py     │ │    utils.py      │
│  (Data Models)   │ │ (Attack Logic)   │ │  (Helpers)       │
└──────────────────┘ └──────────────────┘ └──────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Tools                               │
│      (aircrack-ng, airodump-ng, reaver, tshark, etc.)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Single Responsibility Principle

Each module has one clear purpose:

| Module | Responsibility |
|--------|----------------|
| `config.py` | Parse CLI args, store runtime config |
| `models.py` | Define data structures |
| `utils.py` | Provide helper functions |
| `attacks.py` | Implement attack logic |
| `core.py` | Orchestrate workflow |

### 2. Dependency Injection

Configuration and dependencies are passed explicitly:

```python
# Good - explicit dependencies
def wps_check_targets(targets: List[Target], cap_file: str, verbose: bool) -> None:
    ...

# Bad - hidden global state
def wps_check_targets():
    global RUN_CONFIG
    ...
```

### 3. Abstract Base Classes for Extensibility

The `Attack` class uses ABC to ensure consistent interface:

```python
class Attack(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def RunAttack(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def EndAttack(self) -> Any:
        raise NotImplementedError
```

### 4. Type Safety

All functions and methods include type hints:

```python
def sec_to_hms(sec: int) -> str:
    """Converts integer sec to h:mm:ss format."""
    ...
```

### 5. Defensive Programming

Functions validate inputs and handle errors gracefully:

```python
def remove_file(filename: str) -> None:
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass  # File doesn't exist - that's fine
    except Exception as e:
        logging.warning(f"Failed to remove {filename}: {e}")
```

---

## Project Structure

```
wlfwifi/
├── wlfwifi.py                 # Main entry point script
│
├── wlfwifi/                   # Core package
│   ├── __init__.py            # Package exports, version info
│   ├── __main__.py            # Enables `python -m wlfwifi`
│   │
│   ├── config.py              # Configuration & CLI parsing
│   │   ├── RunConfig          # Configuration class
│   │   └── parse_args()       # Argument parser
│   │
│   ├── models.py              # Data models
│   │   ├── Target             # Wireless network
│   │   ├── Client             # Connected device
│   │   └── CapFile            # Capture file
│   │
│   ├── utils.py               # Utilities
│   │   ├── File operations    # rename, remove_file
│   │   ├── MAC handling       # get_mac, generate_random_mac
│   │   ├── Process control    # send_interrupt, program_exists
│   │   └── Formatting         # sec_to_hms, add_commas
│   │
│   ├── attacks.py             # Attack implementations
│   │   ├── Attack (ABC)       # Base class
│   │   └── wps_check_targets  # WPS detection
│   │
│   └── core.py                # Core engine
│       └── main()             # Entry point
│
├── tests/                     # Test suite (170+ tests)
│   ├── test_models.py         # Model tests
│   ├── test_config.py         # Config tests
│   ├── test_utils.py          # Utility tests
│   ├── test_attacks.py        # Attack tests
│   ├── test_core.py           # Core tests
│   └── test_integration.py    # Integration tests
│
└── docs/                      # Documentation
    ├── README.md
    ├── INSTALLATION.md
    ├── USAGE.md
    ├── ARCHITECTURE.md (this file)
    └── CONTRIBUTING.md
```

---

## Module Deep Dive

### config.py - Configuration Management

**Purpose**: Handle CLI argument parsing and runtime configuration.

#### RunConfig Class

```python
class RunConfig:
    """
    Stores runtime configuration and global state.
    
    Attributes:
        interface (Optional[str]): Wireless interface name
        channel (Optional[int]): Channel to lock to
        verbose (bool): Enable verbose logging
    """
    
    interface: Optional[str]
    channel: Optional[int]
    verbose: bool
    
    def __init__(
        self,
        interface: Optional[str] = None,
        channel: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        # Validation
        if interface is not None and not isinstance(interface, str):
            raise ValueError("interface must be a string or None")
        if channel is not None and not isinstance(channel, int):
            raise ValueError("channel must be an integer or None")
        
        self.interface = interface
        self.channel = channel
        self.verbose = verbose
```

**Key Design Decisions:**
- Type validation in constructor prevents invalid state
- All fields have sensible defaults
- Class is easily extensible for new options

#### parse_args Function

```python
def parse_args() -> RunConfig:
    """Parse CLI arguments and return RunConfig."""
    parser = argparse.ArgumentParser(
        description="wlfwifi: Automated wireless auditor"
    )
    parser.add_argument("-i", "--interface", type=str)
    parser.add_argument("-c", "--channel", type=int)
    parser.add_argument("-v", "--verbose", action="store_true")
    
    args = parser.parse_args()
    return RunConfig(
        interface=args.interface,
        channel=args.channel,
        verbose=args.verbose
    )
```

---

### models.py - Data Models

**Purpose**: Define data structures for wireless entities.

#### Target Class

Represents a wireless network access point:

```python
class Target:
    """
    Represents a wireless network target.
    
    Attributes:
        bssid (str): MAC address of access point
        essid (str): Network name (SSID)
        channel (int): WiFi channel
        encryption (str): Encryption type (WEP, WPA, WPA2)
        wps (bool): WPS enabled status
    """
    
    bssid: str
    essid: str
    channel: int
    encryption: str
    wps: bool
```

**Design Notes:**
- Simple data class with no methods
- All attributes are public for easy access
- Could be converted to dataclass in future

#### Client Class

Represents a connected client device:

```python
class Client:
    """
    Represents a client device connected to a target.
    
    Attributes:
        mac (str): Client MAC address
        target_bssid (str): BSSID of associated network
    """
    
    mac: str
    target_bssid: str
```

#### CapFile Class

Represents a capture file:

```python
class CapFile:
    """
    Represents a capture file with handshake data.
    
    Attributes:
        path (str): File path to capture
        handshakes (int): Number of handshakes captured
    """
    
    path: str
    handshakes: int
```

---

### utils.py - Utility Functions

**Purpose**: Provide helper functions used across the codebase.

#### Function Categories

**File Operations:**
```python
def rename(old: str, new: str) -> None:
    """Rename file, handling cross-partition moves."""

def remove_file(filename: str) -> None:
    """Remove file if exists, ignore if not."""

def remove_airodump_files(prefix: str, config: Any) -> None:
    """Clean up airodump output files."""
```

**Program Management:**
```python
def program_exists(program: str) -> bool:
    """Check if program is installed using 'which'."""

def send_interrupt(process: Any) -> None:
    """Send SIGINT to a process."""

def print_and_exec(cmd: List[str], ...) -> None:
    """Print and execute a command."""
```

**MAC Address Handling:**
```python
def get_mac_address(iface: str) -> str:
    """Get MAC address of interface."""

def generate_random_mac(old_mac: str) -> str:
    """Generate random MAC preserving vendor prefix."""

def mac_anonymize(iface: str, ...) -> None:
    """Randomize interface MAC address."""

def mac_change_back(config: Any, ...) -> None:
    """Restore original MAC address."""
```

**Formatting:**
```python
def sec_to_hms(sec: int) -> str:
    """Convert seconds to [h:mm:ss] format."""

def add_commas(n: int) -> str:
    """Format number with thousands separators."""
```

---

### attacks.py - Attack Logic

**Purpose**: Implement attack algorithms and WPS detection.

#### Attack Abstract Base Class

```python
class Attack(metaclass=abc.ABCMeta):
    """
    Abstract base class for all attack types.
    
    Subclasses must implement:
        RunAttack(): Start the attack
        EndAttack(): Stop and cleanup
    """
    
    @abc.abstractmethod
    def RunAttack(self) -> Any:
        raise NotImplementedError
    
    @abc.abstractmethod
    def EndAttack(self) -> Any:
        raise NotImplementedError
```

**Usage Pattern:**
```python
class WPAAttack(Attack):
    def __init__(self, target: Target, config: RunConfig):
        self.target = target
        self.config = config
        self.running = False
    
    def RunAttack(self) -> str:
        self.running = True
        # ... implementation
        return "Handshake captured"
    
    def EndAttack(self) -> str:
        self.running = False
        # ... cleanup
        return "Attack stopped"
```

#### wps_check_targets Function

```python
def wps_check_targets(
    targets: List[Target],
    cap_file: str,
    verbose: bool = True
) -> None:
    """
    Check targets for WPS support using tshark.
    
    Modifies targets in-place, setting wps=True for
    networks that advertise WPS in beacon frames.
    
    Args:
        targets: List of Target objects to check
        cap_file: Path to capture file with beacon frames
        verbose: Enable verbose output
    """
```

**Implementation Notes:**
- Uses tshark to parse capture files
- Matches BSSIDs in WPS frames
- Updates Target.wps in-place

---

### core.py - Core Engine

**Purpose**: Orchestrate the entire attack workflow.

#### main Function

```python
def main() -> None:
    """
    Main entry point for wlfwifi.
    
    Workflow:
        1. Configure logging
        2. Parse command-line arguments
        3. Initialize attack engine
        4. Handle errors and cleanup
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    try:
        config: RunConfig = parse_args()
        logging.info(f"Starting with interface={config.interface}")
        # TODO: Initialize AttackEngine
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        exit(1)
```

**Future AttackEngine Class:**
```python
class AttackEngine:
    """
    Coordinates scanning, selection, and attack execution.
    
    Attributes:
        config: Runtime configuration
        targets: Discovered networks
        clients: Connected clients
    
    Methods:
        scan(): Discover nearby networks
        select_target(): User target selection
        attack(): Execute selected attack
        cleanup(): Restore interface state
    """
```

---

## Data Flow

### Startup Flow

```
User runs: sudo wlfwifi -i wlan0 -v
                │
                ▼
        wlfwifi.py / __main__.py
                │
                ▼
        core.main() called
                │
                ▼
        logging.basicConfig()
                │
                ▼
        config.parse_args()
                │
                ▼
        RunConfig created
            - interface="wlan0"
            - channel=None
            - verbose=True
                │
                ▼
        AttackEngine initialized
```

### Scanning Flow

```
AttackEngine.scan()
        │
        ▼
utils.program_exists("airodump-ng")
        │
        ▼
subprocess: airodump-ng --output-format csv
        │
        ▼
Parse CSV output
        │
        ▼
Create Target objects
        │
        ▼
wps_check_targets(targets, cap_file)
        │
        ▼
Update Target.wps fields
        │
        ▼
Display targets to user
```

### Attack Flow

```
User selects target
        │
        ▼
Attack subclass instantiated
    WPAAttack(target, config)
        │
        ▼
attack.RunAttack()
        │
        ├──▶ subprocess: aireplay-ng (deauth)
        │
        ├──▶ subprocess: airodump-ng (capture)
        │
        └──▶ Monitor for handshake
                │
                ▼
        Handshake captured
                │
                ▼
        CapFile created
                │
                ▼
attack.EndAttack()
        │
        ▼
Return results
```

---

## Class Diagrams

### Core Classes

```
┌─────────────────────────────────────────────────────┐
│                     RunConfig                        │
├─────────────────────────────────────────────────────┤
│ + interface: Optional[str]                          │
│ + channel: Optional[int]                            │
│ + verbose: bool                                     │
├─────────────────────────────────────────────────────┤
│ + __init__(interface, channel, verbose)             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                      Target                          │
├─────────────────────────────────────────────────────┤
│ + bssid: str                                        │
│ + essid: str                                        │
│ + channel: int                                      │
│ + encryption: str                                   │
│ + wps: bool                                         │
├─────────────────────────────────────────────────────┤
│ + __init__(bssid, essid, channel, encryption, wps)  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                      Client                          │
├─────────────────────────────────────────────────────┤
│ + mac: str                                          │
│ + target_bssid: str                                 │
├─────────────────────────────────────────────────────┤
│ + __init__(mac, target_bssid)                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                      CapFile                         │
├─────────────────────────────────────────────────────┤
│ + path: str                                         │
│ + handshakes: int                                   │
├─────────────────────────────────────────────────────┤
│ + __init__(path, handshakes)                        │
└─────────────────────────────────────────────────────┘
```

### Attack Hierarchy

```
┌─────────────────────────────────────────────────────┐
│                  Attack (ABC)                        │
├─────────────────────────────────────────────────────┤
│ <<abstract>>                                        │
├─────────────────────────────────────────────────────┤
│ + RunAttack(): Any                                  │
│ + EndAttack(): Any                                  │
└─────────────────────────────────────────────────────┘
                        △
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────┴──────┐ ┌──────┴───────┐ ┌─────┴──────┐
│  WPAAttack   │ │   WEPAttack  │ │  WPSAttack │
├──────────────┤ ├──────────────┤ ├────────────┤
│ + target     │ │ + target     │ │ + target   │
│ + config     │ │ + config     │ │ + config   │
│ + running    │ │ + ivs        │ │ + pin      │
├──────────────┤ ├──────────────┤ ├────────────┤
│ + RunAttack()│ │ + RunAttack()│ │ +RunAttack()│
│ + EndAttack()│ │ + EndAttack()│ │ +EndAttack()│
└──────────────┘ └──────────────┘ └────────────┘
```

---

## Extending wlfwifi

### Adding a New Attack

1. **Create attack class in attacks.py:**

```python
class PMKIDAttack(Attack):
    """Attack using PMKID capture (no client needed)."""
    
    def __init__(self, target: Target, config: RunConfig):
        self.target = target
        self.config = config
        self.pmkid = None
    
    def RunAttack(self) -> Optional[str]:
        """Attempt to capture PMKID."""
        if not program_exists("hcxdumptool"):
            logging.error("hcxdumptool not found")
            return None
        
        # Implementation...
        return self.pmkid
    
    def EndAttack(self) -> None:
        """Clean up attack resources."""
        # Cleanup...
        pass
```

2. **Add tests in test_attacks.py:**

```python
class TestPMKIDAttack:
    def test_pmkid_attack_initialization(self):
        target = Target("00:11:22:33:44:55", "Test", 6, "WPA2", False)
        config = RunConfig()
        attack = PMKIDAttack(target, config)
        assert attack.target == target
    
    @patch("wlfwifi.attacks.program_exists")
    def test_pmkid_attack_no_tool(self, mock_exists):
        mock_exists.return_value = False
        # ...test implementation
```

3. **Integrate in core.py:**

```python
def select_attack(target: Target, config: RunConfig) -> Attack:
    """Select appropriate attack based on target."""
    if target.encryption == "WPA2":
        return PMKIDAttack(target, config)
    # ...
```

### Adding CLI Options

1. **Add to parse_args in config.py:**

```python
def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(...)
    
    # Add new option
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=120,
        help="Attack timeout in seconds"
    )
    
    args = parser.parse_args()
    return RunConfig(
        interface=args.interface,
        channel=args.channel,
        verbose=args.verbose,
        timeout=args.timeout,  # New field
    )
```

2. **Update RunConfig class:**

```python
class RunConfig:
    interface: Optional[str]
    channel: Optional[int]
    verbose: bool
    timeout: int  # New field
    
    def __init__(
        self,
        interface: Optional[str] = None,
        channel: Optional[int] = None,
        verbose: bool = False,
        timeout: int = 120,  # New parameter
    ) -> None:
        # ...validation
        self.timeout = timeout
```

3. **Add tests:**

```python
def test_runconfig_with_timeout(self):
    config = RunConfig(timeout=60)
    assert config.timeout == 60

def test_parse_args_timeout(self, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "-t", "60"])
    config = parse_args()
    assert config.timeout == 60
```

### Adding Utility Functions

1. **Add function in utils.py:**

```python
def validate_bssid(bssid: str) -> bool:
    """
    Validate BSSID format (MAC address).
    
    Args:
        bssid: String to validate
    
    Returns:
        True if valid MAC format, False otherwise
    
    Example:
        >>> validate_bssid("00:11:22:33:44:55")
        True
        >>> validate_bssid("invalid")
        False
    """
    import re
    pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    return bool(re.match(pattern, bssid))
```

2. **Add tests in test_utils.py:**

```python
class TestValidateBssid:
    def test_valid_bssid_uppercase(self):
        assert utils.validate_bssid("00:11:22:33:44:55") is True
    
    def test_valid_bssid_lowercase(self):
        assert utils.validate_bssid("aa:bb:cc:dd:ee:ff") is True
    
    def test_invalid_bssid_format(self):
        assert utils.validate_bssid("invalid") is False
    
    def test_invalid_bssid_short(self):
        assert utils.validate_bssid("00:11:22") is False
```

---

## Testing Architecture

### Test Structure

```
tests/
├── test_models.py        # 22 tests - Data model tests
├── test_config.py        # 32 tests - Configuration tests
├── test_utils.py         # 55 tests - Utility function tests
├── test_attacks.py       # 21 tests - Attack logic tests
├── test_core.py          # 21 tests - Core engine tests
└── test_integration.py   # 19 tests - End-to-end tests
```

### Testing Patterns

**Unit Tests:**
```python
def test_sec_to_hms_one_hour():
    assert utils.sec_to_hms(3600) == "[1:00:00]"
```

**Mocking External Dependencies:**
```python
@patch("wlfwifi.utils.Popen")
def test_program_exists_found(self, mock_popen):
    mock_proc = Mock()
    mock_proc.communicate.return_value = (b"/usr/bin/python", b"")
    mock_popen.return_value = mock_proc
    
    result = utils.program_exists("python")
    
    assert result is True
```

**Integration Tests:**
```python
def test_full_workflow(self):
    config = RunConfig(interface="wlan0")
    target = Target("00:11:22:33:44:55", "Test", 6, "WPA2", True)
    attack = WPAAttack(target, config)
    
    result = attack.RunAttack()
    attack.EndAttack()
    
    assert result is not None
```

---

## External Tool Integration

### Tool Wrapper Pattern

```python
def run_airodump(interface: str, output_prefix: str, channel: Optional[int] = None) -> Popen:
    """
    Start airodump-ng process.
    
    Args:
        interface: Monitor mode interface
        output_prefix: Output file prefix
        channel: Optional channel to lock
    
    Returns:
        Popen object for the running process
    """
    cmd = [
        "airodump-ng",
        "--output-format", "csv",
        "-w", output_prefix,
    ]
    
    if channel:
        cmd.extend(["-c", str(channel)])
    
    cmd.append(interface)
    
    return Popen(cmd, stdout=PIPE, stderr=PIPE)
```

### Tool Availability Checks

```python
def ensure_tools_available(required: List[str]) -> bool:
    """Check all required tools are installed."""
    missing = []
    for tool in required:
        if not program_exists(tool):
            missing.append(tool)
    
    if missing:
        logging.error(f"Missing tools: {', '.join(missing)}")
        return False
    return True
```

---

## Error Handling Strategy

### Levels of Error Handling

1. **Function Level**: Handle expected errors, log warnings
2. **Module Level**: Catch and re-raise with context
3. **Main Level**: Catch all, log critical, exit gracefully

```python
# Function level
def remove_file(filename: str) -> None:
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass  # Expected, ignore
    except PermissionError as e:
        logging.warning(f"Cannot remove {filename}: {e}")

# Module level
def capture_handshake(target: Target) -> CapFile:
    try:
        # ... implementation
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Handshake timeout for {target.essid}")

# Main level
def main() -> None:
    try:
        # ... workflow
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        exit(1)
```

---

## Logging System

### Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

### Log Levels Usage

| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed debugging info |
| `INFO` | Normal operation messages |
| `WARNING` | Unexpected but handled situations |
| `ERROR` | Errors that prevent operation |
| `CRITICAL` | Fatal errors, program must exit |

### Examples

```python
logging.debug(f"Executing command: {' '.join(cmd)}")
logging.info(f"Found {len(targets)} networks")
logging.warning(f"WPS locked on {target.essid}")
logging.error(f"Failed to capture handshake: {e}")
logging.critical(f"Cannot access interface: {e}")
```

---

## Future Considerations

### Planned Improvements

1. **Async/Await Support**: For concurrent operations
2. **Plugin System**: Dynamic attack loading
3. **Web Interface**: Optional GUI
4. **Database Storage**: Persist results
5. **API Mode**: Programmatic access

### Potential Refactors

1. **Use dataclasses**: For model classes
2. **Use Pydantic**: For validation
3. **Add Protocol types**: For duck typing
4. **Implement Observer pattern**: For progress updates

---

## See Also

- [README.md](README.md) - Project overview
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [USAGE.md](USAGE.md) - Usage examples
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide
