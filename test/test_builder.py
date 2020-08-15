from tempfile import TemporaryDirectory
from pathlib import Path
from zipapp import create_archive

from plumbum import local
from pyndler import builder


def test_os_arch():
    assert builder.get_os_architecture() in (32, 64)


def test_launchers_exists():
    assert builder.get_launcher_path(arch=32).exists()
    assert builder.get_launcher_path(arch=64).exists()
    assert builder.get_launcher_path(gui=True, arch=32).exists()
    assert builder.get_launcher_path(gui=True, arch=64).exists()


def test_rcedit_exists():
    assert builder.get_rcedit_path(arch=32).exists()
    assert builder.get_rcedit_path(arch=64).exists()


def test_merge_files(tmp_path):
    paths = list()

    for i in range(3):
        path = (tmp_path / f'file{i}')
        path.write_text(str(i))
        paths.append(path)

    builder.merge_files(*paths)
    assert paths[0].read_text() == '012'


def test_build_exe(tmp_path, pyz_archive):
    builder.build_exe(pyz_archive)

    target = tmp_path / 'foo.exe'
    output = local[str(target)]()
    assert output.strip() == 'bar'
