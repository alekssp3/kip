import openpyxl
import re

def timesheetsum_by_post(filename):
    "Подсчет человекочасов в книге по форме RHI"
    wb = openpyxl.load_workbook(filename)
    ws = wb.sheetnames
    out = []
    pattern = '\s\(.*\)'
    regex = re.compile(pattern)
    for sh in ws:
        _sh = wb.get_sheet_by_name(sh)
        for line in range(9, 49):
            post = _sh['f' + str(line)].value
            work_time = _sh['h'+ str(line)].value
            try:
                normal_sheet_name = sh.replace(regex.findall(sh)[0], '')
            except:
                normal_sheet_name = sh
            if work_time is not None:
                out.append(f'{normal_sheet_name}\t{post}\t{work_time}')
    return out