import ctypes
import string
from typing import List, Optional
from src.models import UsbDevice

def get_drive_details(drive_letter: str) -> Optional[UsbDevice]:
    """Get volume details for a Windows drive."""
    drive_letter = drive_letter.upper()
    if not drive_letter.endswith(":\\"):
        drive_letter += ":\\"
        
    kernel32 = ctypes.windll.kernel32
    volume_name_buffer = ctypes.create_unicode_buffer(1024)
    file_system_name_buffer = ctypes.create_unicode_buffer(1024)
    serial_number = ctypes.c_ulong(0)
    max_component_length = ctypes.c_ulong(0)
    file_system_flags = ctypes.c_ulong(0)

    result = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive_letter),
        volume_name_buffer,
        ctypes.sizeof(volume_name_buffer),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(file_system_flags),
        file_system_name_buffer,
        ctypes.sizeof(file_system_name_buffer)
    )

    if result:
        # Convert serial to hex format like 1234-ABCD
        serial_hex = f"{serial_number.value:08X}"
        formatted_serial = f"{serial_hex[:4]}-{serial_hex[4:]}"
        return UsbDevice(
            drive_letter=drive_letter[:2],
            volume_label=volume_name_buffer.value,
            volume_serial=formatted_serial,
            file_system=file_system_name_buffer.value
        )
    return None

def get_all_usb_drives() -> List[UsbDevice]:
    """Scan and return all removable drives."""
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive_path = f"{letter}:\\"
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
            if drive_type == 2:  # DRIVE_REMOVABLE
                details = get_drive_details(drive_path)
                if details:
                    drives.append(details)
        bitmask >>= 1
    return drives
