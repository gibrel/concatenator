from concatenator.services.readers import is_binary_file, read_file_content


def test_is_binary_file_detects_null_bytes(tmp_path):
    binary_path = tmp_path / "data.bin"
    binary_path.write_bytes(b"\x00\x01\x02")
    assert is_binary_file(binary_path)


def test_is_binary_file_handles_text(tmp_path):
    text_path = tmp_path / "notes.txt"
    text_path.write_text("hello world\n")
    assert not is_binary_file(text_path)


def test_read_file_content_falls_back_to_latin1(tmp_path):
    text_path = tmp_path / "latin.txt"
    text_path.write_bytes(b"caf\xe9")
    assert read_file_content(text_path, encoding="utf-8", errors="strict") == "café"


def test_read_file_content_returns_none_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.txt"
    assert read_file_content(missing_path) is None
