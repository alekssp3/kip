import string

from Parser.Token import Token


class Tokenizer:
    def __init__(self, string):
        self.string = string
        # self.token_types = ['NUMBER', 'RANGE', 'OPERATOR', 'SPACE']
        # self.token_value = ['1234567890', '(){}[]-', '*', ' ']
        self.__init_tokens()

    def __init_tokens(self):
        self.tokens = []
        self.tokens.append(Token('Start'))
        self.tokens.append(Token('End'))
        self.tokens.append(Token('Number', string.digits))
        self.tokens.append(Token('Symbol', string.ascii_lowercase))
        self.tokens.append(Token('StartEnum', '['))
        self.tokens.append(Token('EndEnum', ']'))
        self.tokens.append(Token('Range', '-'))
        self.tokens.append(Token('Space', string.whitespace))
        self.tokens.append(Token('Operation', '*'))
        self.tokens.append(Token('Undefined'))

    def tokenize(self):
        tokenized = []
        for ch in self.string:
            tokenized.append(self.get_token(ch))
        return tokenized

    def get_token(self, character):
        for token in self.tokens:
            if character in token.get_value():
                return Token(token.get_type(), character)
        return Token('Undefined')