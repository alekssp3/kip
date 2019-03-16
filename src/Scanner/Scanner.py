import os
import re
from datetime import time

from utils.Utils import unzip, save, load


def load_db(db_name, temp_folder='.'):
    s = Scanner()
    db_uncompresed = os.path.abspath(db_name.replace('.dbz', '.dbraw'))
    if db_name.endswith('.dbz'):
        unzip(db_name, temp_folder)
        s.load(db_uncompresed)
        os.remove(db_uncompresed)
    else:
        s.load(db_name)
    return s


def save_db(db_name, temp_folder='.'):
    pass


class Scanner:
    def __init__(self, path=None, dirs=None, files=None):
        self.path = path or os.path.abspath(os.getcwd())
        self.dirs = dirs or []
        self.files = files or []
        self.errors = []
        self.verbose = False
        self.queryes = []
        self.warnings = []

    def info(self):
        print(f'Now {len(self.files)} files in database')
        if len(self.warnings) > 0:
            print(f'Warnings {len(self.warnings)}')
            if self.verbose:
                for i in self.warnings:
                    print(i)
        if len(self.errors) > 0:
            print(f'Errors {len(self.errors)}')
            if self.verbose:
                for i in self.errors:
                    print(i)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]

    def __sort_dir_data(self):
        for i in os.listdir('.'):
            abs_path = os.path.abspath(i)
            if os.path.isdir(i):
                self.dirs.append(abs_path)
            else:
                if abs_path not in self.files:
                    self.files.append(os.path.abspath(i))
                else:
                    self.warnings.append('\t'.join((abs_path, ' Reapeting')))

    def scan_folder(self, update_query=True):
        startdir = os.path.abspath(os.getcwd())
        self.dirs.append(self.path)
        if update_query:
            self.queryes.append([self.path, os.path.abspath(self.path)])
        while len(self.dirs) > 0:
            if self.verbose:
                for i in self.dirs:
                    print(i, end=' ')
            curpath = self.dirs.pop(0)
            try:
                os.chdir(curpath)
            except Exception:
                pass
            try:
                self.__sort_dir_data()
            except Exception:
                self.errors.append(curpath)
        os.chdir(startdir)
        self.info()

    def find(self, what, case_sensitive=False):
        out = []
        if case_sensitive:
            pattern = re.compile(what)
        else:
            pattern = re.compile(what, re.IGNORECASE)
        for i in self.files:
            finding = pattern.findall(i)
            if len(finding) > 0:
                out.append(i)
        return out

    def scan(self, path=None, update_query=True):
        self.path = path or self.path
        if isinstance(path, (str)):
            self.scan_folder(update_query)
        else:
            try:
                for p in path:
                    self.scan(p)
            except Exception:
                print(f'Cant scan {p}')
        return self

    def update(self):
        current_queryes = [q[1] for q in self.queryes]
        update_query = False
        self.files = []
        for p in current_queryes:
            self.scan(p, update_query)
        return

    def save(self, db_name=None):
        timestamp = '%d%m%Y%H%M%S'
        if db_name is None:
            db_name = time.strftime(timestamp) + '.db'
        buffer = []
        buffer.append(' '.join(map(str, (len(self.queryes), len(self.files)))))
        buffer += ['\t'.join(i) for i in self.queryes]
        buffer += self.files
        save(buffer, db_name)

    def load(self, db_name):
        # TODO: read and write as bites
        # TODO: add hash
        buffer = load(db_name)
        querry_len, data_len = map(int, buffer[0].split())
        querry = [list(line.split('\t')) for line in buffer[1:querry_len + 1]]
        data = buffer[querry_len + 1:]
        # simple hash checking
        if len(data) == data_len:
            print('Data status: OK')
        self.queryes = querry
        self.files = data

    def clean(self):
        self.errors = []
        self.dirs = []
        self.files = []
        self.path = []
        self.queryes = []

    def upgrade(self, db_file):
        save(self.files, db_file)