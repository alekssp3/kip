import zipfile
import datetime

def unzip(filename, folder='.'):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(folder)


def zip_info(archive_name, verbose=False):
    zf = zipfile.ZipFile(archive_name)
    for num, info in enumerate(zf.infolist()):
        print(f'{num + 1} {info.filename}')
        if verbose:
            print(f'\tComment:\t{info.comment}')
            print(f'\tModified:\t{datetime.datetime(*info.date_time)}')
            print(f'\tSystem:\t\t{info.create_system} (0 = Windows, 3 = Unix)')
            print(f'\tZIP version:\t{info.create_version}')
            print(f'\tCompressed:\t{info.compress_size} bytes')
            print(f'\tUncompressed:\t{info.file_size} bytes')
        print()