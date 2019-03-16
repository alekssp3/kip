class Lexem:
    def __init__(self, type='', value=''):
        self.type = type
        self.value = value

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def set(self, type, value):
        self.type = type
        self.value = value

    def update(self, value):
        self.value += value