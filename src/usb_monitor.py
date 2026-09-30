import time
import threading
from typing import Callable, Set
from src.usb_identity import get_all_usb_drives, UsbDevice
from src.logger import logger
import pythoncom
import wmi

class UsbMonitor:
    def __init__(self, callback: Callable[[UsbDevice], None]):
        self.callback = callback
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("Background USB monitoring started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _monitor_loop(self):
        pythoncom.CoInitialize()
        try:
            c = wmi.WMI()
            watcher = c.Win32_VolumeChangeEvent.watch_for(EventType=2)
            while self.running:
                try:
                    event = watcher(timeout_ms=1000)
                    drive = event.DriveName
                    if drive:
                        time.sleep(1)
                        for d in get_all_usb_drives():
                            if d.drive_letter == drive:
                                self.callback(d)
                except wmi.x_wmi_timed_out:
                    continue
                except Exception as e:
                    logger.error(f"WMI event error: {e}")
                    time.sleep(2)
        finally:
            pythoncom.CoUninitialize()
