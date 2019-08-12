from PyPDF4 import PdfFileReader, PdfFileWriter


def closeDescriptor(desk):
    desk.close()


def getDescriptor(file, mode='rb'):
    return open(file, mode)


def get_pages_from_ICJ_scan(name, pages, journal):
    in_desk = getDescriptor(journal)
    out_desk = getDescriptor(name+'.pdf', 'wb')
    pdf_reader = PdfFileReader(in_desk)
    pdf_writer = PdfFileWriter()
    for page in pages:
        pdf_writer.addPage(pdf_reader.getPage(page))
    try:
        with open(name + '.pdf', 'wb') as f:
            pdf_writer.write(f)
    except:
        print('File not writing')
    pdf_writer.write(out_desk)
    closeDescriptor(in_desk)

