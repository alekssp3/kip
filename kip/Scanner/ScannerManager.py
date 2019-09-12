from kip.Scanner.Scanner import Scanner

def loadOrCreateScanner(db_file, scanning_path, autosave=True):
    scanner = Scanner()
    if db_file.exists():
        scanner.load(db_file)
    else:
        scanner.scan(scanning_path)
        if autosave:
            scanner.save(db_file)
    return scanner