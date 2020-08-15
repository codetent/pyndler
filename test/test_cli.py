from pytest import raises

from plumbum import local, cli
from plumbum.cli.application import ShowHelp
from pyndler.cli import Pyndler


def test_cli_help():
    with raises(ShowHelp):
        Pyndler.invoke(help=True)


def test_cli_build(tmp_path, pyz_archive):
    Pyndler.invoke(pyz_archive)

    target = tmp_path / 'foo.exe'
    output = local[str(target)]()
    assert output.strip() == 'bar'
