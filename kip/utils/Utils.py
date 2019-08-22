import glob
import os
import re
import shutil
import string
from ..gui.UtilsGUI import tk_gui
from pathlib import Path


def get_number(text):
    return int(text) if float(text) == int(text) else float(text) 

def sum_from_text(text, separator=' '):
    _input = text.split(separator)
    if '.' in text or ',' in text:
        return sum([float(i) for i in _input if i != ''])
    return sum([int(i) for i in _input if i != ''])


def get_type_from_text(text):
    words = re.findall(r'\s', text)
    print(f'Data len = {len(words)}')


def get_data_type(data):
    if len(data) < 1:
        pass
    if len(data) == 1:
        pass
    else:
        pass


def __get_var_name(var):
    return [k for k, v in globals().items() if v == var][0]


def get_data(path, db=None):
    if db is None:
        data = []
        for i in path:
            data.extend(glob.glob(i + '/**', recursive=True))
        return data
    return db


def create_dir(dir_name):
    bn = os.path.basename(dir_name)
    pd = os.path.dirname(dir_name) or '.'
    if bn not in os.listdir(os.path.abspath(pd)):
        try:
            os.mkdir(dir_name)
        except Exception:
            # FIXED: Understand with file path!!!
            # I hope this will work
            print('Some shit will be')
        print(f'{dir_name} folder is created')


def combine_folder(data_list, folder):
    create_dir(folder)
    for i in data_list:
        try:
            shutil.copy(i, folder)
        except Exception:
            print(f'Cant copy {i} file')


def get_first_num(text):
    for ch in text:
        if ch in string.digits:
            return ch
    return None


def combine_data(data: list, where: dict):
    for i in where:
        for j in data:
            if i in j:
                where[i] = j
                continue
    return where


# v 0.1
# {data : (type=list),  db : (type=Scanner)}
def find_in_db(data=None, db=None):
    if data is None:
        data = tk_gui('Add data for finding')
    if db is None:
        print('No DB for finding')
        return
    data_dict = dict([(i, None) for i in data])
    combine_data(db, data_dict)
    return data_dict


def start(filename):
    '''Open file in default application'''
    os.startfile(os.path.abspath(filename))


def get_files_descriptors(files_paths):
    descs = []
    for f in files_paths:
        fd = open(f, 'rb')
        descs.append(fd)
    return descs


def close_file_descriptors(file_descriptors):
    for fd in file_descriptors:
        try:
            fd.close()
        except Exception:
            print('Cant close file')


def str_sum(string, splitter=' '):
    if '.' in string:
        return sum([float(i) for i in re.split(splitter, string)])
    return sum([int(i) for i in re.split(splitter, string)])


def str_fill(string, length=3, fill='0', align='right'):
    fill_string = ''
    out = ''
    if len(str(string)) < length:
        fill_string = fill * (length - len(str(string)))
    if align == 'right':
        out = fill_string + str(string)
    elif align == 'left':
        out = str(string) + fill_string
    return out


def decimal_len(string):
    count = 0
    for ch in str(string):
        if ch.isdecimal():
            count += 1
        else:
            break
    return count


def decimal_fill(string, length=3, fill='0', align='right'):
    fill_string = ''
    out = ''
    if decimal_len(string) < length:
        fill_string = fill * (length - decimal_len(string))
    if align == 'right':
        out = fill_string + str(string)
    elif align == 'left':
        out = str(string) + fill_string
    return out


def str_ext(string, splitter=r'\s', length=3, fill='0'):
    out = []
    for val in re.split(splitter, string):
        if '(' in val and ')' in val:
            value, count, post = re.split(r'[\(\)]', val)
            for i in str_ext(count, splitter, length, fill):
                out.append(decimal_fill(value + i + post, length=length, fill=fill))
        elif '-' in val:
            start, end = map(int, re.split('-', val))
            if end < start:
                for i in range(start, end - 1, -1):
                    out.append(decimal_fill(i, length=length, fill=fill))
            else:
                for i in range(start, end + 1):
                    out.append(decimal_fill(i, length=length, fill=fill))
        elif '*' in val:
            value, count = map(int, re.split(r'\*', val))
            for i in range(count):
                out.append(decimal_fill(value, length=length, fill=fill))
        elif '[' in val and ']' in val:
            value, count, post = re.split(r'[\[\]]', val)
            for i in range(len(count)):
                out.append(decimal_fill(value + count[i] + post, length=length, fill=fill))
        else:
            out.append(decimal_fill(val, length=length, fill=fill))
    return out


def reproduce(template, extended, length=3, fill='0'):
    for i in str_ext(extended, length=length, fill=fill):
        print(template.format(i).upper())


def pl(lst):
    '''Print list'''
    for i in lst:
        print(i)


def pne(lst, message, view=False):
    '''Print if not empty'''
    if len(lst) > 0:
        print(message)
        if view:
            pl(lst)


def closeDescriptors(desks):
    for d in desks:
        d.close()


def getDescriptors(files_list, mode='rb'):
    return [open(file, mode) for file in files_list]


def getDescriptor(file, mode='rb'):
    return open(file, mode)


def getFiles(path):
    dir_path = Path(path)
    all_files = list(dir_path.iterdir())
    return all_files


def hashOfBools(bools):
    return sum([j*2**i for i, j in enumerate(list(map(int, bools)))])


def get_compiled_regex(pattern):
    return re.compile(pattern)