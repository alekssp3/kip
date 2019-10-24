from pathlib import Path
from testing.TestScanner.BaseScanner import BaseScanner
from time import time


class Scanner(BaseScanner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('path', '.', Path)

    def scan(self, *args, **kwargs):
        start = time()
        _path = self._akd_selection_logic('path', self.default('path'), *args, **kwargs)
        self.default('path', _path)
        self._folder_scaning_logic(_path)
        self._file_scaning_logic()
        end = time()
        if 'debug' in kwargs:
            print(f'Runing time: {end-start}')

    def _akd_selection_logic(self, param, default, *args, **kwargs):
        'args-kwargs-default selection'
        if str(param) in kwargs:
            out = kwargs[str(param)]
        elif len(args) > 0 and str(param) not in kwargs:
            out = args[0]
        else:
            out = default
        return out

    def _folder_scaning_logic(self, path, *args, **kwargs):
        # ScanFolderLogic(path)
        try:
            for file in Path(path).iterdir():
                self._file_sorting_logic(file)
        except:
            self._file_errors_logic(path)

    def _file_sorting_logic(self, file):
        _file_abs = file.absolute()
        if file.is_dir():
            if _file_abs not in self.dirs:
                self.dirs.append(_file_abs)
        elif file.is_file():
            if str(_file_abs) not in self.files:
                self.files.append(str(_file_abs))
        else:
            if _file_abs not in self.other:
                self.others.append(_file_abs)

    def _file_scaning_logic(self):
        while len(self.dirs) > 0:
            self._folder_scaning_logic(Path(self.dirs.pop(0)))

    def _file_errors_logic(self, path):
        self.errors.append(path.absolute())

    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

