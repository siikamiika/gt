"""This module contains the `preprocess' function that converts JavaScript
objects into JSON ones."""

def preprocess(source):
    """Converts JavaScript-compatible data structures sent by Google Translate
    to a valid JSON.

    The only known differences are:
        * omitting of 'null' inside arrays;
        * an optional meaningless comma before ']'.

    >>> preprocess('[1,,2]')
    '[1,null,2]'

    >>> preprocess('[,1,2]')
    '[null,1,2]'

    >>> preprocess('[,,1,,2]')
    '[null,null,1,null,2]'

    >>> preprocess('[1,2,]')
    '[1,2]'

    >>> preprocess('[1,2,,]')
    '[1,2,null]'
    """

    class ParserState:
        """Going to append next symbol as-is"""
        NORMAL = 1
        """Going to append 'null' if the next symbol is comma"""
        COMMA = 2
        """We're inside a string; going to wait for an unescaped comma"""
        STRING = 3
        """We're inside a string, previos character is a backslash"""
        STRING_ESCAPE = 4

    state = ParserState.NORMAL
    result = ''

    for symbol in source:
        if state == ParserState.NORMAL:
            if symbol in ',[':
                state = ParserState.COMMA
            elif symbol == '"':
                state = ParserState.STRING

        elif state == ParserState.COMMA:
            if symbol == ',':
                result += 'null'
            elif symbol == ']':
                result = result.rstrip(',')
                state = ParserState.NORMAL
            elif symbol == '"':
                state = ParserState.STRING
            elif symbol != '[' and not symbol.isspace():
                state = ParserState.NORMAL

        elif state == ParserState.STRING:
            if symbol == '"':
                state = ParserState.NORMAL
            elif symbol == '\\':
                state = ParserState.STRING_ESCAPE

        elif state == ParserState.STRING_ESCAPE:
            state = ParserState.STRING

        result += symbol

    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
