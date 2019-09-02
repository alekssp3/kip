import os
import sys
import time
from pathlib import Path
from kip.utils.pdf.PDFCompiler import PDFCompiler
# from kip.utils.Config import Config
# from kip.core.utils import make_absolute


# app_path = Path(__file__).parent


def main():
    auto_close = False
    path = None
    if len(sys.argv) > 1 :
        path=sys.argv[1]
    else:
        path = os.getcwd()
    try:
        pdf_compiler = PDFCompiler(path=path)
        pdf_compiler.create()
        auto_close = pdf_compiler.config.isExists('CLOSE_AFTER')
    except Exception:
        auto_close = False
    return auto_close


if __name__ == '__main__':   
    if not main():
        input('Press any enter :(')