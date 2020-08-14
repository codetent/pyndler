import struct
from pkg_resources import resource_filename
from pathlib import Path
from shutil import copy
from typing import Union, Dict, Iterable

from plumbum import local


def refresh_icon_cache() -> None:
    local['ie4uinit']['-show']()


def get_os_architecture() -> int:
    return struct.calcsize('P') * 8


def get_launcher_path(gui: bool = False) -> Path:
    prefix = 'w' if gui else 't'
    return Path(resource_filename('pip._vendor.distlib', f'{prefix}{get_os_architecture()}.exe'))


def get_rcedit_path() -> Path:
    return Path(resource_filename('pybox.rcedit', f'rcedit-x{get_os_architecture()}.exe'))


def call_rcedit(source: Union[Path, str], *, icon: Union[Path, str] = None, version_info: Dict[str, str] = None) -> None:
    rcedit_path = get_rcedit_path()
    cmd = local[str(rcedit_path)][str(source)]

    if icon:
        cmd = cmd['--set-icon', str(icon)]

    for key, value in (version_info or dict()).items():
        cmd = cmd['--set-version-string', key, value]

    return cmd()


def combine_exe(source: Union[Path, str], *parts: Iterable[Union[Path, str]]) -> None:
    with open(source, 'ab') as resulting:
        for part in parts:
            resulting.write(Path(part).read_bytes())


def build_exe(source: Union[Path, str], target: Union[Path, str] = None, *, gui: bool = False, icon: Union[Path, str] = None, version_info: Dict[str, str] = None, refresh: bool = False):
    if not target:
        source_path = Path(source)
        target = source_path.parent / f'{source_path.stem}.exe'

    launcher_path = get_launcher_path(gui=gui)
    copy(launcher_path, target)

    call_rcedit(target, icon=icon, version_info=version_info)
    combine_exe(target, source)

    if icon and refresh:
        refresh_icon_cache()
