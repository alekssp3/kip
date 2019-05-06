import os

class Config:
    DEFAULT_PATH = ''.join((r'C:\Users\\', os.getlogin()))
    RFI_FIND_PATH = (r'P:\RFI\Salamat_Suerkul', r'C:\Users\Al\Downloads',)
    RFI_DB_PATH = r'P:\rfi.dbz'
    ANSWER_FIND_PATH = (r'P:\RFI\02 RHI-ZSN.0560-RFI_ответы',)
    ANSWER_DB_PATH = r'P:\ANSWERS.dbraw'
    PROJECT_FIND_PATH = (r'P:\00-General_plan', r'P:\01-E&I_PROJECTS',)
    PROJECT_DB_PATH = r'P:\PROJECTS.dbraw'
