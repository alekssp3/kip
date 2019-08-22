from pathlib import Path
import re
from kip.utils import data
from kip.utils.dxf.DXFQuery import DXF_QURYES, DXF_TYPES
from kip.core.ClassConstructor import DefaultParams
from kip.utils.Errors import WrongDXFAutodeskString, WrongDXFMicrostationString
from kip.utils.Utils import get_compiled_regex

class DXFFormat:
    def format_microstation(self, dxf_string, joiner='\t'):
        regex_step1 = get_compiled_regex(DXF_QURYES.DXF_SEPARATOR)
        regex_step2 = get_compiled_regex(DXF_QURYES.DXF_NEWLINE)
        try:
            step1 = regex_step1.split(dxf_string)
            step2 = regex_step2.split(step1)
            step3 = joiner.join(step2)
            return step3.strip()
        except Exception:
            raise WrongDXFMicrostationString

    def format_autodesk(self, dxf_string, joiner='\t'):
        regex_step1 = get_compiled_regex(DXF_QURYES.DXF_NEWLINE)
        try:
            step1 = regex_step1.split(dxf_string)
            step2 = joiner.join(step1)
            return step2
        except Exception:
            raise WrongDXFAutodeskString


class DXF(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('filename')
        self.default('query', DXF_QURYES.FIXTURES)
        self.default('project', self.default('filename').name)
        self.default('format', DXF_TYPES.AUTODESK)
        self.default('joiner', '\t')

    def get_data(self):
        buffer = []
        file_buffer = self.load()
        regex = get_compiled_regex(self.default('query'))
        for line in file_buffer:
            finding = regex.findall(line)
            if len(finding) > 0:
                try:
                    buffer.append(self.select_format(line.strip()))
                except Exception:
                    buffer.append(line.strip())
        return buffer

    def load(self):
        return data.load(self.default('filename'))

    def save(self, **kwargs):
        buffer = []
        for line in self.get_data():
            buffer.append('\t'.join((self.default('project'), line)))
        data.save(buffer, self.new_file_name())

    def set_query(self, query):
        self.query = query

    def set_format(self, format):
        self.format = format

    def new_file_name(self):
        filename = str(self.default('filename').name)
        return self.default('filename').parent.joinpath(filename.replace('.dxf','.txt'))

    def select_format(self, dxf_string):
        if DXF_TYPES.MICROSTATION in self.format:
            return DXFFormat().format_microstation(dxf_string, self.default('joiner'))
        elif DXF_TYPES.AUTODESK in self.format:
            return DXFFormat().format_autodesk(dxf_string, self.default('joiner'))
        else:
            return dxf_string