from ..utils.data import load
from ..utils.text import isAllNumber
from ..utils.Errors import WrongConfigurationFile
import time

class Config:
    '''Load configuration from file '''

    def __init__(self, path=None, *args, **kwargs):
        self.__path__ = path
        self.__dict__.update(kwargs)
        self.__delimetr__ = ','
        self.__load__()

    def __load__(self):
        data = load(self.__path__)
        out = dict()
        for d in data:
            if not (d.startswith('#') or d == ''):
                # if '=' in d:
                try:
                    d1, d2 = d.split('=')
                except Exception:
                    self.__dict__ = dict()
                    raise WrongConfigurationFile
                d1 = d1.strip()
                if self.__delimetr__ in d2:
                    d2 = d2.split(self.__delimetr__)
                    out.update({d1: tuple(i.strip() for i in d2)})
                else:
                    out.update({d1: d2.strip()})
                    # out.update({d1: tuple(i.strip() for i in d2)})
                # for _d in d2:
                #     isAllNumber(_d)
                
                # else:
                #     out.update({d1: ''})
        self.__dict__.update(out)


    def isExists(self, key):
        return key in self.__dict__.keys()


    def __getattribute__(self, name):
        atr = None
        try:
            atr = super().__getattribute__(name)
        except Exception:
            pass
        return atr
