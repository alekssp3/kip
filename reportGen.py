import xlrd

cable_range = range(2000)
sensor_range = [3021, 3022, 3025]
controler_range = [3011,]
box_range = [2000, 2001, 2002, 2003, 2004, 2010, 3004, 4010]
exclude_range = [1111, 2222, 3333, 4444, 5555]


def getInt(text):
    try:
        return int(text)
    except:
        return


def get_number(text):
    return int(text) if float(text) == int(text) else float(text) 


def getReportFromEHTBook(path):
    out = []
    wb = xlrd.open_workbook(path)
    sh1 = wb.sheet_by_name('DB')
    sh2 = wb.sheet_by_name('Матрица POSов')
    sh3 = wb.sheet_by_name('Основа')
    date = sh1.cell(9,3).value
    pipl = ''
    pipe = sh1.cell(9,1).value
    proj = sh1.cell(5,1).value
    circ = sh1.cell(10,1).value
    if ',' in circ:
        circ = [i.strip() for i in circ.split(',')]
    # for j in range(11, 21):
    if isinstance(circ, str):
        # print('One circuit')
        for i in range(1, 130):
            _q = 0
            try:
                _q = get_number(sh2.cell(i, 11).value)
            except:
                pass
            if _q > 0:
                pos = getInt(sh2.cell(i, 1).value)
                desk = sh2.cell(i, 8).value
                u = sh2.cell(i, 10).value
                if pos not in exclude_range and \
                    (pos in cable_range or \
                    pos in sensor_range or \
                    pos in controler_range or \
                    pos in box_range):
                    out.append([date, pipl, pipe, proj, circ, pos, desk, u, _q])
    else:
        # print('Some circuits')
        for c in range(len(circ)):
            for i in range(9, 150):
                _q = 0
                try:
                    _q = get_number(sh3.cell(i, c + 11).value)
                except:
                    pass
                if _q > 0:
                    pos = getInt(sh3.cell(i, 1).value)
                    desk = sh2.cell(i-8, 8).value
                    u = sh2.cell(i-8, 10).value
                    if pos not in exclude_range and \
                        (pos in cable_range or \
                        pos in sensor_range or \
                        pos in controler_range or \
                        pos in box_range):
                        out.append([date, pipl, pipe, proj, circ[c], pos, desk, u, _q])
    return out