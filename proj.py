import os
import sys
import importlib as imp


sys.path.insert(0, os.path.abspath(r'kip'))


def run():
    import main as kip
    global kip


def reload():
    imp.reload(kip)
