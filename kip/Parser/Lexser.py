from Parser.Lexem import Lexem
from Parser.Token import Token


class Lexer:
    def __init__(self, tokenized):
        self.token_list = tokenized
        self.length = len(self.token_list)
        self.position = 0
        self.__init_tokens()

    def __init_tokens(self):
        self.lexems = []
        self.lexems.append(Lexem('NumberLexem'))
        self.lexems.append(Lexem('WordLexem'))
        self.lexems.append(Lexem('RangeLexem'))
        self.lexems.append(Lexem('RepetitionLexem'))
        self.lexems.append(Lexem('EnumerateLexem'))
        self.lexems.append(Lexem('EOFLexem'))

    def peek(self, relatve_position=0):
        current_position = self.position + relatve_position
        if current_position >= self.length:
            return Lexem('EOFLexem')
        self.position = current_position + 1
        return self.token_list[current_position]

    def next(self):
        self.peek(1)

    def lexing(self):
        previous_token = Token('Start')
        current_token = self.token_list.pop(0)
        if current_token.get_type() == "Number":
            pass
        elif current_token.get_type() == "Symbol":
            pass
        elif current_token.get_type() == "Range":
            pass
        elif current_token.get_type() == "Symbol":
            pass
        elif current_token.get_type() == "StartEnum":
            pass
        elif current_token.get_type() == "EndEnum":
            pass