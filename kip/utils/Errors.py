class WrongTypeError(BaseException):
    pass

class NotAFileError(BaseException):
    pass

class WrongConfigurationFile(BaseException):
    def __init__(self): 
        print(f'Wrong configuration file')

class WriteFileError(BaseException):
    def __init__(self): 
        print(f'Can\'t write file')

class StructFieldError(BaseException):
    def __init__(self): 
        print(f'Wrong field in struct')

class WrongDXFMicrostationString(BaseException):
    def __init__(self): 
        print(f'Wrong microstation format string')

class WrongDXFAutodeskString(BaseException):
    def __init__(self): 
        print(f'Wrong autodesk format string')

# class NotFoundError(BaseException):
#     def __init__(self, *args, **kwargs): 
#         print(f'')