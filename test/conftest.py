import pytest
from zipapp import create_archive


@pytest.fixture
def pyz_archive(tmp_path):
    source = tmp_path / 'pkg' / 'foo.py'
    source.parent.mkdir()
    source.write_text('def main():\n\tprint(\'bar\')')

    pyz = tmp_path / 'foo.pyz'
    create_archive(source.parent, target=pyz, main='foo:main', interpreter='/usr/bin/env python')
    return pyz
