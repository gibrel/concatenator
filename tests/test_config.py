from concatenator.core.config import Settings


def test_ensure_paths_resolves_to_absolute(tmp_path):
    root = tmp_path / "root"
    output_file = tmp_path / "output.md"
    settings = Settings(root_directory=root, output_file=output_file)

    resolved = settings.ensure_paths()
    assert resolved.root_directory.is_absolute()
    assert resolved.output_file.is_absolute()
