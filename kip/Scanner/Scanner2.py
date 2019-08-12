from pathlib import Path
from ..core.ClassConstructor import DefaultParams


class Scanner(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('path', '.', Path)
        # self.default('recursive', 0)
        self.files = []
        self.dirs = []
        self.others = []
        # self.__recursive = 0
        self.__dirs = set()

    # @update_kwargs default('path', self.default('path'))
    def scan(self, *args, **kwargs):
        if 'path' in kwargs:
            path = Path(kwargs['path'])
        else:
            path = Path(self.default('path'))
        self.scan_folder(path=path)
        while len(self.dirs) > 0:
            self.scan_folder(path=self.dirs.pop(0))

    # @update_kwargs
    def scan_folder(self, *args, **kwargs):
        if 'path' in kwargs:
            path = Path(kwargs['path'])
        else:
            path = Path(self.default('path'))
        for file in path.iterdir():
            if file.is_dir():
                if file not in self.__dirs:
                    self.__dirs.add(file.absolute())
                    self.dirs.append(file.absolute())
            elif file.is_file():
                self.files.append(file.absolute())
            else:
                self.others.append(file.absolute())

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]



