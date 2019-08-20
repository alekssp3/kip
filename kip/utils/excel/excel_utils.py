from ..Structures import PROJECT_STRUCTURES
from collections import namedtuple
import xlrd
import pyxlsb
from testing.excelb2x import get_data_from_xlsb, write_data_to_xlsx

def get_data_from_icj(sheet, start_row=3):
    out = []
    for i in range(start_row, sheet.nrows):
        if isinstance(sheet.cell_value(i, 0), (float, int)):
            d = {'date': sheet.cell_value(i, 0), \
                'obj': sheet.cell_value(i, 1), \
                'cert': sheet.cell_value(i, 2), \
                'quant': sheet.cell_value(i, 3), \
                'unit': sheet.cell_value(i, 4)}
            out.append(create_struct_from_dict(PROJECT_STRUCTURES.ICJDATA, d))
    return out


def create_struct_from_dict(struct, d:dict):
    return namedtuple(*struct)._make(d.values())


def get_needed_sheet(workbook):
    for sheet in workbook.sheets():
        # print(sheet.name)
        try:
            if sheet.ncols * sheet.nrows > 0:
                if sheet.cell(0,0).value == 'Дата записи':
                    return sheet
        except:
            print(f'Cant find needed sheet in {workbook}')
            pass


def get_workbooks(path_list):
    out = []
    for wb in path_list:
        out.append(xlrd.open_workbook(wb))
    return out


def get_workbook(path):
    if path.suffix == '.xlsb':
        return xlrd.open_workbook(write_data_to_xlsx(get_data_from_xlsb(path), path))
    return xlrd.open_workbook(path)


def close_workbooks(wb_list):
    for wb in wb_list:
        wb.close()


def get_icj_sheets(workbooks):
    out = []
    for wb in workbooks:
        out.append(get_needed_sheet(wb))
    return out