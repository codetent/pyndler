from pytest import raises

from plumbum import local, cli
from plumbum.cli.application import ShowHelp
from pybox.cli import PyBox


def test_cli_help():
    with raises(ShowHelp):
        PyBox.invoke(help=True)


def test_cli_build(tmp_path, pyz_archive):
    PyBox.invoke(pyz_archive)

    target = tmp_path / 'foo.exe'
    output = local[str(target)]()
    assert output.strip() == 'bar'
