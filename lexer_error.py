
class LexerError(Exception):
    ''' Signifies an error when using a lexer. '''

    def __init__(self, string):
        ''''''
        super().__init__(string)
