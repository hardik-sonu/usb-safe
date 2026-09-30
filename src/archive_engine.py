import os
from pathlib import Path
from datetime import datetime
from src.models import Config, UsbDevice
from src.file_hasher import calculate_sha256
from src.logger import logger

class ArchiveEngine:
    def __init__(self, config: Config):
        self.config = config
        self.buffer_size = config.copy_buffer_mb * 1024 * 1024

    def archive_device(self, device: UsbDevice):
        source_root = Path(device.drive_letter + "\\")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        
        # Use Volume Label and Serial to uniquely identify the USB archive folder
        folder_name = f"{device.volume_label}_{device.volume_serial}".strip("_")
        if not folder_name:
            folder_name = "Unknown_USB"
            
        dest_root = Path(self.config.archive_root) / folder_name / timestamp
        
        logger.info(f"Archive session started for {device.volume_label} ({device.volume_serial}) to {dest_root}")
        
        try:
            dest_root.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create archive directory {dest_root}: {e}")
            return
        
        processed_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(source_root):
            rel_path = Path(root).relative_to(source_root)
            dest_dir = dest_root / rel_path
            
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"FAILED: directory {dest_dir} - {e}")
                continue
                
            for file in files:
                source_file = Path(root) / file
                dest_file = dest_dir / file
                
                if not source_root.exists():
                    logger.error(f"Session interrupted: device {device.drive_letter} disconnected.")
                    return
                
                success = self._copy_and_verify(source_file, dest_file)
                if success:
                    processed_count += 1
                else:
                    error_count += 1
                    
        logger.info(f"Archive verification completed. {processed_count} files processed, {error_count} errors.")

    def _copy_and_verify(self, source_file: Path, dest_file: Path) -> bool:
        try:
            final_dest = self._get_safe_dest(dest_file, source_file)
            if final_dest is None:
                return True
                
            with open(source_file, "rb") as fsrc, open(final_dest, "wb") as fdst:
                while True:
                    buf = fsrc.read(self.buffer_size)
                    if not buf:
                        break
                    fdst.write(buf)
            
            if self.config.verify_sha256:
                src_hash = calculate_sha256(source_file, self.buffer_size)
                dst_hash = calculate_sha256(final_dest, self.buffer_size)
                if src_hash != dst_hash:
                    logger.error(f"FAILED: {source_file} - Hash mismatch")
                    final_dest.unlink(missing_ok=True)
                    return False
            
            return True
        except Exception as e:
            logger.error(f"FAILED: {source_file} - Reason: {e}")
            return False

    def _get_safe_dest(self, dest_file: Path, source_file: Path) -> Path | None:
        if not dest_file.exists():
            return dest_file
            
        if self.config.verify_sha256:
            src_hash = calculate_sha256(source_file, self.buffer_size)
            dst_hash = calculate_sha256(dest_file, self.buffer_size)
            if src_hash == dst_hash:
                return None
                
        version = 2
        while True:
            new_name = f"{dest_file.stem}__version_{version}{dest_file.suffix}"
            new_dest = dest_file.with_name(new_name)
            if not new_dest.exists():
                return new_dest
            version += 1
