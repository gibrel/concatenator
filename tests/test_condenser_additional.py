import pytest

from concatenator.core.config import Settings
from concatenator.core.exceptions import InvalidRootError
from concatenator.services import condenser


def test_build_display_path_supports_absolute_paths(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    target = root / "dir" / "file.txt"
    target.parent.mkdir(parents=True)
    target.write_text("hi")

    assert (
        condenser.build_display_path(target, root, use_relative_paths=True) == "/root/dir/file.txt"
    )
    assert condenser.build_display_path(target, root, use_relative_paths=False) == str(target)


def test_condense_directory_rejects_invalid_root(tmp_path):
    output_file = tmp_path / "output.md"
    settings = Settings(root_directory=tmp_path / "missing", output_file=output_file)

    with pytest.raises(InvalidRootError):
        condenser.condense_directory(settings)


def test_condense_directory_skips_binary_when_requested(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    binary_file = root / "data.bin"
    binary_file.write_bytes(b"\x00\x01\x02")
    output_file = tmp_path / "output.md"

    settings = Settings(
        root_directory=root,
        output_file=output_file,
        include_extensions={".bin"},
        skip_binary=True,
    )

    assert condenser.condense_directory(settings) == 0
