from concatenator.core.config import Settings


def test_ensure_paths_resolves_to_absolute(tmp_path):
    root = tmp_path / "root"
    output_file = tmp_path / "output.md"
    settings = Settings(root_directory=root, output_file=output_file)

    resolved = settings.ensure_paths()
    assert resolved.root_directory.is_absolute()
    assert resolved.output_file.is_absolute()


def test_ensure_paths_normalizes_filters(tmp_path):
    settings = Settings(
        root_directory=tmp_path,
        ignore_directories=["build", "dist/"],
        ignore_extensions=["Py", ".TXT"],
        include_extensions={" md "},
    )

    resolved = settings.ensure_paths()
    assert "build" in resolved.ignore_directories
    assert "dist" in resolved.ignore_directories
    assert ".py" in resolved.ignore_extensions
    assert ".txt" in resolved.ignore_extensions
    assert resolved.include_extensions == {".md"}
