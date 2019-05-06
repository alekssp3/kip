import re

from .patterns.singleton import singleton


@singleton
class Splitter:

    def by_tab(self, string):
        return re.split(r'\t', string)

    def by_nl(self, string):
        return re.split(r'\n', string)

    def by_dbl_nl(self, string):
        return re.split(r'\n{2}', string)