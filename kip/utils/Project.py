import re
import string
from .Utils import get_first_num
from pathlib import Path


def get_project_rev(project, path):
    buffer = []
    end = re.split(project, path)[-1]
    for ch in end[end.index(get_first_num(end)):]:
        if ch in string.digits:
            buffer.append(ch)
        else:
            break
    return int(''.join(buffer))


def get_journal_date(project):
    return Path(project).stat().st_ctime
    

def get_last_rev(data):
    return max([i.rev for i in data])


def get_last_proj_rev(proj, data):
    return max([i.rev for i in data if proj in i.name])


def get_last_journal_date(proj, data):
    return max([i.date for i in data if proj in i.name])


def get_file_type(path):
    if '.' not in path:
        return ''
    else:
        return path.split('.')[-1]
