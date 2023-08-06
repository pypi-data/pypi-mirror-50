import sys


def print_err(msg, color=True):
    if color:
        msg = '\033[31m' + msg + '\033[39m'
    print(msg, file=sys.stderr)
