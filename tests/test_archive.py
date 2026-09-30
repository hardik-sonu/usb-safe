import os
from pathlib import Path
from src.archive_engine import ArchiveEngine
from src.models import Config, UsbDevice

def test_archive_engine_copy(tmp_path):
    archive_dir = tmp_path / "archive"
    source_dir = tmp_path / "usb_mock"
    source_dir.mkdir()
    
    (source_dir / "folder A").mkdir()
    (source_dir / "folder A" / "file.txt").write_text("content")
    (source_dir / "unicode_測試.txt").write_text("unicode content")
    
    config = Config(
        archive_root=str(archive_dir),
        verify_sha256=True
    )
    
    engine = ArchiveEngine(config)
    
    device = UsbDevice(str(source_dir), "TEST-USB", "123", "NTFS")
    
    engine.archive_device(device)
    
    # Verify destination using the new folder naming convention (Label_Serial)
    dest_usb_root = archive_dir / "TEST-USB_123"
    assert dest_usb_root.exists()
    
    # Should contain timestamp dir
    timestamp_dirs = list(dest_usb_root.iterdir())
    assert len(timestamp_dirs) == 1
    session_dir = timestamp_dirs[0]
    
    assert (session_dir / "folder A" / "file.txt").exists()
    assert (session_dir / "unicode_測試.txt").exists()
    assert (session_dir / "folder A" / "file.txt").read_text() == "content"
