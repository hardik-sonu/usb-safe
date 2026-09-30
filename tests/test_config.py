import json
from pathlib import Path
from src.config_manager import load_config

def test_load_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_data = {
        "archive_root": str(tmp_path / "archive"),
        "verify_sha256": False
    }
    with open(config_file, "w") as f:
        json.dump(config_data, f)
        
    config = load_config(str(config_file))
    assert config.archive_root == str(tmp_path / "archive")
    assert config.verify_sha256 is False
