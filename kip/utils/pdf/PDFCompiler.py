'''Testing module'''
from pathlib import Path
import PyPDF4 as pdf
import os
import sys
import string
from ..Config import Config
from ..Utils import getFiles, getDescriptors, closeDescriptors, hashOfBools
from ...core.ClassConstructor import DefaultParams
from ..Errors import NotAFileError, WrongConfigurationFile, WriteFileError

class PDFCompiler(DefaultParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default('path', '.', Path)
        self.default('config_name','id.conf')
        config_path = self.default('path').joinpath(self.default('config_name'))
        self.default('config_path', config_path)
        try:
            self.config = Config(self.default('config_path'))
        except WrongConfigurationFile:
            pass
        except NotAFileError:
            print('Can\'t find config file. Set config_path parametr.')
        except Exception:
            print('Some shit happens')

    def create(self):
        path = self.default('path')
        dir_path = Path(path)
        files = getFiles(path)
        filtered_files = self.__filter_files(files, self.config.NEEDED_FILES)
        sorted_files = self.__sort_files(filtered_files, self.config.NEEDED_FILES)
        files = sorted_files
        if len(files) < 14:
            print('Not all files!')
            sys.exit(1)
        desks = getDescriptors(files)
        pdf_writer = pdf.PdfFileWriter()
        for desk in desks:
            self.pageManager(desk, pdf_writer)
        self.save(pdf_writer, dir_path)
        closeDescriptors(desks)
        if self.config.isExists('AUTO_CLEAN'):
            for f in files:
                os.remove(f)

    def __filter_files(self, files, fltr):
        return filter(lambda a: any(i in a.name for i in fltr), files)
    
    def __sort_files(self, files, fltr):
        return sorted(files, key=lambda a: hashOfBools((i in a.name for i in fltr)))


    def save(self, pdf_writer, path_obj):
        try:
            with open(path_obj.joinpath('ИД ' + path_obj.name + '.pdf'), 'wb') as f:
                pdf_writer.write(f)
        except:
            raise WriteFileError


    def pageManager(self, desk, pdf_writer, config=None):
        pdf_reader = pdf.PdfFileReader(desk)
        page_count = pdf_reader.getNumPages()
        rotate_angle = -90
        adding_pages = 0
        for page in pdf_reader.pages:
            pdf_writer.addPage(page)
            if page_count % 2 != 0 or any((i in desk.name for i in self.config.ONE_SIDE)):
                pdf_writer.addBlankPage()
                adding_pages += 1
        if any((i in desk.name for i in self.config.ROTATED_FILES)):
            for p in range(page_count + adding_pages, 0, -1):
                pdf_writer.getPage(-p).rotateClockwise(rotate_angle)
                rotate_angle *= -1