import os
import sys
from pathlib import Path
from kip.Scanner.Scanner import Scanner

def main(*args, **kwargs):
    print(sys.argv)
    if len(sys.argv) > 1:
        scanner = Scanner().scan(sys.argv[1])
    else:
        usage()
        sys.exit(0)

    input('Eny Enter for exit')


def usage():
    print('Usage appname param')

if __name__ == '__main__':
    main()