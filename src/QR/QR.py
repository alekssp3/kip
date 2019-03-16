import qrcode

class QR():
    def __init__(self, text=''):
        self.text = text

    def get_qr(self, text=None, type='ascii'):
        if text is None:
            text = self.text
        qr = qrcode.QRCode()
        qr.add_data(self.text)
        if type == 'ascii':
            qr.print_ascii()
        else:
            qr.print_tty()