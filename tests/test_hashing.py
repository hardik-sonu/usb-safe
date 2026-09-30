from src.file_hasher import calculate_sha256

def test_calculate_sha256(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world")
    
    hash_val = calculate_sha256(file)
    # Expected hash for "hello world"
    assert hash_val == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
