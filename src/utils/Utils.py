import glob
import os
import re
import shutil
import string
import zipfile
import datetime
from collections import namedtuple
import tkinter as tk

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from .Config import Config

def sum_from_text(text, separator=' '):
    l = text.split(separator)
    if '.' in text or ',' in text:
        return sum([float(i) for i in l if i != ''])
    return sum([int(i) for i in l if i != ''])


def __get_var_name(var):
    return [k for k, v in globals().items() if v == var][0]


def unzip(filename, folder='.'):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(folder)


def zip_info(archive_name, verbose=False):
    zf = zipfile.ZipFile(archive_name)
    for num, info in enumerate(zf.infolist()):
        print(f'{num + 1} {info.filename}')
        if verbose:
            print(f'\tComment:\t{info.comment}')
            print(f'\tModified:\t{datetime.datetime(*info.date_time)}')
            print(f'\tSystem:\t\t{info.create_system} (0 = Windows, 3 = Unix)')
            print(f'\tZIP version:\t{info.create_version}')
            print(f'\tCompressed:\t{info.compress_size} bytes')
            print(f'\tUncompressed:\t{info.file_size} bytes')
        print()


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


def get_project_rev(project, path):
    buffer = []
    end = re.split(project, path)[-1]
    for ch in end[end.index(get_first_num(end)):]:
        if ch in string.digits:
            buffer.append(ch)
        else:
            break
    return int(''.join(buffer))


def get_last_rev(data):
    return max([i.rev for i in data])


def get_last_proj_rev(proj, data):
    return max([i.rev for i in data if proj in i.name])


def get_file_type(path):
    if '.' not in path:
        return ''
    else:
        return path.split('.')[-1]


def combine_data(data: list, where: dict):
    for i in where:
        for j in data:
            if i in j:
                where[i] = j
                continue
    return where


# v 0.2.5
def check_rfi(rfi_list, rfi_db=None, answers_db=None):
    RFI = create_new_structure(*PROJECT_STRUCTURES.RFI)
    rfi_dict = find_in_db(rfi_list, rfi_db)
    # RFI_STRUCT = create_new_structure(*PROJECT_STRUCTURES.RFI_STRUCT)
    # rfi_struct = get_structure_from_dict(rfi_dict, RFI_STRUCT)
    answers_dict = find_in_db(rfi_list, answers_db)
    # ANSWER_STRUCT = create_new_structure(*PROJECT_STRUCTURES.ANS_STRUCT)
    # answers_struct = get_structure_from_dict(answers_dict, ANSWER_STRUCT)
    return RFI._make((rfi_dict, answers_dict))


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


def pdf_merge(files_paths, file_name):
    pdf_writer = PdfFileWriter()
    descs = get_files_descriptors(files_paths)
    for fd in descs:
        try:
            pdf_reader = PdfFileReader(fd)
        except Exception:
            print('Cant read file')
        for page in range(pdf_reader.getNumPages()):
            try:
                pdf_writer.addPage(pdf_reader.getPage(page))
            except Exception:
                print('Cant merge file')
    with open(file_name, 'wb') as f:
        try:
            pdf_writer.write(f)
        except Exception:
            print('Cant write file')
        finally:
            close_file_descriptors(descs)
            print('All descriptors are closed')


def merger(input_paths, output_path):
    pdf_merger = PdfFileMerger()
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


class QUESTION:
    YES_NO = '[y|N]'

    def __init__(self):
        self.status = False

    def view(self, question, type):
        query = input(' '.join((question, type, ': ')))
        return query

    def check(self, query):
        if 'y' in query.lower():
            return True
        return False


def check_and_merge(out_file, rfi_list=None, rfi_db=None, answers_db=None, open_on_done=True):
    if rfi_list is None:
        rfi_list = tk_gui("Add rfi's")
    if '.pdf' in out_file:
        save(rfi_list, out_file.replace('.pdf', '.txt'))
    else:
        save(rfi_list, out_file + '.txt')

    paths = check_rfi(rfi_list, rfi_db, answers_db)
    pdf_merge(paths.rfi.values(), out_file)
    if not open_on_done:
        q = QUESTION()
        if q.check(q.view('Open file in editor', QUESTION.YES_NO)):
            os.startfile(os.path.abspath(out_file))
    else:
        os.startfile(os.path.abspath(out_file))


class Check_and_merge_gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.out = []
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # self.lable = tk.Label(self)
        # self.lable['text'] = "File name"
        # self.lable.pack()

        # self.filename = tk.Entry(self)
        # self.filename.pack()

        self.text = tk.Text(self)
        self.text.pack(side='top')

        self.combine = tk.Button(self)
        self.combine['text'] = 'Done'
        self.combine["command"] = self.get_lines_from_text
        self.combine.pack(side="bottom")

        # self.open_doc = tk.Checkbutton(self)
        # self.open_doc['text'] = 'Open file after combine'
        # self.open_doc.select()
        # self.open_doc.pack()

    def get_lines_from_text(self):
        out = []
        lines = ''.join(self.text.get('1.0', tk.END))
        for i in lines.split('\n'):
            if len(i) > 0:
                out.append(i)
        self.out = out
        self.master.destroy()

    # def merge(self):
    #     check_and_merge(self.filename.get(), self.get_lines_from_text(), open_on_done=self.open_doc.state)


def tk_gui(title=''):
    root = tk.Tk()
    root.title = title
    app = Check_and_merge_gui(master=root)
    app.mainloop()
    return app.out


def check_and_combine(rfi_list=None, folder=None, rfi_db=None, answers_db=None, excludes=None, exactly=None):
    # folder_name = folder_name or ''.join(rfi_list.split('.')[:-1])
    if rfi_list is None:
        rfi_list = tk_gui("Add rfi's")

    if folder is None:
        folder = tk_gui("Add folder name")

    rfi_db = rfi_db or Scanner.load_db(Config.RFI_DB_PATH)
    answers_db = answers_db or Scanner.load_db(Config.ANSWER_DB_PATH)
    # excludes = excludes or load(rfi_list+'.excludes')
    # exactly = exactly or load(rfi_list+'.exactly')
    data = check_rfi(rfi_list, rfi_db, answers_db)
    combine_folder(data.rfi.values(), folder)
    return data



# def check_and_combine_2(data_list, folder, database):
#     data = check_data(data_list, database)
#     combine_folder(data[0].values(), folder)
#     return data


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





def lists_compare(list1, list2):
    min_list = list1
    max_list = list2
    if len(min_list) > len(max_list):
        min_list, max_list = max_list, min_list
    buffer = []
    for unit in min_list:
        if unit not in max_list:
            buffer.append(unit)
    return buffer


def find_str_in_list(string, lst):
    out = []
    for l in lst:
        if string.lower() in l.lower():
            out.append(1)
        else:
            out.append(0)
    return sum(out)


def find_list_in_list(lst1, lst2):
    out = []
    LIL = create_new_structure('LIL', 'field data')
    for l1 in lst1:
        out.append(LIL._make((l1, find_str_in_list(l1, lst2))))
    return out