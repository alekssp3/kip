class DXF_QURYES:
    FIXTURES = r'[A-Za-z]\d{3}-L.*$'
    HTP_PANELS = r'[A-Za-z]{3}-.*\..*-.*-.*$'
    DXF_NEWLINE = r'\\P'
    DXF_SEPARATOR = r';'
    TRAY = r'L='


class DXF_TYPES:
    MICROSTATION = 'microstation'
    AUTODESK = 'autodesk'
