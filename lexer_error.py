
class LexerError(Exception):
    ''' Signifies an error when using a lexer. '''

    def __init__(self, *args):
        ''''''
        super().__init__(*args)
