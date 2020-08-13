from argparse import ArgumentParser

from .builder import build_exe


def run(*args):
    parser = ArgumentParser(description='Convert .pyz to .exe')
    parser.add_argument('source', help='Path to source py or pyz file')
    parser.add_argument('-o', '--target', help='Path to output file. If not set, the filename of the pyz file is taken')
    parser.add_argument('--icon', help='Path to icon file')
    #parser.add_argument('--version', help='Version of generated executable')
    parser.add_argument('--gui', action='store_true', help='Set if the pyz file contains a application')
    args = parser.parse_args(args=args)

    build_exe(**vars(args))
