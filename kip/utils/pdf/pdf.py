from PyPDF4 import PdfFileWriter, PdfFileReader, PdfFileMerger
from ..Utils import get_files_descriptors, close_file_descriptors


def pdf_merge(files_paths, file_name):
    pdf_writer = PdfFileWriter()
    descs = get_files_descriptors(files_paths)
    for fd in descs:
        try:
            pdf_reader = PdfFileReader(fd)
        except Exception:
            print('Cant read file')
        for page in range(pdf_reader.getNumPages()):
            try:
                pdf_writer.addPage(pdf_reader.getPage(page))
            except Exception:
                print('Cant merge file')
    with open(file_name, 'wb') as f:
        try:
            pdf_writer.write(f)
        except Exception:
            print('Cant write file')
        finally:
            close_file_descriptors(descs)
            print('All descriptors are closed')


def merger(input_paths, output_path):
    pdf_merger = PdfFileMerger()
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
