from __future__ import annotations

from configparser import ConfigParser
from typing import TYPE_CHECKING, Dict, Union

from plumbum import cli

from .builder import build_exe

if TYPE_CHECKING:
    from pathlib import Path


def parse_config(path: Union[Path, str], *, section: str = 'VERSIONINFO') -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(path)
    return parser[section]


class PyBox(cli.Application):
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
    def main(self, source) -> None:
        if self.config:
            info = parse_config(self.config)
        else:
            info = None

        build_exe(source=source,
                  target=self.target,
                  icon=self.icon,
                  version_info=info,
                  gui=self.gui,
                  refresh=self.refresh)
