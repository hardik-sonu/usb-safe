from pathlib import Path
from src.archive_engine import ArchiveEngine
from src.models import Config

def test_duplicate_handling(tmp_path):
    archive_dir = tmp_path / "archive"
    
    config = Config(
        archive_root=str(archive_dir),
        verify_sha256=True
    )
    engine = ArchiveEngine(config)
    
    source = tmp_path / "source.txt"
    source.write_text("v1")
    
    dest = tmp_path / "dest.txt"
    dest.write_text("v1")
    
    # Same content - should skip
    safe_dest = engine._get_safe_dest(dest, source)
    assert safe_dest is None
    
    # Different content - should version
    source.write_text("v2")
    safe_dest = engine._get_safe_dest(dest, source)
    assert safe_dest is not None
    assert safe_dest.name == "dest__version_2.txt"
    
    # Create version 2
    safe_dest.write_text("v2_different_than_new")
    
    # Should version again
    safe_dest2 = engine._get_safe_dest(dest, source)
    assert safe_dest2 is not None
    assert safe_dest2.name == "dest__version_3.txt"
