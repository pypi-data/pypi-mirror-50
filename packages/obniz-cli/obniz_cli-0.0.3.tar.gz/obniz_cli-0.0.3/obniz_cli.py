import sys
import argparse

from commands import flashos
from commands import eraseos

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_flashos = subparsers.add_parser('flashos', help='see `flashos -h`')
parser_flashos.add_argument('-p', '--port', help='Serial port you want to flash (like: `/dev/tty.SLAB_USBtoUART`)')
parser_flashos.add_argument('-b', '--bps', help='Speen in Serial communication(bps)', default='i')
parser_flashos.set_defaults(handler=flashos.command)

parser_eraseos = subparsers.add_parser('eraseos', help='see `eraseos -h`')
parser_eraseos.add_argument('-p', '--port', help='Serial port you want to flash (like: `/dev/tty.SLAB_USBtoUART`)')
parser_eraseos.set_defaults(handler=eraseos.command)

def main():
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

if __name__=="__main__":
    main()