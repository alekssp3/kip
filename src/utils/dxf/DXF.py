import os

from ..Utils import load
from .DXFQuery import DXF_QURYES


def get_data_from_dxf(filename, dxf_query):
    buffer = []
    file_buffer = load(filename)
    for line in file_buffer:
        finding = re.findall(dxf_query, line)
        if len(finding) > 0:
            buffer.append(line.strip())
    return buffer


class WrongDXFString(Exception):
    def __str__(self):
        return 'Wrong dxf string'


class WrongFileFormat(Exception):
    def __str__(self):
        return 'Wrong file format'


def format_microstation(dxf_string):
    try:
        return '\t'.join(re.split(DXF_QURYES.DXF_NEWLINE, re.split(r';', dxf_string)[2])).strip()
    except Exception:
        raise WrongDXFString


def format_autodesk(dxf_string):
    try:
        return '\t'.join(re.split(DXF_QURYES.DXF_NEWLINE, dxf_string))
    except Exception:
        raise WrongDXFString


def get_project_name(project):
    return os.path.basename(project).replace('.dxf', '\t')


def select_format(dxf_string, filetype='microstation'):
    if 'microstation' in filetype:
        return format_microstation(dxf_string)
    else:
        return format_autodesk(dxf_string)


def save_data_from_dxf_to_file(projects_list, filename, filetype='microstation', dxf_query=DXF_QURYES.FIXTURES):
    buffer = []
    for project in projects_list:
        for line in get_data_from_dxf(project, dxf_query):
            try:
                buffer.append(get_project_name(project) + select_format(line, filetype))
            except Exception:
                buffer.append(get_project_name(project) + line)
    save(buffer, filename)


