import json
from pathlib import Path
from src.models import Config

def load_config(config_path: str = "config/config.json") -> Config:
    path = Path(config_path)
    
    # Automatically resolve the current user's Downloads folder
    auto_downloads_dir = str(Path.home() / "Downloads" / "USB-Safe-Archive")
    
    if not path.exists():
        # If no config file exists at all, just use the automatic defaults!
        return Config(
            archive_root=auto_downloads_dir,
            verify_sha256=True,
            copy_buffer_mb=4,
            log_directory="logs"
        )
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return Config(
        archive_root=data.get("archive_root", auto_downloads_dir),
        verify_sha256=data.get("verify_sha256", True),
        copy_buffer_mb=data.get("copy_buffer_mb", 4),
        log_directory=data.get("log_directory", "logs")
    )
