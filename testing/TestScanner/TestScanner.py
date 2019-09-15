from pathlib import Path
from testing.TestScanner.BaseScanner import BaseScanner


class Scanner(BaseScanner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('path', '.', Path)

    def scan(self, path='.', *args, **kwargs):
        self._scan_folder(Path(path))
        self._file_scaning_logic()

    def _scan_folder(self, path:Path, *args, **kwargs):
        try:
            for file in path.iterdir():
                self._file_sorting_logic(file)            
        except:
            self._file_errors_logic(path)

    def _file_sorting_logic(self, file):
        if file.is_dir():
                # if file not in self.__dirs:
                #     self.__dirs.add(file.absolute())
                #     self.dirs.append(file.absolute())
            self.dirs.append(file.absolute())
        elif file.is_file():
            self.files.append(file.absolute())
        else:
            self.others.append(file.absolute())

    def _file_scaning_logic(self):
        while len(self.dirs) > 0:
            self._scan_folder(Path(self.dirs.pop(0)))

    def _file_errors_logic(self, path):
        self.errors.append(path.absolute())
