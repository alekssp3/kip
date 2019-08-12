from collections import namedtuple
from ..utils.Project import get_last_proj_rev, get_project_rev
from ..utils.Project import get_last_journal_date, get_journal_date
from pathlib import Path


class PROJECT_STRUCTURES:
    # name path rev
    NPR = ('NRP', 'name path rev')
    NORM = ('NORM', 'zone desc draw rfi date quant')
    RFI = ('RFI', 'rfi ans')
    RFI_STRUCT = ('RFI_STRUCT', 'data path')
    ANS_STRUCT = ('ANS_STRUCT', 'data path')
    NPD = ('NPD', 'name path date')
    SCAN = ('SCAN', 'name path type ext date')
    ZIPSCAN = ('ZIPSCAN', 'name path data type ext date')
    DATE = ('DATE', 'c m a')
    ICJDATA = ('ICJDATA', 'date obj cert qa qp')
    ICJDATASTRUCT = ('ICJDATASTRUCT', 'book sheet data')
    DS = ('DS', 'name data')


def get_structure(struct, data):
    return namedtuple(*struct)._make(data)


def create_new_structure(name, fields):
    return namedtuple(name, fields)


def sum_by_struct_field(struct, field):
    return sum([string_to_num(i.__getattribute__(field)) for i in struct])


def get_structure_from_dict(d: dict, structure):
    out = []
    for struct in zip(d.keys(), d.values()):
        out.append(structure._make(struct))
    return out


def get_projects_structure(projects_list, projects_paths):
    DataStructure = namedtuple(*PROJECT_STRUCTURES.NPR)
    ProjectsStructure = []
    for project in projects_list:
        for path in projects_paths:
            if project.lower() in path.lower():
                ProjectsStructure.append(
                    DataStructure._make((project, Path(path), get_project_rev(project.lower(), path.lower()))))
    return ProjectsStructure


def get_journals_structure(projects_list, projects_paths):
    DataStructure = namedtuple(*PROJECT_STRUCTURES.NPD)
    ProjectsStructure = []
    for project in projects_list:
        for path in projects_paths:
            if project.lower() in path.lower():
                ProjectsStructure.append(
                    DataStructure._make((project, Path(path), get_journal_date(path.lower()))))
    return ProjectsStructure


def get_last_projects_structure(projects_list, projects_structure):
    buffer = []
    for project in projects_list:
        for data_structure in projects_structure:
            if project == data_structure.name and get_last_proj_rev(project, projects_structure) == data_structure.rev:
                if data_structure not in buffer:
                    buffer.append(data_structure)
    return buffer


def get_last_journals_structure(projects_list, projects_structure):
    buffer = []
    for project in projects_list:
        for data_structure in projects_structure:
            if project == data_structure.name and get_last_journal_date(project, projects_structure) == data_structure.date:
                if data_structure not in buffer:
                    buffer.append(data_structure)
    return buffer


def struct_to_string_buffer(struct, splitter='\t'):
    buffer = []
    for line in struct:
        buffer.append(splitter.join(line))
    return buffer


def string_to_num(string):
    num = string.replace(',', '.').strip()
    try:
        num = float(num)
    except Exception:
        print('Not correct numeric string')
    if int(num) == num:
        num = int(num)
    return num


def restruct_rfi_by_draw(rfi_struct, new_struct):
    buffer = []
    for line in rfi_struct:
        spl = line.draw.split(';')
        current_quant = string_to_num(line.quant)
        cur_module = current_quant % len(spl)
        if cur_module != 0:
            quant = [float((current_quant - cur_module) / len(spl)) for _ in range(len(spl))]
            quant[-1] = current_quant - sum(quant[:-1])
        else:
            quant = [float(current_quant / len(spl)) for _ in range(len(spl))]
        for i in range(len(spl)):
            draw = spl[i].split('_')
            if isinstance(quant, (int, float)):
                if int(quant) == quant:
                    quant = int(quant)
                l = new_struct._make((line.zone, line.desc, draw[0], line.rfi, line.date, str(quant).replace('.', ',')))
            else:
                if int(quant[i]) == quant[i]:
                    quant[i] = int(quant[i])
                l = new_struct._make(
                    (line.zone, line.desc, draw[0], line.rfi, line.date, str(quant[i]).replace('.', ',')))
            buffer.append(l)
    return buffer


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


def get_finding_list(string, lst):
    out = []
    for l in lst:
        if string.lower() in l.lower():
            out.append(l)
    return out


def find_list_in_list(lst1, lst2):
    out = []
    LIL = create_new_structure('LIL', 'field data')
    for l1 in lst1:
        out.append(LIL._make((l1, find_str_in_list(l1, lst2))))
    return out


def get_findings_lists(lst1, lst2):
    out = []
    LIL = create_new_structure('LIL', 'field data')
    for l1 in lst1:
        out.append(LIL._make((l1, get_finding_list(l1, lst2))))
    return out