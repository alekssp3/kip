from kip.core.ClassConstructor import DefaultParams


class BaseLogic(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do(self, *args, **kwargs):
        raise NotImplementedError