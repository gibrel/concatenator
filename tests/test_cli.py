from pathlib import Path

from concatenator import cli


def test_build_parser_defaults():
    parser = cli.build_parser()
    args = parser.parse_args([str(Path.cwd())])

    assert args.output_file == Path.cwd() / "output.md"
    assert args.footer_text == "````\n\n// End of {path}\n"
    assert args.header_text == "### {path}\n\n````{extension_name}"
