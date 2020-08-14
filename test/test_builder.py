from tempfile import TemporaryDirectory
from pathlib import Path
from zipapp import create_archive

from plumbum import local
from pybox import builder


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


def test_merge_files():
    with TemporaryDirectory() as tmp:
        paths = list()

        for i in range(3):
            path = (Path(tmp) / f'file{i}')
            path.write_text(str(i))
            paths.append(path)

        builder.merge_files(*paths)
        assert paths[0].read_text() == '012'


def test_build_exe():
    tmp = TemporaryDirectory().name
    Path(tmp).mkdir()

    source = Path(tmp) / 'foo.py'
    source.write_text('def main():\n\tprint(\'bar\')')

    pyz = Path(tmp) / 'foo.pyz'
    create_archive(source, target=pyz, main='foo:main')

    builder.build_exe(pyz)

    target = Path(tmp) / 'foo.exe'
    output = local[str(target)]()
    assert output == 'bar'
