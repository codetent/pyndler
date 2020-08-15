"""Functions for building executables from pyz files."""
from __future__ import annotations

import struct
from pathlib import Path
from pkg_resources import resource_filename
from shutil import copy
from typing import Dict, Iterable, Union

from plumbum import local


def refresh_icon_cache() -> None:
    """Refresh windows icon cache.

    This is required to show icon changes in the Windows Explorer.
    """
    local['ie4uinit']['-show']()


def get_os_architecture() -> int:
    """Get current os architecture (32 or 64 bit)."""
    return struct.calcsize('P') * 8


def get_launcher_path(*, gui: bool = False, arch: int = None) -> Path:
    """Get path of distlib launcher executable.

    Args:
        gui (bool, optional): Set to true if GUI launcher is required. Defaults to False.
        arch (int, optional): Set os architecture explicitly. If None, it is determined using get_os_architecture().
                              Defaults to None.
    """
    prefix = 'w' if gui else 't'
    arch = arch if arch else get_os_architecture()
    return Path(resource_filename('pip._vendor.distlib', f'{prefix}{arch}.exe'))


def get_rcedit_path(*, arch: int = None) -> Path:
    """Get patch to included rcedit executable.

    Args:
        arch (int, optional): Set os architecture explicitly. If None, it is determined using get_os_architecture().
                              Defaults to None.
    """
    arch = arch if arch else get_os_architecture()
    return Path(resource_filename('pyndler.rcedit', f'rcedit-x{arch}.exe'))


def call_rcedit(source: Union[Path, str], *, icon: Union[Path, str] = None, metadata: Dict[str, str] = None) -> None:
    """Call rcedit executable for changing the icon or setting metadata of an executable.

    Args:
        source (Union[Path, str]): Path to existing executable which should be modified.
        icon (Union[Path, str], optional): Icon to be set. If None, it will not be changed. Defaults to None.
        metadata (Dict[str, str], optional): Executable metadata. Available keys can be found here:
                                             https://bit.ly/3aoo2i7. Defaults to None.
    """
    rcedit_path = get_rcedit_path()
    cmd = local[str(rcedit_path)][str(source)]

    if icon:
        cmd = cmd['--set-icon', str(icon)]

    for key, value in (metadata or {}).items():
        cmd = cmd['--set-version-string', key, value]

    return cmd()


def merge_files(target: Union[Path, str], *parts: Iterable[Union[Path, str]]) -> None:
    """Merge multiple files by appending their bytes to the first file given.

    Args:
        target (Union[Path, str]): First file to which bytes should be copied.
    """
    with open(target, 'ab') as resulting:
        for part in parts:
            resulting.write(Path(part).read_bytes())


def build_exe(source: Union[Path, str],
              target: Union[Path, str] = None,
              *,
              gui: bool = False,
              icon: Union[Path, str] = None,
              metadata: Dict[str, str] = None,
              refresh: bool = False) -> None:
    """Build executable from pyz file and set icon or additional metadata.

    Args:
        source (Union[Path, str]): Path to source pyz file.
        target (Union[Path, str], optional): Path to target exe file. If None, the name is taken from the source path.
                                             Defaults to None.
        gui (bool, optional): Set to True, if application is a GUI app. Defaults to False.
        icon (Union[Path, str], optional): Path to optional icon file. Defaults to None.
        metadata (Dict[str, str], optional): Dictionary containing additional metadata. See call_rcedit(). Defaults to
                                             None.
        refresh (bool, optional): Set to True, if Windows icon cache should be refreshed afterwards. Defaults to False.
    """
    if not target:
        source_path = Path(source)
        target = source_path.parent / f'{source_path.stem}.exe'

    launcher_path = get_launcher_path(gui=gui)
    copy(launcher_path, target)

    call_rcedit(target, icon=icon, metadata=metadata)
    merge_files(target, source)

    if icon and refresh:
        refresh_icon_cache()
