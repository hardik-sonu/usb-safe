import sys
import os
import time
import argparse
import ctypes
from pathlib import Path

# Ensure the root project directory is in the path when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import load_config
from src.logger import setup_logger, logger
from src.usb_monitor import UsbMonitor
from src.archive_engine import ArchiveEngine
from src.usb_identity import get_drive_details, UsbDevice

def process_device(device: UsbDevice, engine: ArchiveEngine):
    logger.info(f"USB Detected: {device.volume_label} ({device.drive_letter})")
    
    # 0x04 = MB_YESNO (Yes/No buttons)
    # 0x20 = MB_ICONQUESTION (Question mark icon)
    # 0x1000 = MB_SYSTEMMODAL (Brings dialog to front)
    # 0x40000 = MB_TOPMOST
    style = 0x04 | 0x20 | 0x40000 
    
    title = "USB Storage Detected"
    text = (f"A USB storage device has been connected:\n\n"
            f"Drive: {device.drive_letter}\n"
            f"Name: {device.volume_label}\n"
            f"Serial: {device.volume_serial}\n\n"
            f"Allow this application to copy its data to the local computer?")
            
    # Show the native Windows prompt (blocks until user clicks Yes or No)
    result = ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
    if result == 6:  # IDYES
        logger.info(f"User ALLOWED backup for {device.volume_label}")
        engine.archive_device(device)
    else:
        logger.info(f"User DENIED backup for {device.volume_label}. Ignoring.")

def main():
    parser = argparse.ArgumentParser(description="USB Safe - Local USB Archival Tool")
    parser.add_argument("--test-drive", type=str, help="Simulate a USB source from a folder")
    args = parser.parse_args()

    try:
        config = load_config()
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    setup_logger(config.log_directory)
    logger.info("USB Safe starting...")

    engine = ArchiveEngine(config)

    if args.test_drive:
        test_path = Path(args.test_drive)
        if not test_path.exists():
            logger.error(f"Test drive path not found: {test_path}")
            sys.exit(1)
            
        logger.info(f"Running in test mode for path: {test_path}")
        test_device = UsbDevice(
            drive_letter=str(test_path).rstrip("\\"),
            volume_label="TEST-DRIVE",
            volume_serial="TEST-1234",
            file_system="NTFS"
        )
        process_device(test_device, engine)
        sys.exit(0)

    def on_usb_connected(device: UsbDevice):
        process_device(device, engine)

    monitor = UsbMonitor(on_usb_connected)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        monitor.stop()

if __name__ == "__main__":
    main()
