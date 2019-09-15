from kip.core.ClassConstructor import DefaultParams

class BaseScanner(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean()

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]

    def clean(self):
        self.files = []
        self.dirs = []
        self.others = []
        self.errors = []