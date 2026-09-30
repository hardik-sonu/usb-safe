from dataclasses import dataclass

@dataclass
class Config:
    archive_root: str
    verify_sha256: bool = True
    copy_buffer_mb: int = 4
    log_directory: str = "logs"

@dataclass
class UsbDevice:
    drive_letter: str
    volume_label: str
    volume_serial: str
    file_system: str
