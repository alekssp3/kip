import datetime

def get_day(struct, delta_day=0, delta_month=0, delta_year=0):
    out = []
    day = datetime.datetime.today().day - delta_day
    month = datetime.datetime.today().month - delta_month
    year = datetime.datetime.today().year - delta_year

    for file in struct:
        file_day = datetime.datetime.fromtimestamp(file.date.m).day
        file_month = datetime.datetime.fromtimestamp(file.date.m).month
        file_year = datetime.datetime.fromtimestamp(file.date.m).year
        if all((file_day == day, file_month == month, file_year == year)):
            out.append(file)
    return out