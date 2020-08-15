"""Constructs for cli builder app."""
from __future__ import annotations

from configparser import ConfigParser
from typing import TYPE_CHECKING, Dict, Union

from plumbum import cli

from .builder import build_exe

if TYPE_CHECKING:
    from pathlib import Path


def parse_config(path: Union[Path, str], *, section: str = 'VERSIONINFO') -> Dict[str, str]:
    """Parse config file containing executable metadata.

    The file must have the following format:
    [VERSIONINFO]
    <key>=<value>

    Available keys can be found here: https://bit.ly/3aoo2i7.
    """
    parser = ConfigParser()
    parser.read(path)
    return parser[section]


class Pyndler(cli.Application):
    """CLI builder application."""
    target = cli.SwitchAttr(['t', 'target'],
                            argtype=cli.ExistingFile,
                            help='Path to output file. If not set, the source path is taken')
    icon = cli.SwitchAttr(['i', 'icon'], argtype=cli.ExistingFile, help='Path to exe icon')
    config = cli.SwitchAttr(['c', 'config'],
                            argtype=cli.ExistingFile,
                            help='Path to config file for setting additional metadata')
    gui = cli.Flag(['--gui'], help='Set to true, if source is a GUI application')
    refresh = cli.Flag(['--refresh'], help='Refresh Windows icon cache after building')

    @cli.positional(cli.ExistingFile)
    def main(self: 'Pyndler', source: str) -> None:
        """Main entrypoint for cli app."""
        if self.config:
            metadata = parse_config(self.config)
        else:
            metadata = None

        build_exe(source=source,
                  target=self.target,
                  icon=self.icon,
                  metadata=metadata,
                  gui=self.gui,
                  refresh=self.refresh)
