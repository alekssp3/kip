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
            finding = self.__get_or_call__(obj)
            if len(regexp.findall(finding)) > 0:
                out.append(obj)
        return BaseFinder(where=out)

    def out(self):
        return self.default('where')

    def set(self, *args, **kwargs):
        if len(args) > 0:
            where = args[0]
            args = args[1:]
            kwargs['where'] = where
        if len(args) > 0:
            field = args[0]
            args = args[1:]
            kwargs['field'] = field
        super().__init__(*args, **kwargs)

    def __get_or_call__(self, obj):
        obj = obj.__getattribute__(self.default('field'))
        if '__call__' in dir(obj):
            return str(obj())
        return str(obj)