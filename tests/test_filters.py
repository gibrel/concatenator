from concatenator.services.filters import (
    normalize_extensions,
    normalize_ignore_directories,
    should_ignore_dir,
    should_include_file,
)


def test_normalize_extensions_handles_dots_and_case():
    normalized = normalize_extensions(["py", ".TXT", " md "])
    assert normalized == {".py", ".txt", ".md"}


def test_normalize_ignore_directories_includes_path_variants():
    normalized = normalize_ignore_directories(["build", "dist/"])
    assert "build" in normalized
    assert "dist/" in normalized
    assert "dist" in normalized


def test_should_ignore_dir_matches_relative_paths(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    (root / "logs").mkdir()
    (root / "src").mkdir()

    dirnames = ["logs", "src"]
    to_remove = should_ignore_dir(root, dirnames, {"logs"}, root)
    assert to_remove == ["logs"]


def test_should_include_file_treats_extensionless_as_txt(tmp_path):
    no_ext = tmp_path / "Makefile"
    no_ext.write_text("all:\n\techo ok\n")

    include_extensions = {".txt"}
    ignore_extensions = set()
    assert should_include_file(no_ext, include_extensions, ignore_extensions)

    ignore_extensions = {".txt"}
    assert not should_include_file(no_ext, include_extensions, ignore_extensions)
