class Question:
    YES_NO = '[y|N]'

    def __init__(self):
        self.status = False

    def view(self, question, type):
        query = input(' '.join((question, type, ': ')))
        return query

    def check(self, query):
        if 'y' in query.lower():
            return True
        return False