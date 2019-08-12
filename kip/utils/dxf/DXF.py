import os
import re
from ...utils import data
from .DXFQuery import DXF_QURYES, DXF_TYPES


class DXF_FORMAT:
    def format_microstation(dxf_string):
        try:
            step1 = re.split(DXF_QURYES.DXF_SEPARATOR, dxf_string)
            step2 = re.split(DXF_QURYES.DXF_NEWLINE, step1)
            step3 = '\t'.join(step2)
            return step3.strip()
        except Exception:
            raise WrongDXFMicrostationString

    def format_autodesk(dxf_string):
        try:
            step1 = re.split(DXF_QURYES.DXF_NEWLINE, dxf_string)
            step2 = '\t'.join(step1)
            return step2
        except Exception:
            raise WrongDXFAutodeskString


class DXF:
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.query = DXF_QURYES.FIXTURES
        self.project = self.get_name()
        self.format = DXF_FORMAT.AUTODESK

    def get_data(self):
        buffer = []
        file_buffer = data.load(self.filename)
        for line in file_buffer:
            finding = re.findall(self.query, line)
            if len(finding) > 0:
                buffer.append(line.strip())
        return buffer

    def save(self, **kwargs):
        buffer = []
        for line in self.get_data():
            try:
                buffer.append(self.project + self.select_format(line))
            except Exception:
                buffer.append(self.project + line)
        data.save(buffer, self.filename+'.txt')

    def set_query(self, query):
        self.query = query

    def set_format(self, format):
        self.format = format

    def get_name(self):
        return os.path.basename(self.filename).replace('.dxf', '\t')

    def select_format(self, dxf_string):
        if DXF_TYPES.MICROSTATION in self.format:
            return DXF_FORMAT.format_microstation(dxf_string)
        elif DXF_TYPES.AUTODESK in self.format:
            return DXF_FORMAT.format_autodesk(dxf_string)
        else:
            return dxf_string


class WrongDXFMicrostationString(Exception):
    pass


class WrongDXFAutodeskString(Exception):
    pass
