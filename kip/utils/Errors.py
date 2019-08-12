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