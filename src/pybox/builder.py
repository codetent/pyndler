import json
import os
import struct
from argparse import ArgumentParser
from subprocess import check_call
from pkg_resources import resource_filename
from urllib.request import urlopen, urlretrieve
from pathlib import Path
from itertools import chain
from shutil import copy


def refresh_icon_cache():
    check_call(['ie4uinit', '-show'])


def get_os_architecture():
    return struct.calcsize('P') * 8


def get_launcher_path(gui=False):
    prefix = 'w' if gui else 't'
    return Path(resource_filename('pip._vendor.distlib', f'{prefix}{get_os_architecture()}.exe'))


def get_rcedit_path():
    return Path()


def call_rcedit(source, *, rcedit_path=None, **kwargs):
    param_list = []
        
    for key, value in kwargs.items():
        param_list.append('--set-' + key.replace('_', '-'))
        param_list.append(value)

    if not rcedit_path:
        rcedit_path = get_rcedit_path()

    check_call([str(rcedit_path), str(source), *param_list])


def combine_exe(source, *parts):
    with open(source, 'ab') as resulting:
        for part in parts:
            resulting.write(Path(part).read_bytes())


def build_exe(source, target=None, *, gui=False, launcher_path=None, refresh=False, **rcargs):
    if not target:
        source_path = Path(source)
        target = source_path.parent / f'{source_path.stem}.exe'

    if not launcher_path:
        launcher_path = get_launcher_path(gui=gui)

    copy(launcher_path, target)

    if rcargs:
        call_rcedit(**rcargs)

    combine_exe(target, source)

    if refresh:
        refresh_icon_cache()
