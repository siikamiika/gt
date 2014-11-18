"""This module contains the `preprocess' function that converts JavaScript
objects into JSON ones."""

def preprocess(source):
    """Converts JavaScript-compatible data structures sent by google to a valid
    JSON.

    The only known differences are:
        1) 'null' omitting inside arrays;
        2) optional meaningless comma before ']'.

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
        """ Insert next symbol to the result as-is """
        NORMAL = 1
        """ Insert 'null' to the result if next symbol is comma """
        COMMA = 2
        """ Inside a string """
        STRING = 3
        """ Inside a string, previos character is a backslash """
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
