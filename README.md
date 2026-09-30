# USB Safe

An authorized laboratory archival tool for Windows. USB Safe runs silently in the background, monitors for specific authorized USB devices by their volume serial numbers, and automatically archives their contents to a specified local directory.

## Features
- **Authorized-Use Only:** Only explicitly registered USB devices are processed. Unregistered devices are ignored.
- **Silent Background Operation:** No GUIs, progress bars, or popups. Operates reliably without interrupting the user.
- **Data Integrity:** Streaming file copy with SHA-256 verification.
- **Safe Versioning:** Does not overwrite existing files. Uses deterministic versioning for duplicate file names with different contents.
- **Resilience:** Gracefully handles unexpected USB removal and file permission errors.
- **No Cloud/Telemetry:** 100% local operation. No external APIs or uploads.

## Requirements
- Windows OS
- Python 3.8+ (to build from source)

## Installation & Building
1. Clone the repository:
   ```cmd
   git clone https://github.com/your-org/usb-safe.git
   cd usb-safe
   ```
2. Build the executable using PowerShell:
   ```powershell
   .\build.ps1
   ```
3. The resulting `USB Safe.exe` will be located in the `dist/` directory. You can move this to your Desktop or startup folder.

## Configuration
Before running, you must configure the application. Create a `config.json` file inside the `config/` directory (you can copy `config.example.json`):
```json
{
    "archive_root": "D:\\USB-Safe-Archive",
    "authorized_devices": [
        {
            "name": "LAB-USB-01",
            "volume_serial": "1234-ABCD"
        }
    ],
    "verify_sha256": true,
    "copy_buffer_mb": 4,
    "log_directory": "logs"
}
```

## USB Registration
To register a new USB device, run the registration tool while the USB is connected:
```cmd
python tools/register_usb.py
```
This will display the Volume Serial for connected drives. Add this serial to your `config.json` to authorize the device.

## Test Mode
You can simulate a USB insertion using a local folder for testing purposes without needing physical hardware:
```cmd
python src/main.py --test-drive "C:\Path\To\Mock\USB"
```

## Security Limitations
- This tool does not implement encryption. The archive is stored in plaintext at the destination folder.
- USB Serial Numbers can potentially be spoofed by advanced adversaries. This tool is designed for laboratory compliance and convenience, not defense against sophisticated malicious actors.

## Troubleshooting
Check the rotating logs in the `logs/` directory for errors. `errors.log` contains a filtered view of just the failures.

## License
MIT License
