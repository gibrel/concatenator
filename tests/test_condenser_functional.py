from concatenator.core.config import Settings
from concatenator.services.condenser import condense_directory


def test_condense_directory_formats_paths_and_includes_extensionless(tmp_path):
    root = tmp_path / "pasta-alvo"
    project_dir = root / "src" / "project"
    project_dir.mkdir(parents=True)

    main_file = project_dir / "main.py"
    main_file.write_text("print('hi')\n")

    makefile = root / "Makefile"
    makefile.write_text("all:\n\techo ok\n")

    output_file = tmp_path / "output.md"
    settings = Settings(
        root_directory=root,
        output_file=output_file,
        include_extensions={".py", ".txt"},
    )

    count = condense_directory(settings)
    assert count == 2

    output = output_file.read_text()
    assert "## /pasta-alvo/src/project" in output
    assert "### /pasta-alvo/src/project/main.py" in output
    assert "### /pasta-alvo/Makefile" in output
    assert "````Makefile" in output
    assert not output.endswith("\n\n")
