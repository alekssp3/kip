from kip.core.ClassConstructor import DefaultParams


class Sorting(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('query', '')

    def sort(self):
        pass

class DateSorting(Sorting):
    pass

class StructSorting(Sorting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('struct', '')