import hashlib
from pathlib import Path
from src.logger import logger

def calculate_sha256(file_path: Path, buffer_size: int = 4 * 1024 * 1024) -> str:
    """Calculate SHA-256 hash of a file efficiently using streaming."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(buffer_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.error(f"Failed to hash {file_path}: {e}")
        return ""
