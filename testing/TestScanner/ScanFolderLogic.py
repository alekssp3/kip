from pathlib import Path
from testing.TestScanner.BaseLogic import BaseLogic


class ScanFolderLogic(BaseLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do(self, *args, **kwargs):
        try:
            for file in Path(path).iterdir():
                self._file_sorting_logic(file)
        except:
            self._file_errors_logic(path)