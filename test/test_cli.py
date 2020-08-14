from pytest import raises

from plumbum.cli.application import ShowHelp
from pybox.cli import PyBox


def test_cli_help():
    with raises(ShowHelp):
        PyBox.invoke(help=True)


def test_cli_build():
    pass
