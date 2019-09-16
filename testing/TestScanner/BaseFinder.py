import re
from kip.core.ClassConstructor import DefaultParams

class BaseFinder(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        out = []
        pattern = args[0]
        regexp = re.compile(pattern)
        for obj in self.default('where'):
            finding = str(obj.__getattribute__(self.default('field')))
            if len(regexp.findall(finding)) > 0:
                out.append(obj)
        return BaseFinder(where=out)

    def out(self):
        return self.default('where')

    def set_where(self, where):
        self.default('where', where)

    def set_field(self, field):
        self.default('field', field)