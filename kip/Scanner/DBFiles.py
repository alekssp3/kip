from kip.Scanner.Scanner import Scanner
import os
from kip.utils.zip.zip import unzip

def load(db_name, temp_folder='.', remove_after=True):
    s = Scanner()
    db_uncompresed = os.path.abspath(db_name.replace('.dbz', '.dbraw'))
    print(db_uncompresed)
    if db_name.endswith('.dbz'):
        print(db_name)
        print(os.path.dirname(db_name))
        print(os.path.abspath(os.path.dirname(db_name)))

        unzip(db_name, os.path.dirname(db_name))
        s.load(db_uncompresed)
        if remove_after:
            os.remove(db_uncompresed)
    else:
        s.load(db_name)
    return s


def save(db_name, temp_folder='.'):
    pass