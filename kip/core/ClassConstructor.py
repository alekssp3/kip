class DefaultParams():
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    def default(self, key, value=None, vtype=None):
        _value = self.__dict__.get(key)
        if _value is None:
            if value is not None:
                if vtype is not None:
                    if not isinstance(value, (vtype)):
                        self.__dict__.update({key:vtype(value)}) 
                else:
                    self.__dict__.update({key:value})
            else:
                self.__dict__.update({key:value})
        else:
            if vtype is not None:
                    if not isinstance(value, (vtype)):
                        self.__dict__.update({key:vtype(_value)})
            return _value