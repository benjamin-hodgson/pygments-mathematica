from pygments.lexer import RegexLexer, bygroups, include, using, this
from pygments.token import *
import re

class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'Mathematica']
    filenames = ['*.m']
    
    def definition(lexer, match):
        # This doesn't work! That's why it's not actually used anywhere.
        
        # r'^([a-z][A-Za-z0-9]*)(\[.*?\])(\s*)(:?=)(\s*)(.*?)$'
        yield match.start(1), Name.Function, match.group(1)
        for posn, tokentype, token in lexer.get_tokens_unprocessed(match.group()[match.end(1):]):
            yield posn, tokentype, token
        yield match.start(2), Punctuation, '['
        
        arguments = [arg + ',' for arg in match.group(2)[1:-1].split(',')][:-1]
        posn = match.start(2) + 1
        variable_list = []
        for arg in arguments:
            argmatch = re.match(r'(\s*)([A-Za-z0-9,_\?]+)(_\??)([A-Za-z0-9]*)(,?)', arg)
            for tokentype, value in zip([Whitespace, Name.Variable,
                                         Punctuation, None, Punctuation],
                                        argmatch.groups()):
                if value:
                    if tokentype is None:  # deals with '_?NumericQ' and similar
                        tokentype = Name.Builtin if value[1].isupper() else Name
                    yield posn, tokentype, value
                    posn += len(value)
                if tokentype is Name.Variable: variable_list.append(value)
        
        yield match.end(2) - 1, Punctuation, ']'
        if match.group(3): yield match.start(3), Whitespace, match.group(3)
        yield match.start(4), Punctuation, match.group(4)
        if match.group(5): yield match.start(5), Whitespace, match.group(5)
        
        for tup in lexer.get_tokens_unprocessed(match.group(6)):
            yield tup
        
    def LHS(lexer, match, ctx=None):
        print('entering LHS')
        s = match.start()
        for i, t, v in lexer.get_tokens_unprocessed(match.group()):
            new_t = Name.Function if t is Name else t
            yield i + s, new_t, v
        if ctx:
            ctx.pos = match.end()
    
    tokens = {
        'root': [
            (r'\(\*', Comment, 'comment'),  # comments (* look like this *)
            (r'\s+', Whitespace),
            (r'(?s)".*?"', String),
            (r'\\\[\w*?\]', Error),
            include('numbers'),
            include('names'),
            include('symbols')
        ],
        'numbers': [
            (r'[\+\-]?[0-9]+\.[0-9]*[eE]?[\+\-]?[0-9]*', Number.Float),
            (r'[\+\-]?[0-9]+', Number.Integer)
        ],
        'symbols': [
            (r'[\+\-/*=^:<>@~\.]', Operator),
            (r'[\[\]\(\){}]', Punctuation),  # various braces
            (r'[,;_&\?]', Punctuation)
        ],
        'comment': [
            (r'[^\*\(\)]+', Comment),
            (r'\(\*', Comment, '#push'),
            (r'\*\)', Comment, '#pop'),
            (r'[\(\)\*]', Comment)  # star or brackets on their own
        ],
        'names': [
            (r'[A-Z][A-Za-z0-9]*', Name.Builtin),  # builtins start with a capital letter
            (r'^([A-Za-z0-9,\s{}]+)(\[?.*?\]?)(\s*)(:?=)(\s*)(.*?)$',
             bygroups(LHS, using(this), Whitespace, Operator, Whitespace,
                      using(this))),
            (r'[a-z][A-Za-z0-9]*', Name),  # user-defined names start with lowercase
            (r'#[0-9]*', Name.Variable)
        ]
    }
