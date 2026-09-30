import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

def setup_logger(log_dir: str = "logs") -> logging.Logger:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("USBSafe")
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # Main log
    main_handler = RotatingFileHandler(Path(log_dir) / "usb-safe.log", maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    main_handler.setFormatter(formatter)
    logger.addHandler(main_handler)
    
    # Error log
    error_handler = RotatingFileHandler(Path(log_dir) / "errors.log", maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # Console for test mode and feedback
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

logger = logging.getLogger("USBSafe")
