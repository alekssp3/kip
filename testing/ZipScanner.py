import zipfile
import rarfile
import patoolib
from kip.utils.Structures import PROJECT_STRUCTURES, get_structure
from kip.core.ClassConstructor import DefaultParams
from pathlib import Path
from kip.Scanner.Scanner import Scanner
from kip.utils.Utils import pne

class ZipScanner(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('path', '.', Path)
        self.default('filter', 'zip')
        self.errors = []

    def scan(self):
        scanner = Scanner().scan(self.path)
        files = [i for i in scanner.get_struct() if self.filter in i.ext]
        return files

    def get_struct(self):
        out = []
        for i in self.scan():
            p = Path(i.path)
            try:
                zf = self.getArchiveFile(p)
                if zf is None:
                    # print(f'Error with {p}')
                    self.errors.append(p)
                    continue
            except:
                self.errors.append(p)
                # print(f'Error with {p}')
                continue
            d = {'name':p.name, \
                'path':p.absolute(), \
                'data':zf.namelist(), \
                'type': 'd' if p.is_dir() else 'f', \
                'ext': p.suffix,\
                'date': get_structure(PROJECT_STRUCTURES.DATE, ([p.stat().st_ctime, \
                    p.stat().st_mtime, \
                    p.stat().st_atime]))}
            out.append(get_structure(PROJECT_STRUCTURES.ZIPSCAN, d.values()))
        return out    

    def find(self, what):
        out = []
        for st in self.get_struct():
            for d in st.data:
                if what in d:
                    out.append(st)
        pne(self.errors, 'Run scanErrors')
        return out

    def getArchiveFile(self, file:Path, verbose=False):
        archive_file = None
        if 'zip' in file.suffix:
            try:
                archive_file = zipfile.ZipFile(file)
            except:
                if verbose:
                    print(f'Bad zip file {file}')
                    print('Trying open as rar file')
                try:
                    archive_file = rarfile.RarFile(str(file))
                except:
                    if verbose:
                        print(f'Cant read {file} as rar')
        if 'rar' in file.suffix:
            try:
                archive_file = rarfile.RarFile(str(file))
            except:
                if verbose:
                    print(f'Bad rar file {file}')
        return archive_file

    def scanErrors(self):
        for e in self.errors:
            if e is not None:
                patoolib.list_archive(str(e))